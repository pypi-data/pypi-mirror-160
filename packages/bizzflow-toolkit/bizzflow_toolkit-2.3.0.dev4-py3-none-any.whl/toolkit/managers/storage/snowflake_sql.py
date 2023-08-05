"""Snowflake Storage Manager

Provides functions to manage AWS S3 storage based on Snowflake.
"""

import os
from datetime import datetime
from logging import getLogger
from typing import List, Optional, Tuple, Union

from toolkit.base.kex import Kex
from toolkit.base.metadata import ObjectMetadata
from toolkit.base.table import Table, TableDetails, TableSchema
from toolkit.managers.file_storage.base import BaseFileStorageManager
from toolkit.managers.file_storage.s3 import S3FileStorageManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.managers.vault.base import BaseVaultManager
from toolkit.utils.helpers import humanize_size

logger = getLogger(__name__)

try:
    from snowflake.connector import Connect as SnowflakeConnection
    from snowflake.connector import DictCursor
except ImportError:
    logger.info("Snowflake libraries are not installed, install snowflake extras.")


class SnowflakeStorageManager(BaseStorageManager):
    """Manage flow of data inside AWS S3, Snowflake and between them."""

    LAST_OPERATION_COLUMN_TYPE = "VARCHAR(1)"
    TIMESTAMP_COLUMN_COLUMN_TYPE = "VARCHAR(16777216)"
    DEFAULT_COLUMN_TYPE = "VARCHAR(16777216)"
    QUOTATION_MARK = '"'
    TRANSLATION_INPUT = "áéěíýóúůžščřďťň .-"
    TRANSLATION_OUTPUT = "aeeiyouuzscrdtn___"

    def __init__(self, vault_manager: BaseVaultManager, account, warehouse, database):
        """Initiate Snowflake Storage Manager

        Arguments:
            snf_connection {SnowflakeConnection, optional} -- Snowflake connection. Defaults to ORCHESTRATOR role connection.

            default_role {int, optional} -- Default role to be used by connection, defaults to ORCHESTRATOR

            vault_manager {VaultManager, optional} -- Vault manager containing connection credentials. Default project vault manager is used when None
        """
        self.vault_manager = vault_manager
        self.account = account
        self.warehouse = warehouse
        self.database = database
        # create connection and keep it alive - until it is closed - keep alive works in heartbeat by default
        # every 3600 seconds
        user = "ORCHESTRATOR"
        password = self.vault_manager.get_credentials("snowflake-{}".format(user))
        if password is None:
            logger.error("Could not find password for Snowflake user %s", user)
            raise ValueError("Could not find password for Snowflake user {}".format(user))

        self.snf_connection = SnowflakeConnection(
            user=user,
            password=password,
            account=self.account,
            warehouse=self.warehouse,
            database=self.database,
            client_session_keep_alive=True,
        )

    def get_current_timestamp_value(self):
        return f"'{datetime.now().isoformat()}'"

    @property
    def project(self) -> str:
        """Return kex project name"""
        return self.database

    def list_tables(self, kex: Kex):
        """List all tables in specified kex

        Arguments:
            kex {Kex}

        Returns:
            tables {list} -- List of Table objects in specified kex
        """
        cursor = self.snf_connection.cursor()
        r = cursor.execute(f'DESCRIBE SCHEMA "{self.database}"."{kex.kex}";')
        tbl = r.fetchall()
        return [Table(row[1], kex) for row in tbl if row[2] == "TABLE"]

    def drop_column(self, table: Table, column_name: str):
        """Drop column from table"""
        cursor = self.snf_connection.cursor()
        cursor.execute(f'ALTER TABLE "{self.database}"."{table.kex.kex}"."{table.table}" DROP COLUMN "{column_name}"')

    def get_table_details(self, table: Table):
        """Get table details ~ selected snowflake table attributes

        Arguments:
            table {Table}

        Returns:
            table.details {TableDetails}
        """
        cursor = self.snf_connection.cursor(DictCursor)
        r = cursor.execute(f'SHOW TABLES LIKE \'{table.table}\' IN "{self.database}"."{table.kex.kex}";')
        result = r.fetchall()
        for res in result:
            table.details = TableDetails(
                created=res["created_on"].strftime("%Y-%m-%d %H:%M:%S"),
                description=res["comment"],
                location=None,
                modified=None,
                size=None,
                size_readable=humanize_size(res["bytes"]),
                num_rows=res["rows"],
                path=None,
                schema=[
                    TableSchema(name, data_type, None) for name, data_type in self.get_table_columns(table).items()
                ],
            )
        cursor.close()
        return table.details or TableDetails()

    def set_kex_metadata(self, kex: Kex, metadata: ObjectMetadata):
        """Set kex metadata as schema's comment text"""
        cursor = self.snf_connection.cursor()
        cursor.execute(f"""COMMENT ON SCHEMA "{self.database}"."{kex.kex}" IS '{metadata.payload}';""")

    def set_table_metadata(self, table: Table, metadata: ObjectMetadata):
        """Set table metadata as tables's comment text"""
        cursor = self.snf_connection.cursor()
        cursor.execute(f"""COMMENT ON TABLE {self._escaped_full_table_name(table)} IS '{metadata.payload}';""")

    def get_kex_metadata(self, kex: Kex) -> Optional[ObjectMetadata]:
        """Returns kex metadata if they were previously stored in a schema's comment"""
        cursor = self.snf_connection.cursor(DictCursor)
        cursor.execute(
            f"""SELECT "COMMENT" FROM "{self.database}"."INFORMATION_SCHEMA"."SCHEMATA" WHERE SCHEMA_NAME='{kex.kex}';"""
        )
        comment = cursor.fetchone().get("COMMENT")
        if comment:
            try:
                metadata = ObjectMetadata.from_payload(comment)
                return metadata
            except ValueError:
                logger.error("Failed to get metadata for kex %s", kex.kex, exc_info=True)
        return None

    def get_table_metadata(self, table: Table) -> Optional[ObjectMetadata]:
        """Returns table metadata if they were previously stored in table's comment"""
        cursor = self.snf_connection.cursor(DictCursor)
        cursor.execute(
            f"""SELECT "COMMENT" FROM "{self.database}"."INFORMATION_SCHEMA"."TABLES" WHERE TABLE_NAME='{table.table}' AND TABLE_SCHEMA='{table.kex.kex}';"""
        )
        comment = cursor.fetchone().get("COMMENT")
        if comment:
            try:
                metadata = ObjectMetadata.from_payload(comment)
                return metadata
            except ValueError:
                logger.error("Failed to get metadata for table %s", table.get_id(), exc_info=True)
        return None

    def create_table(self, table: Table, fields: List[Union[str, Tuple[str, str]]]):

        table_id = table.get_full_id()
        table_objects = self.list_tables(table.kex)
        if table_id in [t.get_full_id() for t in table_objects]:
            logger.warning("Table with following id '%s' already exists", table_id)
        else:
            cursor = self.snf_connection.cursor()
            fieldset = []
            for field in fields:
                if isinstance(field, str):
                    fieldset.append((field, self.DEFAULT_COLUMN_TYPE))
                elif hasattr(field, "__getitem__") and len(field) == 2:
                    fieldset.append(field)
            fieldlist = ", ".join(['"{}" {}'.format(self.normalize_string(f[0]), f[1]) for f in fieldset])

            query = f"CREATE TABLE {self._escaped_full_table_name(table)} ({fieldlist});"

            logger.debug(query)
            cursor.execute(query)
            logger.info("Created table '%s'", table_id)
            cursor.close()

    def delete_table(self, table: Table):
        """Delete table with specified name in specified kex

        Arguments:
            table {Table}
        """
        table_id = table.get_full_id()
        cursor = self.snf_connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self._escaped_full_table_name(table)} CASCADE;")
        logger.info("Deleted table '%s'.", table_id)
        cursor.close()

    def truncate_table(self, table: Table):
        """Truncate table with specified name in specified kex

        Arguments:
            table {Table}

        Raises:
            Exception: In case of problems with query job
        """
        table_id = table.get_full_id()
        cursor = self.snf_connection.cursor()
        cursor.execute(f"TRUNCATE TABLE IF EXISTS {self._escaped_full_table_name(table)};")
        logger.info("Truncated table '%s'.", table_id)
        cursor.close()

    def load_table_from_s3_storage(self, table: Table, path: str, file_storage_manager: S3FileStorageManager):
        """Load table from AWS S3 input bucket to Snowflake schema

        Arguments:
            table {Table}

            path {str} -- path to table in uri format
        """
        path = file_storage_manager.get_absolute_path(path)
        try:
            cursor = self.snf_connection.cursor()
            cursor.execute(
                f"COPY INTO {self._escaped_full_table_name(table)} FROM '{path}' credentials=(aws_key_id='{file_storage_manager.aws_access_key_id}' aws_secret_key='{file_storage_manager.aws_secret_access_key}') file_format=(type='csv' skip_header = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '\"');"
            )
            cursor.close()
        except Exception as e:
            logger.error(f"Failed to load table {table}")
            raise Exception(e)

    def _copy_table(self, source_table: Table, destination_table: Table, exists_ok: bool = True):
        """Copy table from one Snowflake dataset to another

        Arguments:
            source_table {Table}

            destination_table {Table}

            exists_ok {boolean} -- If True, truncate and update schema of existing table
        """
        source_table_id = source_table.get_full_id()
        destination_table_id = destination_table.get_full_id()

        if self.table_exists(destination_table):
            if exists_ok:
                # check schema if destination table already exists and raise exception whe it is not compatible
                self.check_tables_columns_compatibility(source_table, destination_table)
            else:
                raise ValueError("Destination table '{}' exists.".format(destination_table_id))
        cursor = self.snf_connection.cursor()
        cursor.execute(
            f"CREATE OR REPLACE TABLE {self._escaped_full_table_name(destination_table)} CLONE {self._escaped_full_table_name(source_table)};"
        )
        cursor.close()
        logger.info("Copy table: '%s' to '%s'", source_table_id, destination_table_id)

    def _preview(self, table: Table, number_results: int):
        """Preview random specified number of rows from specified table

        Arguments:
            table {Table}

            number_results {int} --  Number of results to be returned

        Returns:
            Dictionary with specified number of rows from specified table
        """
        cursor = self.snf_connection.cursor(DictCursor)
        columns_string = ", ".join((f'"{column}"' for column in self.get_table_columns(table).keys()))
        r = cursor.execute(
            f"SELECT {columns_string} FROM {self._escaped_full_table_name(table)} LIMIT {number_results};"
        )
        result = r.fetchall()
        cursor.close()
        return {"rows": result}

    def describe(self, kex: Kex):
        """Describe specified kex

        Arguments:
            kex {Kex}

        Returns:
            dictionary with basic information about Snowflake schema
        """
        cursor = self.snf_connection.cursor(DictCursor)
        r = cursor.execute(f"SHOW SCHEMAS LIKE '{kex.kex}' IN '{self.database}';")
        result = r.fetchall()
        tables = []
        for table in self.list_tables(kex):
            tables.append(table.get_full_id())
        cursor.close()
        for res in result:
            return {
                "name": res["name"],
                "full_name": kex.get_id(),
                "created": res["created_on"].strftime("%Y-%m-%d %H:%M:%S"),
                "modified": None,
                "description": res["comment"],
                "location": None,
                "tables": tables,
            }

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
        path = file_storage_manager.get_absolute_path(path)
        table_id = table.get_full_id()
        cursor = self.snf_connection.cursor()
        cursor.execute(
            f"""COPY INTO '{path}' FROM {self._escaped_full_table_name(table)} credentials=(aws_key_id='{file_storage_manager.aws_access_key_id}' aws_secret_key='{file_storage_manager.aws_secret_access_key}') file_format=(type='csv' field_delimiter=',' FIELD_OPTIONALLY_ENCLOSED_BY = '"' COMPRESSION='GZIP' FILE_EXTENSION=''  EMPTY_FIELD_AS_NULL=TRUE NULL_IF=('', 'NULL', 'null', '\\N')) HEADER=TRUE overwrite=true;"""
        )
        cursor.close()
        logger.info("Exported %s to %s", table_id, path)

    def list_kexes(self):
        """List all schemas in database.
        This turns out to be a lot faster than SELECTing from INFORMATION_SCHEMA
        """
        cursor = self.snf_connection.cursor()
        r = cursor.execute(f'SHOW SCHEMAS IN DATABASE "{self.database}";')
        kxs = r.fetchall()
        return [Kex(row[1], self.database) for row in kxs]

    def create_kex(self, kex: Kex):
        kex_id = kex.get_id()
        if kex_id in [k.get_id() for k in self.list_kexes()]:
            logger.warning("Kex with following id '%s' already exists.", kex_id)
        else:
            cursor = self.snf_connection.cursor()
            cursor.execute(f'CREATE SCHEMA "{self.database}"."{kex.kex}";')
            logger.info("Created kex '%s'.", kex_id)
            cursor.close()

    def delete_kex(self, kex: Kex):
        kex_id = kex.get_id()
        cursor = self.snf_connection.cursor()
        cursor.execute(f'DROP SCHEMA IF EXISTS "{self.database}"."{kex.kex}" CASCADE;')
        logger.info("Deleted kex '%s'.", kex_id)
        cursor.close()

    def append_columns(self, table, columns):
        current_columns = self.get_table_columns(table)
        columns_string = []
        for column_name, column_type, value in columns:
            if column_name in current_columns:
                logger.info(f"Column {column_name} is already in table {table}")
            else:
                logger.info(f"Append column {column_name} to table {table}")
                column_string = f""""{column_name}" {column_type}"""
                if value:
                    column_string += f" NOT NULL DEFAULT {value}"
                columns_string.append(column_string)

        if columns_string:
            query = f"""ALTER TABLE {self._escaped_full_table_name(table)} ADD {", ".join(columns_string)};"""
            cursor = self.snf_connection.cursor()
            cursor.execute(query)
        else:
            logger.info("No columns to add")

    def _escaped_full_table_name(self, table: Table):
        return f'"{self.database}"."{table.kex.kex}"."{table.table}"'

    def _incremental_load(self, table: Table, destination: Table, primary_keys: List[str], mark_deletes: bool):
        all_columns_names = [
            column for column in self.get_table_columns(table).keys() if column not in self.RESERVED_COLUMNS
        ]

        all_columns_not_equal_condition = " OR ".join(
            (f"""NOT(EQUAL_NULL(S."{column}", D."{column}"))""" for column in all_columns_names)
        )

        columns_assign = ", ".join((f'"{column}" = S."{column}"' for column in all_columns_names))

        match_statement = f"""WHEN MATCHED AND ({all_columns_not_equal_condition}) THEN UPDATE SET  {columns_assign}, "{self.TIMESTAMP_COLUMN}"={self.get_current_timestamp_value()}, "{self.LAST_OPERATION_COLUMN}"= '{self.LAST_OPERATION_UPDATE}' """

        destination_all_columns = ", ".join((f'"{column}"' for column in [*all_columns_names, *self.RESERVED_COLUMNS]))
        source_all_columns = ", ".join((f'S."{column}"' for column in all_columns_names))
        not_match_statement = f"""WHEN NOT MATCHED THEN INSERT ({destination_all_columns}) VALUES ({source_all_columns}, {self.get_current_timestamp_value()}, '{self.LAST_OPERATION_INSERT}')"""

        primary_keys_equal_condition = " AND ".join((f'S."{column}" = D."{column}"' for column in primary_keys))

        query = f"""MERGE INTO {self._escaped_full_table_name(destination)} D USING {self._escaped_full_table_name(table)} S ON {primary_keys_equal_condition} {match_statement} {not_match_statement};"""

        cursor = self.snf_connection.cursor()
        cursor.execute(query)
        logger.info(f"New increment for table '{destination}' - inserted {cursor.rowcount} rows")
        cursor.close()

        if mark_deletes:
            # mark rows as deleted
            self._mark_deletes(table, destination, primary_keys)

    def _mark_deletes(self, table: Table, destination: Table, primary_keys: list):
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
        t_primary_keys_equal_condition = " AND ".join((f'D."{column}" = T."{column}"' for column in primary_keys))
        source_primary_is_null = " AND ".join((f'S."{column}" IS NULL' for column in primary_keys))

        query = f"""
            UPDATE {destination_full_table_name} D
            SET D."{self.LAST_OPERATION_COLUMN}" = '{self.LAST_OPERATION_DELETE}', D."{self.TIMESTAMP_COLUMN}" = {self.get_current_timestamp_value()}
            FROM 
                (SELECT {destination_primary_columns} FROM {destination_full_table_name} D
                LEFT JOIN {source_full_table_name} S ON {primary_keys_equal_condition}
                WHERE {source_primary_is_null}) T
            WHERE D."{self.LAST_OPERATION_COLUMN}" != '{self.LAST_OPERATION_DELETE}' AND {t_primary_keys_equal_condition}
            """

        cursor = self.snf_connection.cursor()
        cursor.execute(query)
        logger.info(f"{cursor.rowcount} rows was marked as deleted in table '{destination}'")
        cursor.close()

    def _filter_table(self, table: Table, destination: Table, filter_query: str):
        query = f"CREATE OR REPLACE TABLE {self._escaped_full_table_name(destination)} AS SELECT * FROM {self._escaped_full_table_name(table)} WHERE {filter_query};"
        cursor = self.snf_connection.cursor()
        cursor.execute(query)
        cursor.close()
        source_table_info = self.get_table_details(table)
        destination_table_info = self.get_table_details(destination)
        filtered_rows = source_table_info.num_rows - destination_table_info.num_rows
        logger.info(
            f"Filtered {filtered_rows} rows from {source_table_info.num_rows} rows from table: '{table}' to '{destination}', {destination_table_info.num_rows} rows left",
        )

    def _whitelist_table(self, table, destination, columns):
        fields = ", ".join(f'"{field}"' for field in columns)
        query = f"""CREATE OR REPLACE TABLE {self._escaped_full_table_name(destination)} AS SELECT {fields} FROM {self._escaped_full_table_name(table)};"""
        cursor = self.snf_connection.cursor()
        cursor.execute(query)
        logger.debug(query)
        cursor.close()
        logger.info(f"Whitelist {len(columns)}: {columns} from {table} to {destination}")

    def _union_table(self, tables, destination, distinct):
        union_type = "UNION" if distinct else "UNION ALL"
        first_table = tables[0]
        fields = ", ".join(f'"{field}"' for field in self.get_table_columns(first_table).keys())
        unions = f"""SELECT {fields} FROM {self._escaped_full_table_name(first_table)} """
        for table in tables[1:]:
            unions += f"""{union_type} SELECT {fields} FROM {self._escaped_full_table_name(table)} """
        query = f"""CREATE OR REPLACE TABLE  {self._escaped_full_table_name(destination)} AS {unions};"""
        cursor = self.snf_connection.cursor()
        cursor.execute(query)
        cursor.close()
        logger.debug(query)
        logger.info(f"Union tables {tables} to {destination}")

    def get_table_columns(self, table):
        cursor = self.snf_connection.cursor(DictCursor)
        r = cursor.execute(f"DESC TABLE {self._escaped_full_table_name(table)};")
        result = r.fetchall()
        cursor.close()
        return {res["name"]: res["type"] for res in result}

    def list_shared_out_tables(self):
        # TODO: add table sharing logic once BQ manager supports sharing
        return []

    def shared_out_table_destinations(self, table: Table):
        # TODO: add table sharing logic once snowflake manager supports sharing
        return []
