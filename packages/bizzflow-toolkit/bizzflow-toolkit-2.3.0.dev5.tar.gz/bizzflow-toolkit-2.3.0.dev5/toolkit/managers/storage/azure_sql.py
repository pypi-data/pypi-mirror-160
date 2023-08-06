import logging
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from uuid import uuid4

from toolkit.base.kex import Kex
from toolkit.base.metadata import ObjectMetadata
from toolkit.base.table import Table, TableDetails, TableSchema
from toolkit.managers.file_storage.abs import ABSFileStorageManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.utils.azure_sql import AzureSQLConnector

logger = logging.getLogger(__name__)
try:
    import pyodbc
except ImportError:
    logger.info("PyODBC libraries are not installed, install azure extras.")


class AzureSQLSharedSourceConfig:
    def __init__(
        self,
        project_name: str,
        hostname: str,
        database: str,
        username: str,
        password: str,
    ):
        self.project_name = project_name
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password


class AzureSQLSharingConfig:
    def __init__(self, sources: Dict[str, AzureSQLSharedSourceConfig], destinations: Dict[str, List[str]]):
        """
        Args:
            sources:
            destinations: dict where tables full.id is key and value is list of projects to be shared into
        """
        self.sources = sources
        self.destinations = destinations


class AzureSQLStorageManager(BaseStorageManager):
    """Azure SQL Storage Manager"""

    LAST_OPERATION_COLUMN_TYPE = "VARCHAR(1)"
    TIMESTAMP_COLUMN_COLUMN_TYPE = "DATETIME"
    DEFAULT_COLUMN_TYPE = "VARCHAR(8000)"
    QUOTATION_MARK = '"'

    def __init__(
        self, host, database, username, password, port=1433, timeout=30, sharing: AzureSQLSharingConfig = None
    ):
        self.host = host
        self.port = port
        self.database = database
        self._connector = AzureSQLConnector(
            self.host, self.database, username, password, timeout=timeout, port=self.port
        )
        self.sharing = sharing or AzureSQLSharingConfig({}, {})
        self._connect_shared_data_sources()

    def get_current_timestamp_value(self):
        return "CURRENT_TIMESTAMP"

    @property
    def project(self) -> str:
        """Return kex project name"""
        return self.database

    def drop_column(self, table: Table, column_name: str):
        """Drop column from table"""
        with self._connector:
            self._connector.execute(f'UPDATE TABLE {self._escaped_full_table_name(table)} DROP COLUMN "{column_name}"')

    def list_tables(self, kex: Kex) -> List[Table]:
        """List all tables in specified {kex}."""
        tables = []
        with self._connector:
            result = self._connector.execute(
                f"""SELECT TABLE_NAME FROM "INFORMATION_SCHEMA"."TABLES" WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = '{kex.kex}';"""
            )
        for t in result:
            tables.append(Table(t["TABLE_NAME"], kex))
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
        logger.info("Created table '%s'", table.full_id)

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
            with self._connector:
                self._connector.execute(
                    f"""ALTER TABLE "{table.kex.kex}"."{table.table}" ADD {", ".join(columns_string)};"""
                )
        else:
            logger.info("No columns to add")

    def load_table_from_azure_blob_storage(self, table: Table, path: str, file_storage_manager: ABSFileStorageManager):
        path = file_storage_manager.get_absolute_path(path)

        blob_path = file_storage_manager.get_blob_name(path)
        blob_storage_location = file_storage_manager.container_url
        sas_token = file_storage_manager.get_sas_token(
            resource_kwargs={"object": True}, permission_kwargs={"read": True}
        )
        eds_name = f"BF{uuid4().hex}"
        with self._connector:
            self._connector.execute(
                f"""ALTER DATABASE SCOPED CREDENTIAL "{file_storage_manager.blob_storage_credential}" WITH IDENTITY = 'SHARED ACCESS SIGNATURE', SECRET='{sas_token}';"""
            )
            try:
                self._connector.execute(
                    f"""CREATE EXTERNAL DATA SOURCE "{eds_name}" WITH (TYPE = BLOB_STORAGE, LOCATION='{blob_storage_location}', CREDENTIAL="{file_storage_manager.blob_storage_credential}");"""
                )
                self._connector.execute(
                    f"""BULK INSERT "{table.kex.kex}"."{table.table}" FROM '{blob_path}' WITH (DATA_SOURCE='{eds_name}', FORMAT='CSV', CODEPAGE=65001, FIRSTROW=2, ROWTERMINATOR = '0x0a', TABLOCK);"""
                )
            finally:
                self._connector.execute(f"""DROP EXTERNAL DATA SOURCE "{eds_name}";""")

    def get_table_columns(self, table: Table) -> dict:
        columns_dict = {}
        with self._connector:
            result = self._connector.execute(
                f"""SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{table.kex.kex}' AND TABLE_NAME='{table.table}';"""
            )
        for line in result:
            if line["CHARACTER_MAXIMUM_LENGTH"] is not None:
                columns_dict[line["COLUMN_NAME"]] = f"{line['DATA_TYPE']}({line['CHARACTER_MAXIMUM_LENGTH']})"
            elif line["DATA_TYPE"] in ("decimal", "numeric"):
                columns_dict[
                    line["COLUMN_NAME"]
                ] = f"{line['DATA_TYPE']}({line['NUMERIC_PRECISION']}, {line['NUMERIC_SCALE']})"
            else:
                columns_dict[line["COLUMN_NAME"]] = line["DATA_TYPE"]
        return columns_dict

    def _get_schema_property(self, prop_name: str, schema: str) -> Optional[str]:
        with self._connector:
            result = self._connector.execute(
                f"SELECT CAST(ep.value as NVARCHAR(MAX)) as metadata FROM sys.extended_properties ep INNER JOIN sys.schemas s ON s.schema_id = ep.major_id WHERE s.name = '{schema}' AND ep.name = '{prop_name}';"
            )
        if not result:
            return None
        return result[0].get("metadata")

    def _create_schema_property(self, prop_name: str, schema: str, value: str):
        with self._connector:
            self._connector.execute(
                f"EXEC sp_addextendedproperty @name = N'{prop_name}', @value = '{value}', @level0type = N'Schema', @level0name = '{schema}';"
            )

    def _update_schema_property(self, prop_name: str, schema: str, value: str):
        with self._connector:
            self._connector.execute(
                f"EXEC sp_updateextendedproperty @name = N'{prop_name}', @value = '{value}', @level0type = N'Schema', @level0name = '{schema}';"
            )

    def _get_table_property(self, prop_name: str, schema: str, table: str) -> Optional[str]:
        with self._connector:
            result = self._connector.execute(
                (
                    "SELECT CAST(ep.value as NVARCHAR(MAX)) as metadata FROM sys.extended_properties ep "
                    f"INNER JOIN sys.tables t ON t.object_id = ep.major_id "
                    f"INNER JOIN sys.schemas s ON s.schema_id = t.schema_id "
                    f"WHERE t.name = '{table}' and s.name = '{schema}' and ep.name = '{prop_name}';"
                )
            )
        if not result:
            return None
        return result[0].get("metadata")

    def _create_table_property(self, prop_name: str, schema: str, table: str, value: str):
        with self._connector:
            self._connector.execute(
                f"EXEC sp_addextendedproperty @name = N'{prop_name}', @value = '{value}', @level0type = N'Schema', @level0name = '{schema}', @level1type = N'Table',  @level1name = '{table}';"
            )

    def _update_table_property(self, prop_name: str, schema: str, table: str, value: str):
        with self._connector:
            self._connector.execute(
                f"EXEC sp_updateextendedproperty @name = N'{prop_name}', @value = '{value}', @level0type = N'Schema', @level0name = '{schema}', @level1type = N'Table',  @level1name = '{table}';"
            )

    def get_kex_metadata(self, kex: Kex) -> Optional[ObjectMetadata]:
        """Get kex metadata from extended property 'Metadata'"""
        val = self._get_schema_property("Metadata", kex.kex)
        if val is None:
            return None
        try:
            metadata = ObjectMetadata.from_payload(val)
            return metadata
        except ValueError:
            logger.error("Could not deserialize metadata for kex %s", kex, exc_info=True)
        return None

    def set_kex_metadata(self, kex: Kex, metadata: ObjectMetadata):
        """Set kex metadata into extended property 'Metadata'"""
        val = self._get_schema_property("Metadata", kex.kex)
        if val is not None:
            self._update_schema_property("Metadata", kex.kex, metadata.payload)
            return
        self._create_schema_property("Metadata", kex.kex, metadata.payload)

    def get_table_metadata(self, table: Table) -> Optional[ObjectMetadata]:
        """Get table metadata from extended property 'Metadata'"""
        val = self._get_table_property("Metadata", table.kex.kex, table.table)
        if val is None:
            return None
        try:
            metadata = ObjectMetadata.from_payload(val)
            return metadata
        except ValueError:
            logger.error("Could not deserialize metadata for table %s", table, exc_info=True)
        return None

    def set_table_metadata(self, table: Table, metadata: ObjectMetadata):
        """Set table metadata into extended property 'Metadata'"""
        val = self._get_table_property("Metadata", table.kex.kex, table.table)
        if val is not None:
            self._update_table_property("Metadata", table.kex.kex, table.table, metadata.payload)
            return
        self._create_table_property("Metadata", table.kex.kex, table.table, metadata.payload)

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
                f"""SELECT * INTO  "{destination_table.kex.kex}"."{destination_table.table}" FROM "{source_table.kex.kex}"."{source_table.table}";"""
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
                f"""SELECT TOP {number_results} * FROM "{table.kex.kex}"."{table.table}";"""
            )
        return {"rows": result}

    def describe(self, kex: Kex):
        """Describe kex."""
        # probably not possible in MSSQL without having own meta table
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

    def _get_table_rows_count(self, table: Table):
        """Get table rows count

        Arguments:
            table {Table}

        Returns:
            int
        """

        with self._connector:
            result = self._connector.execute(
                f"""SELECT COUNT(1) as "rowcount" FROM "{table.kex.kex}"."{table.table}";"""
            )
        return result[0]["rowcount"]

    def get_table_details(self, table: Table):
        """Get table details ~ selected (available) azure table attributes

        Arguments:
            table {Table}

        Returns:
            table.details {TableDetails}
        """

        with self._connector:
            result = self._connector.execute(
                f"""SELECT create_date, modify_date FROM sys.tables t JOIN sys.schemas s ON t.schema_id=s.schema_id WHERE s.name='{table.kex.kex}' and t.name='{table.table}';"""
            )

        for line in result:
            created, modified = line["create_date"], line["modify_date"]
            table.details = TableDetails(
                created=created.strftime("%Y-%m-%d %H:%M:%S"),
                description=None,
                location=None,
                modified=modified.strftime("%Y-%m-%d %H:%M:%S"),
                size=None,
                size_readable=None,
                num_rows=self._get_table_rows_count(table),
                path=None,
                schema=[
                    TableSchema(name, column_type, None) for name, column_type in self.get_table_columns(table).items()
                ],
            )
        return table.details or TableDetails()

    def get_lines_from_table(self, table: Table) -> Iterable[Dict[str, Any]]:
        with self._connector:
            yield from self._connector.execute(
                f'''SELECT * FROM "{table.kex.kex}"."{table.table}"''', generator=True, chunk_size=1000
            )

    def list_kexes(self):
        kexes = []
        with self._connector:
            result = self._connector.execute("""SELECT SCHEMA_NAME FROM "INFORMATION_SCHEMA"."SCHEMATA";""")
        for item in result:
            kexes.append(Kex(item["SCHEMA_NAME"]))
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
            unions += f"""{union_type} SELECT {fields} FROM "{table.kex.kex}"."{table.table}" """
        with self._connector:
            self._connector.execute(
                f"""SELECT {fields} INTO  "{destination.kex.kex}"."{destination.table}" FROM "{first_table.kex.kex}"."{first_table.table}" {unions};"""
            )
        logger.info(f"Union tables {tables} to {destination}")

    def _whitelist_table(self, table: Table, destination: Table, columns: List[str]):
        fields = ", ".join(columns)
        with self._connector:
            self._connector.execute(
                f"""SELECT {fields} INTO  "{destination.kex.kex}"."{destination.table}" FROM "{table.kex.kex}"."{table.table}";"""
            )
        logger.info(f"Whitelist {len(columns)}: {columns} from {table} to {destination}")

    def _filter_table(self, table: Table, destination: Table, filter_query: str):
        with self._connector:
            self._connector.execute(
                f"""SELECT * INTO  "{destination.kex.kex}"."{destination.table}" FROM "{table.kex.kex}"."{table.table}" WHERE {filter_query};"""
            )
        logger.info(f"Filter by {filter_query} from {table} to {destination}")

    def _escaped_full_table_name(self, table: Table):
        return f'"{self.database}"."{table.kex.kex}"."{table.table}"'

    def _incremental_load(self, table: Table, destination: Table, primary_keys: List[str], mark_deletes: bool):

        all_columns_names = [
            column for column in self.get_table_columns(table).keys() if column not in self.RESERVED_COLUMNS
        ]

        all_columns_not_equal_condition = " OR ".join(
            (f"""EXISTS(SELECT S."{column}" EXCEPT SELECT D."{column}")""" for column in all_columns_names)
        )

        columns_assign = ", ".join((f'''"{column}" = S."{column}"''' for column in all_columns_names))

        match_statement = f"""WHEN MATCHED AND ({all_columns_not_equal_condition}) THEN UPDATE SET  {columns_assign}, "{self.TIMESTAMP_COLUMN}"={self.get_current_timestamp_value()}, "{self.LAST_OPERATION_COLUMN}"= '{self.LAST_OPERATION_UPDATE}' """

        destination_all_columns = ", ".join(
            (f'''"{column}"''' for column in [*all_columns_names, *self.RESERVED_COLUMNS])
        )
        source_all_columns = ", ".join((f'S."{column}"' for column in all_columns_names))
        not_match_statement = f"""WHEN NOT MATCHED THEN INSERT ({destination_all_columns}) VALUES ({source_all_columns}, {self.get_current_timestamp_value()}, '{self.LAST_OPERATION_INSERT}')"""

        primary_keys_equal_condition = " AND ".join((f'S."{column}" = D."{column}"' for column in primary_keys))

        if mark_deletes:
            not_match_statement_by_source = f"""WHEN NOT MATCHED BY SOURCE AND D."{self.LAST_OPERATION_COLUMN}" != '{self.LAST_OPERATION_DELETE}' THEN UPDATE SET "{self.TIMESTAMP_COLUMN}"={self.get_current_timestamp_value()}, "{self.LAST_OPERATION_COLUMN}"= '{self.LAST_OPERATION_DELETE}' """
        else:
            not_match_statement_by_source = ""

        query = f"""MERGE INTO {self._escaped_full_table_name(destination)} D USING {self._escaped_full_table_name(table)} S ON {primary_keys_equal_condition} {match_statement} {not_match_statement} {not_match_statement_by_source};"""

        with self._connector:
            self._connector.execute(query)

    def _get_shared_project_credentials_name(self, project_name):
        return f"shared_{project_name}_credentials"

    def _get_shared_project_data_source_name(self, project_name):
        return f"shared_{project_name}_data_source"

    def _connect_shared_data_sources(self):
        for key, item in self.sharing.sources.items():
            self._update_create_data_source(item)
        # TODO: solve deleting deleting datasource when not needed anymore

    def _update_create_data_source(self, project: AzureSQLSharedSourceConfig):
        credentials_name = self._get_shared_project_credentials_name(project.project_name)
        data_source_name = self._get_shared_project_data_source_name(project.project_name)
        with self._connector:
            try:
                self._connector.execute(
                    f"""ALTER DATABASE SCOPED CREDENTIAL "{credentials_name}" WITH IDENTITY = '{project.username}', SECRET='{project.password}';"""
                )
            except pyodbc.ProgrammingError:
                logger.info(f"Credentials {credentials_name} probably does not exists, creating it")
                self._connector.execute(
                    f"""CREATE DATABASE SCOPED CREDENTIAL "{credentials_name}" WITH IDENTITY = '{project.username}', SECRET='{project.password}';"""
                )
            try:
                self._connector.execute(
                    f"""ALTER EXTERNAL DATA SOURCE "{data_source_name}" SET LOCATION='{project.hostname}', DATABASE_NAME='{project.database}', CREDENTIAL="{credentials_name}";"""
                )
            except pyodbc.ProgrammingError:
                logger.info(f"Data source {data_source_name} probably does not exists, creating it")
                self._connector.execute(
                    f"""CREATE EXTERNAL DATA SOURCE "{data_source_name}" WITH (TYPE = RDBMS, LOCATION='{project.hostname}', DATABASE_NAME='{project.database}', CREDENTIAL="{credentials_name}");"""
                )

    def link_shared_table(self, table: Table, destination: Table):
        logger.info(f"Linking shared table {table} to {destination}")
        shared_project = self.sharing.sources[table.project]
        shared_storage_manager = AzureSQLStorageManager(
            host=shared_project.hostname,
            database=shared_project.database,
            username=shared_project.username,
            password=shared_project.password,
        )

        columns = shared_storage_manager.get_table_columns(table)
        if not columns:
            raise KeyError(f"Table {table} does not exist in shared project {shared_project.project_name}")
        logger.info(f"Found columns {columns} in shared table {table}")
        data_source_name = self._get_shared_project_data_source_name(table.project)
        columns_as_string = ",".join(['"{}" {}'.format(k, v) for k, v in columns.items()])
        with self._connector:
            self._connector.execute(
                f"""CREATE EXTERNAL TABLE "{destination.kex.kex}"."{destination.table}" ({columns_as_string}) WITH (DATA_SOURCE = {data_source_name}, SCHEMA_NAME='{table.kex.kex}', OBJECT_NAME='{table.table}');"""
            )

    def unlink_shared_table(self, table: Table):
        with self._connector:
            self._connector.execute(f"""DROP EXTERNAL TABLE "{table.kex.kex}"."{table.table}";""")

    def shared_out_table_destinations(self, table: Table):
        """Check if table should be shared"""
        return self.sharing.destinations.get(table.get_full_id(), [])

    def list_shared_out_tables(self):
        """List all tables to be shared"""
        return [Table.table_from_str(table_id) for table_id in self.sharing.destinations.keys()]
