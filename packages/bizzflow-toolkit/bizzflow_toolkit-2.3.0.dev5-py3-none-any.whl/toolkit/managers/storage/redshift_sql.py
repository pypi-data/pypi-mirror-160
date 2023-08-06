import logging
from typing import List, Optional

from toolkit.base import Kex, ObjectMetadata
from toolkit.base.table import Table, TableDetails, TableSchema
from toolkit.managers.file_storage import S3FileStorageManager
from toolkit.managers.file_storage.base import BaseFileStorageManager
from toolkit.managers.storage import PostgreSQLStorageManager
from toolkit.utils.helpers import humanize_size
from toolkit.utils.redshift_connector import RedshiftConnectorIAM

logger = logging.getLogger(__name__)


class RedshiftStorageManager(PostgreSQLStorageManager):
    """Redshift SQL Storage Manager"""

    def __init__(
        self, database, db_user, cluster_identifier, aws_access_key_id, aws_secret_access_key, session_token, region
    ):
        self.database = database
        self._connector = RedshiftConnectorIAM(
            database=database,
            db_user=db_user,
            cluster_identifier=cluster_identifier,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            session_token=session_token,
            region=region,
        )

    def get_table_details(self, table: Table):

        with self._connector:
            result = self._connector.execute(
                f"""SELECT size, tbl_rows FROM SVV_TABLE_INFO WHERE "schema" = '{table.kex.kex}' AND "table" = '{table.table}';"""
            )
            size = result[0]["size"]
            tbl_rows = result[0]["tbl_rows"]

        table.details = TableDetails(
            created=None,
            description=None,
            location=None,
            modified=None,
            size=size,
            size_readable=humanize_size(size),
            num_rows=tbl_rows,
            path=None,
            schema=[TableSchema(name, type, None) for name, type in self.get_table_columns(table).items()],
        )
        return table.details or TableDetails()

    def get_kex_metadata(self, kex: Kex) -> Optional[ObjectMetadata]:
        with self._connector:
            result = self._connector.execute(
                f"""SELECT "description" FROM pg_catalog.pg_description WHERE objoid = (SELECT oid FROM pg_catalog.pg_namespace where nspname = '{kex.kex}');"""
            )
            comment = result[0].get("description")
        if comment:
            try:
                metadata = ObjectMetadata.from_payload(comment)
                return metadata
            except ValueError:
                logger.error(f"Failed to get metadata for kex {kex}", exc_info=True)
        return None

    def load_table_from_s3_storage(self, table: Table, path: str, file_storage_manager: S3FileStorageManager):
        """Load table from AWS S3 input bucket to redshift schema

        Arguments:
            table {Table}

            path {str} -- path to table in uri format
        """
        # TODO: need to be tested properly with S3
        path = file_storage_manager.get_absolute_path(path)
        iam_role = file_storage_manager.aws_iam_role
        with self._connector:
            self._connector.execute(
                f"COPY TABLE {self._escaped_full_table_name(table)} FROM '{path}' iam_role {iam_role} FORMAT CSV;"
            )
        logger.info("Loaded %s from %s", table.get_full_id(), path)

    def export_to_file_storage(self, table: Table, path: str, file_storage_manager: BaseFileStorageManager):
        if isinstance(file_storage_manager, S3FileStorageManager):
            self.export_to_s3_storage(table, path, file_storage_manager)
        else:
            super().export_to_file_storage(table, path, file_storage_manager)

    def export_to_s3_storage(self, table: Table, path: str, file_storage_manager: S3FileStorageManager):
        """Export specified table to .csv in AWS S3

        Arguments:
            table {Table}

            path {str} -- path to table in uri format
        """
        # TODO: need to be tested properly with S3
        path = file_storage_manager.get_absolute_path(path)
        table_id = table.get_full_id()
        iam_role = file_storage_manager.aws_iam_role
        with self._connector:
            self._connector.execute(
                f"""UNLOAD ('SELECT * FROM {self._escaped_full_table_name(table)}') TO '{path}' IAM_ROLE '{iam_role}' ALLOWOVERWRITE CSV GZIP HEADER DELIMITER AS ',';"""
            )
        logger.info("Exported %s to %s", table_id, path)

    def _incremental_load(self, table: Table, destination: Table, primary_keys: List[str], mark_deletes: bool):
        """Load incremental data from table to destination table"""
        self._incremental_insert(table, destination, primary_keys)
        self._incremental_update(table, destination, primary_keys)
        if mark_deletes:
            self._mark_deletes(table, destination, primary_keys)

    def _incremental_insert(self, table: Table, destination: Table, primary_keys: List[str]):
        """Insert rows when primary keys not match

        Arguments:
            source {Table}
            destination {Table}
            primary_key_concat {str} -- string get by _get_primary_key_concat
        """
        destination_full_table_name = f"{self._escaped_full_table_name(destination)}"
        source_full_table_name = f"{self._escaped_full_table_name(table)}"
        all_columns_names = [
            column for column in self.get_table_columns(table).keys() if column not in self.RESERVED_COLUMNS
        ]
        destination_all_columns = ", ".join((f'"{column}"' for column in [*all_columns_names, *self.RESERVED_COLUMNS]))
        source_all_columns = ", ".join((f'S."{column}"' for column in all_columns_names))
        t_all_columns = ", ".join((f'T."{column}"' for column in all_columns_names))

        primary_keys_equal_condition = " AND ".join((f'S."{column}" = D."{column}"' for column in primary_keys))

        destination_primary_is_null = " AND ".join((f'D."{column}" IS NULL' for column in primary_keys))
        query = f"""
            INSERT INTO {destination_full_table_name} ({destination_all_columns})
            SELECT {t_all_columns}, {self.get_current_timestamp_value()}, '{self.LAST_OPERATION_INSERT}'
            FROM 
                (SELECT {source_all_columns} FROM {source_full_table_name} S
                LEFT JOIN {destination_full_table_name} D ON {primary_keys_equal_condition}
                WHERE {destination_primary_is_null}) T
            """
        with self._connector:
            self._connector.execute(query)
        logger.info(f"Insert rows from {table} to {destination}")

    def _incremental_update(self, table: Table, destination: Table, primary_keys: List[str]):
        """Update rows when primary keys match but at least one other value differs

        Arguments:
            source {Table}
            destination {Table}
            primary_key_concat {str} -- string get by _get_primary_key_concat
        """
        destination_full_table_name = f"{self._escaped_full_table_name(destination)}"
        source_full_table_name = f"{self._escaped_full_table_name(table)}"
        all_columns_names = [
            column for column in self.get_table_columns(table).keys() if column not in self.RESERVED_COLUMNS
        ]
        all_columns_not_equal_condition = " OR ".join(
            (
                f"""COALESCE(S."{column}!={destination_full_table_name}."{column}, S."{column} IS NOT NULL OR {destination_full_table_name}."{column} IS NOT NULL)"""
                for column in all_columns_names
            )
        )
        columns_assign = ", ".join((f'"{column}" = S."{column}"' for column in all_columns_names))
        primary_keys_equal_condition = " AND ".join(
            (f'S."{column}" = {destination_full_table_name}."{column}"' for column in primary_keys)
        )

        query = f"""
            UPDATE {destination_full_table_name}
            SET {columns_assign}, "{self.LAST_OPERATION_COLUMN}" = '{self.LAST_OPERATION_UPDATE}', "{self.TIMESTAMP_COLUMN}" = {self.get_current_timestamp_value()}
            FROM {source_full_table_name} S
            WHERE {primary_keys_equal_condition} AND ({all_columns_not_equal_condition})
            """
        with self._connector:
            self._connector.execute(query)
        logger.info(f"Update rows from {table} to {destination}")

    def _mark_deletes(self, table: Table, destination: Table, primary_keys: List[str]):
        """Mark rows as deleted when coping table incrementally.

        Arguments:
            source {Table}
            destination {Table}
            primary_key_concat {str} -- string get by _get_primary_key_concat
        """
        destination_full_table_name = f"{self._escaped_full_table_name(destination)}"
        source_full_table_name = f"{self._escaped_full_table_name(table)}"

        primary_keys_equal_condition = " AND ".join((f'S."{column}" = D."{column}"' for column in primary_keys))
        destination_primary_columns = ", ".join((f'D."{column}"' for column in primary_keys))
        t_primary_keys_equal_condition = " AND ".join(
            (f'{destination_full_table_name}."{column}" = T."{column}"' for column in primary_keys)
        )
        source_primary_is_null = " AND ".join((f'S."{column}" IS NULL' for column in primary_keys))

        query = f"""
            UPDATE {destination_full_table_name}
            SET "{self.LAST_OPERATION_COLUMN}" = '{self.LAST_OPERATION_DELETE}', "{self.TIMESTAMP_COLUMN}" = {self.get_current_timestamp_value()}
            FROM 
                (SELECT {destination_primary_columns} FROM {destination_full_table_name} D
                LEFT JOIN {source_full_table_name} S ON {primary_keys_equal_condition}
                WHERE {source_primary_is_null}) T
            WHERE "{self.LAST_OPERATION_COLUMN}" != '{self.LAST_OPERATION_DELETE}' AND {t_primary_keys_equal_condition}
            """
        with self._connector:
            self._connector.execute(query)
        logger.info(f"Mark deleted rows from {table} to {destination}")

    def shared_table_destinations(self, table: Table):
        # TODO: add table sharing logic once redshift manager supports sharing
        return []
