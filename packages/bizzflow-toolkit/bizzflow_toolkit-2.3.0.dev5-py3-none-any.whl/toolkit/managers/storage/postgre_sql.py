import csv
import logging
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from toolkit.base.kex import Kex
from toolkit.base.metadata import ObjectMetadata
from toolkit.base.table import Table, TableDetails, TableSchema
from toolkit.managers.file_storage import LocalFileStorageManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.utils.postre_sql import PostgreSQLConnector

# PyODBC does not support loading from STDIN
# Using fast_executemany turns out to be 3 times slower than using bcp / psql to load
# https://github.com/mkleehammer/pyodbc/issues/350
# I see no other way than using psycopg2 for loading.
# I would like to see the PSQL Storage Manager rewritten
# using psycopg2 altogether, but that would be a huge setback right now.
# Also, calling `psql` directly using a subprocess would be possible,
# but we have experience using `bcp` like that and there were always
# troubles with that.


logger = logging.getLogger(__name__)


class PostgreSQLStorageManager(BaseStorageManager):
    """Postgre SQL Storage Manager"""

    LAST_OPERATION_COLUMN_TYPE = "VARCHAR(1)"
    TIMESTAMP_COLUMN_COLUMN_TYPE = "TIMESTAMP"
    DEFAULT_COLUMN_TYPE = "VARCHAR(65535)"
    QUOTATION_MARK = '"'

    def __init__(self, host, database, username, password, port=5432, timeout=30):
        self.host = host
        self.port = port
        self.database = database
        self._connector = PostgreSQLConnector(
            self.host, self.database, username, password, timeout=timeout, port=self.port
        )

    @property
    def project(self) -> str:
        """Return kex project name"""
        return self.database

    def get_current_timestamp_value(self):
        return "CURRENT_TIMESTAMP"

    def get_kex_project(self) -> str:
        """Return kex project name"""
        return self.database

    def list_tables(self, kex: Kex) -> List[Table]:
        """List all tables in specified {kex}."""
        tables = []
        with self._connector:
            result = self._connector.execute(
                f"""SELECT "tablename" FROM "pg_catalog"."pg_tables" WHERE "schemaname" = '{kex.kex}';"""
            )
        for t in result:
            tables.append(Table(t["tablename"], kex))
        return tables

    def create_table(self, table: Table, fields: List[Union[str, Tuple[str, str]]]):
        """Crate table with specified name and structure

        Arguments:
            table {Table}
            fields {list} --  List of columns definitions consisting of a name
            and optional data type (e. g. ("name", "varchar(255)") or "name"
        """
        if self.table_exists(table):
            logger.info("Table with following id '%s' already exists", table.get_full_id())
            return

        fieldset = []
        for field in fields:
            if isinstance(field, str):
                fieldset.append((field, self.DEFAULT_COLUMN_TYPE))
            elif isinstance(field, (list, tuple)) and len(field) == 2:
                fieldset.append(field)
            else:
                raise ValueError("Unsupported field format")
        fieldlist = ", ".join([f'"{self.normalize_string(f[0])}" {f[1]}' for f in fieldset])

        with self._connector:
            self._connector.execute(f"""CREATE TABLE "{table.kex.kex}"."{table.table}" ({fieldlist});""")
        logger.info("Created table '%s' with fields (%s)", table.full_id, fieldlist)

    def load_table_from_local_storage(self, table: Table, path: str, file_storage_manager: LocalFileStorageManager):
        """Load csv into {table} from local file {path} using LocalFileStorageManager"""
        # TODO: use psycopg2's copy_from_expert for performance boost (as seen in wr-postgres)
        logger.info("Load table %s from local storage path %s", table, path)
        columns = self.get_table_columns(table)
        path = file_storage_manager.get_absolute_path(path)
        fieldset = [f'"{column}"' for column in columns]
        query = (
            f"""INSERT INTO "{table.kex.kex}"."{table.table}" ({", ".join(fieldset)}) """
            f"""VALUES ({", ".join(("?" for _ in fieldset))})"""
        )
        logger.info("Loading using query: %s", query)
        with self._connector, open(path, "r", encoding="utf-8", newline="") as src_fd:
            self._connector.cursor.fast_executemany = True
            reader = csv.reader(src_fd)
            try:
                # skip header
                next(reader)
            except StopIteration:
                logger.warning("File is empty, nothing to load.")
                return
            self._connector.cursor.executemany(query, reader)

    def delete_table(self, table: Table):
        """Delete {table}."""
        with self._connector:
            self._connector.execute(f"""DROP TABLE IF EXISTS "{table.kex.kex}"."{table.table}";""")
        logger.info("Deleted table '%s'.", table.get_full_id())

    def truncate_table(self, table: Table):
        """Truncate {table}."""
        with self._connector:
            self._connector.execute(f"""TRUNCATE TABLE "{table.kex.kex}"."{table.table}";""")
        logger.info("Truncated table '%s'.", table.get_full_id())

    def append_columns(self, table: Table, columns: List[Tuple[str, str, Optional[str]]]):
        current_columns = self.get_table_columns(table)
        for column_name, column_type, value in columns:
            if column_name in current_columns:
                logger.info(f"Column {column_name} is already in table {table}")
            else:
                logger.info(f"Append column {column_name} to table {table}")
                column_string = f""""{column_name}" {column_type}"""
                if value:
                    column_string += f" NOT NULL DEFAULT {value}"
                with self._connector:
                    self._connector.execute(f"""ALTER TABLE "{table.kex.kex}"."{table.table}" ADD  {column_string};""")

    def get_table_columns(self, table: Table) -> dict:
        columns_dict = {}
        with self._connector:
            result = self._connector.execute(
                f"""SELECT column_name, data_type, character_maximum_length, numeric_precision, numeric_scale FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{table.kex.kex}' AND TABLE_NAME='{table.table}';"""
            )
        for line in result:
            if line["character_maximum_length"] is not None:
                columns_dict[line["column_name"]] = f"{line['data_type']}({line['character_maximum_length']})"
            elif line["data_type"] in ("decimal", "numeric"):
                columns_dict[
                    line["column_name"]
                ] = f"{line['data_type']}({line['numeric_precision']}, {line['numeric_scale']})"
            else:
                columns_dict[line["column_name"]] = line["data_type"]
        return columns_dict

    def get_lines_from_table(self, table: Table) -> Iterable[Dict[str, Any]]:
        with self._connector:
            yield from self._connector.execute(
                f'''SELECT * FROM "{table.kex.kex}"."{table.table}"''', generator=True, chunk_size=1000
            )

    def get_kex_metadata(self, kex: Kex) -> Optional[ObjectMetadata]:
        with self._connector:
            result = self._connector.execute(f"SELECT obj_description('{kex.kex}'::regnamespace);")
            comment = result[0].get("obj_description")
        if comment:
            try:
                metadata = ObjectMetadata.from_payload(comment)
                return metadata
            except ValueError:
                self.logger.error(f"Failed to get metadata for kex {kex}", exc_info=True)
        return None

    def set_kex_metadata(self, kex: Kex, metadata: ObjectMetadata):
        with self._connector:
            self._connector.execute(f"""COMMENT ON SCHEMA "{kex.kex}" IS '{metadata.payload}';""")

    def get_table_metadata(self, table: Table) -> Optional[ObjectMetadata]:
        with self._connector:
            result = self._connector.execute(f"SELECT obj_description('{table.kex.kex}.{table.table}'::regclass);")
            comment = result[0].get("obj_description")
        if comment:
            try:
                metadata = ObjectMetadata.from_payload(comment)
                return metadata
            except ValueError:
                self.logger.error(f"Failed to get metadata for table {table}", exc_info=True)
        return None

    def set_table_metadata(self, table: Table, metadata: ObjectMetadata):
        with self._connector:
            self._connector.execute(f"""COMMENT ON TABLE "{table.kex.kex}"."{table.table}" IS '{metadata.payload}';""")

    def _copy_table(self, source_table: Table, destination_table: Table, exists_ok: bool = True):
        """Copy table

        Arguments:
            source_table {Table}

            destination_table {Table}

            exists_ok {boolean} -- If True, truncate and update schema of existing table
        """

        source_table_id = source_table.get_full_id()
        destination_table_id = destination_table.get_full_id()
        # check and append schema if destination table already exists
        if self.table_exists(destination_table):
            if exists_ok:
                self.check_tables_columns_compatibility(source_table, destination_table)
                self.delete_table(destination_table)
            else:
                raise ValueError("Destination table '{}' exists.".format(destination_table_id))
        with self._connector:
            self._connector.execute(
                f"CREATE TABLE {self._escaped_full_table_name(destination_table)} AS SELECT * FROM {self._escaped_full_table_name(source_table)};"
            )
        logger.info("Copy table: '%s' to '%s'", source_table_id, destination_table_id)

    def _preview(self, table: Table, number_results: int):
        """Preview random specified number of rows from specified table

        Arguments:
            table {Table}

            number_results {int} --  Number of results to be returned

        Returns:
            Dictionary with specified number of rows from specified table
        """

        with self._connector:
            result = self._connector.execute(
                f"SELECT * FROM {self._escaped_full_table_name(table)} ORDER BY random() LIMIT {number_results};"
            )
        return {"rows": result}

    def describe(self, kex: Kex):
        """Describe kex."""
        # probably not possible in POSTGRES without having own meta table
        tables = []
        for table in self.list_tables(kex):
            tables.append(table.get_full_id())
        return {
            "name": kex.kex,
            "full_name": kex.get_id(),
            "created": None,
            "modified": None,
            "description": None,
            "location": None,
            "tables": tables,
        }

    def get_table_details(self, table: Table):

        with self._connector:
            result = self._connector.execute(
                f"SELECT pg_size_pretty(pg_relation_size('{table.kex.kex}.{table.table}')), pg_relation_size('{table.kex.kex}.{table.table}');"
            )
            size = result[0]["pg_relation_size"]
            size_readable = result[0]["pg_size_pretty"]

            result = self._connector.execute(
                f'SELECT COUNT(1) as "rowcount" FROM {self._escaped_full_table_name(table)};'
            )
            num_rows = result[0]["rowcount"]

        table.details = TableDetails(
            created=None,
            description=None,
            location=None,
            modified=None,
            size=size,
            size_readable=size_readable,
            num_rows=num_rows,
            path=None,
            schema=[TableSchema(name, type, None) for name, type in self.get_table_columns(table).items()],
        )
        return table.details or TableDetails()

    def list_kexes(self):
        kexes = []
        with self._connector:
            result = self._connector.execute("""SELECT "nspname" FROM "pg_catalog"."pg_namespace";""")
        for item in result:
            kexes.append(Kex(item["nspname"], self.project))
        logger.debug(f"Found following kexes, {kexes}")
        return kexes

    def create_kex(self, kex: Kex):
        kex_id = kex.get_id()
        if kex_id in [k.get_id() for k in self.list_kexes()]:
            logger.warning("Kex with following id '%s' already exists.", kex_id)
        else:
            with self._connector:
                self._connector.execute(f"""CREATE SCHEMA "{kex.kex}";""")
                logger.info("Created kex '%s'.", kex_id)

    def delete_kex(self, kex: Kex):
        for table in self.list_tables(kex):
            self.delete_table(table)
        with self._connector:
            self._connector.execute(f"""DROP SCHEMA IF EXISTS "{kex.kex}";""")
            logger.info("Deleted kex '%s'.", kex.get_id())

    def _union_table(self, tables: List[Table], destination: Table, distinct: bool = False):
        union_type = "UNION" if distinct else "UNION ALL"
        first_table = tables[0]
        fields = ", ".join(self.get_table_columns(first_table).keys())
        unions = ""
        for table in tables[1:]:
            unions += f"{union_type} SELECT {fields} FROM {self._escaped_full_table_name(table)} "
        with self._connector:
            self._connector.execute(
                f"""CREATE TABLE  {self._escaped_full_table_name(destination)} AS SELECT {fields} FROM {self._escaped_full_table_name(first_table)} {unions};"""
            )
        logger.info(f"Union tables {tables} to {destination}")

    def _whitelist_table(self, table: Table, destination: Table, columns: List[str]):
        fields = ", ".join(columns)
        with self._connector:
            self._connector.execute(
                f"""CREATE TABLE {self._escaped_full_table_name(destination)} AS SELECT {fields} FROM {self._escaped_full_table_name(table)};"""
            )
        logger.info(f"Whitelist {len(columns)}: {columns} from {table} to {destination}")

    def _filter_table(self, table: Table, destination: Table, filter_query: str):
        with self._connector:
            self._connector.execute(
                f"""CREATE TABLE {self._escaped_full_table_name(destination)} AS SELECT * FROM {self._escaped_full_table_name(table)} WHERE {filter_query};"""
            )
        logger.info(f"Filter by {filter_query} from {table} to {destination}")

    def _escaped_full_table_name(self, table: Table):
        return f'"{self.database}"."{table.kex.kex}"."{table.table}"'

    def _get_primary_key_name(self, table: Table) -> str:
        """Get primary key name. Constraint's name must be unique within the database"""
        tid = table.get_id().replace(".", "_")
        return f"pk_{tid}"

    def _incremental_load(self, table: Table, destination: Table, primary_keys: List[str], mark_deletes: bool):
        all_columns_names = [
            column for column in self.get_table_columns(table).keys() if column not in self.RESERVED_COLUMNS
        ]
        columns_assign = ", ".join((f'''"{column}" = EXCLUDED."{column}"''' for column in all_columns_names))
        all_columns_str = ", ".join((f'"{column}"' for column in all_columns_names))
        primary_keys_str = ", ".join((f'"{column}"' for column in primary_keys))

        query = f"""INSERT INTO {self._escaped_full_table_name(destination)} ({all_columns_str}, "{self.TIMESTAMP_COLUMN}", "{self.LAST_OPERATION_COLUMN}") SELECT {all_columns_str}, {self.get_current_timestamp_value()}, '{self.LAST_OPERATION_INSERT}'  FROM {self._escaped_full_table_name(table)} ON CONFLICT ({primary_keys_str}) DO UPDATE SET {columns_assign}, "{self.TIMESTAMP_COLUMN}"={self.get_current_timestamp_value()}, "{self.LAST_OPERATION_COLUMN}"= '{self.LAST_OPERATION_UPDATE}'"""
        pkname = self._get_primary_key_name(destination)
        with self._connector:
            # SELECT INTO ... ON CONFLICT ... needs CONSTRAINT for conflict
            self._connector.execute(
                f'ALTER TABLE {self._escaped_full_table_name(destination)} DROP CONSTRAINT IF EXISTS "{pkname}"'
            )
            self._connector.execute(
                f'ALTER TABLE {self._escaped_full_table_name(destination)} ADD CONSTRAINT "{pkname}" PRIMARY KEY ({primary_keys_str})'
            )
            self._connector.execute(query)

        if mark_deletes:
            self._mark_deletes(table, destination, primary_keys)
        # Cleanup
        # We do not want primary key to mess with analytics
        with self._connector:
            self._connector.execute(
                f'ALTER TABLE {self._escaped_full_table_name(destination)} DROP CONSTRAINT IF EXISTS "{pkname}"'
            )

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
        t_primary_keys_equal_condition = " AND ".join((f'D."{column}" = T."{column}"' for column in primary_keys))
        source_primary_is_null = " AND ".join((f'S."{column}" IS NULL' for column in primary_keys))

        query = f"""
            UPDATE {destination_full_table_name} D
            SET "{self.LAST_OPERATION_COLUMN}" = '{self.LAST_OPERATION_DELETE}', "{self.TIMESTAMP_COLUMN}" = {self.get_current_timestamp_value()}
            FROM 
                (SELECT {destination_primary_columns} FROM {destination_full_table_name} D
                LEFT JOIN {source_full_table_name} S ON {primary_keys_equal_condition}
                WHERE {source_primary_is_null}) T
            WHERE D."{self.LAST_OPERATION_COLUMN}" != '{self.LAST_OPERATION_DELETE}' AND {t_primary_keys_equal_condition}
            """
        with self._connector:
            self._connector.execute(query)
        logger.info(f"Mark deleted rows from {table} to {destination}")

    def list_shared_out_tables(self):
        # TODO: add table sharing logic once BQ manager supports sharing
        return []

    def shared_out_table_destinations(self, table: Table):
        # TODO: add table sharing logic once postgres manager supports sharing
        return []
