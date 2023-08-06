"""BigQuery Storage Manager

Provides functions to manage storage based on Google BigQuery.
"""

from logging import getLogger
from typing import List, Optional, Tuple, Union

from toolkit.base import Kex, ObjectMetadata, Table, TableDetails
from toolkit.managers.file_storage.base import BaseFileStorageManager
from toolkit.managers.file_storage.gcs import GcsFileStorageManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.utils.helpers import humanize_size

logger = getLogger(__name__)

try:
    from google.cloud import bigquery, storage
except ImportError:
    logger.info("Google Cloud libraries are not installed.")


class BqStorageManager(BaseStorageManager):
    """Manage flow of data inside storage, BQ and between them."""

    LAST_OPERATION_COLUMN_TYPE = "STRING"
    TIMESTAMP_COLUMN_COLUMN_TYPE = "STRING"
    DEFAULT_COLUMN_TYPE = "STRING"
    QUOTATION_MARK = "`"

    def __init__(self, project_id, dataset_location):
        """Initiate BQ Storage Manager

        Arguments:
            bq_client {Client} -- Client to BigQuery

            gcs_client {Client} -- Client to Google Cloud Storage
        """
        self.bq_client = bigquery.Client()
        self.gcs_client = storage.Client()
        self.project_id = project_id
        self.location = dataset_location

    def get_current_timestamp_value(self):
        return "CAST(CURRENT_TIMESTAMP() AS STRING)"

    @property
    def project(self) -> str:
        """Return kex project name"""
        return self.project_id

    def list_tables(self, kex: Kex):
        """List all tables in specified kex

        Arguments:
            kex {Kex}

        Returns:
            tables {list} -- List of Table objects in specified kex
        """
        dataset_id = kex.get_id()
        tables = []
        tbls = self.bq_client.list_tables(dataset_id)
        for table in tbls:
            tables.append(Table(table.table_id, kex))
        return tables

    def get_table_details(self, table: Table):
        """Get table details ~ selected bq table attributes

        Arguments:
            table {Table}

        Returns:
            table.details {TableDetails}
        """
        bq_table = self.bq_client.get_table(table.get_id())
        table.details = TableDetails(
            created=bq_table.created.strftime("%Y-%m-%d %H:%M:%S"),
            description=bq_table.description,
            location=bq_table.location,
            modified=bq_table.modified.strftime("%Y-%m-%d %H:%M:%S"),
            size=bq_table.num_bytes,
            size_readable=humanize_size(bq_table.num_bytes),
            num_rows=bq_table.num_rows,
            path=bq_table.path,
            schema=bq_table.schema,
        )
        return table.details

    def create_table(self, table: Table, fields: List[Union[str, Tuple[str, str]]]):
        table_id = table.get_full_id()
        if self.table_exists(table):
            logger.warning("Table with following id '%s' already exists", table_id)
        else:
            schema = []
            for field in fields:
                if isinstance(field, str):
                    schema.append(
                        bigquery.schema.SchemaField(
                            name=self.normalize_string(field), field_type=self.DEFAULT_COLUMN_TYPE
                        )
                    )
                elif hasattr(field, "__getitem__") and len(field) == 2:
                    schema.append(
                        bigquery.schema.SchemaField(name=self.normalize_string(field[0]), field_type=field[1])
                    )
            tbl = bigquery.Table(table_id, schema=schema)
            self.bq_client.create_table(tbl)
            logger.info("Created table '%s'", table_id)

    def delete_table(self, table: Table):
        """Delete table with specified name in specified kex

        Arguments:
            table {Table}
        """
        table_id = table.get_full_id()
        self.bq_client.delete_table(table_id, not_found_ok=True)
        logger.info("Deleted table '%s'.", table_id)

    def truncate_table(self, table: Table):
        """Truncate table with specified name in specified kex

        Arguments:
            table {Table}

        Raises:
            Exception: In case of problems with query job
        """
        table_id = table.get_full_id()
        query = f""" 
                DELETE FROM {self._escaped_full_table_name(table)}
                WHERE true;
                """
        query_job = self.bq_client.query(query)
        query_job.result()
        logger.info("Table: %s is empty now", table_id)

    def append_columns(self, table: Table, columns: List[Tuple[str, str, Optional[str]]]):
        bq_table = self.bq_client.get_table(table.get_full_id())
        schema = bq_table.schema
        current_columns = [c.name for c in schema]
        needs_update = False
        value_updates = []
        for column_name, column_type, value in columns:
            if column_name in current_columns:
                logger.info(f"Column {column_name} is already in table {table}")
            else:
                needs_update = True
                logger.info(f"Append column {column_name} to table {table}")
                schema.append(bigquery.SchemaField(column_name, column_type))
                if value:
                    value_updates.append(f"`{column_name}` = {value}")
        if needs_update:
            bq_table.schema = schema
            self.bq_client.update_table(bq_table, ["schema"])
            if value_updates:
                value_updates_str = ", ".join(value_updates)
                query = f"UPDATE {self._escaped_full_table_name(table)} SET {value_updates_str} WHERE True"
                job = self.bq_client.query(query)
                job.result()
        else:
            logger.info("No columns to add")

    def drop_column(self, table: Table, column_name: str):
        """Drop column from table"""
        # Client.update_table cannot drop columns, DDL query must be used
        self.bq_client.query(
            f"ALTER TABLE `{self.project_id}`.`{table.kex.kex}`.`{table.table}` DROP COLUMN `{column_name}`"
        ).result()

    def get_table_columns(self, table: Table) -> dict:
        bq_table = self.bq_client.get_table(table.get_full_id())
        return {field.name: field.field_type for field in bq_table.schema}

    def load_table_from_gcs_storage(self, table: Table, path: str, file_storage_manager: GcsFileStorageManager):
        """Load table from GCS input bucket to BigQuery dataset

        Arguments:
            table {Table}

            path {str} -- path to table in uri format
        """
        path = file_storage_manager.get_absolute_path(path)
        try:
            load_job_config = bigquery.LoadJobConfig(allow_quoted_newlines=True)
            load_job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
            table_ref = self.bq_client.get_table(table.get_full_id())
            load_job_config.schema = table_ref.schema
            load_job_config.skip_leading_rows = 1
            load_job = self.bq_client.load_table_from_uri(
                path, table_ref, location=self.location, project=self.project_id, job_config=load_job_config
            )
            logger.info("Starting job %s, loading data into table: %s", load_job.job_id, table.table)
            load_job.result()
            logger.info("Load job result state: %s", load_job.result().state)
            logger.info("Loaded %s rows into %s.", table_ref.num_rows, table_ref.table_id)
        except Exception as e:
            logger.error("Failed to create table %s", table.get_full_id())
            logger.error(load_job.errors)
            logger.error(load_job.error_result)
            raise Exception(e)
        return True

    def _copy_table(self, source_table: Table, destination_table: Table, exists_ok: bool = True):
        """Copy table from one BQ dataset to another

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
        job_config = bigquery.CopyJobConfig()
        # rewrite table if already exists
        job_config.write_disposition = "WRITE_TRUNCATE"
        job = self.bq_client.copy_table(source_table_id, destination_table_id, job_config=job_config)
        job.result()
        logger.info("Copy table: '%s' to '%s'", source_table_id, destination_table_id)

    def _preview(self, table: Table, number_results: int):
        """Preview random specified number of rows from specified table

        Arguments:
            table {Table}

            number_results {int} --  Number of results to be returned

        Returns:
            Dictionary with specified number of rows from specified table
        """
        table_id = table.get_id()
        table_obj = self.bq_client.get_table(table_id)
        rows = self.bq_client.list_rows(table_obj, max_results=number_results)
        data = []
        for row in rows:
            current_row = {}
            for k, v in row.items():
                current_row[k] = v
            data.append(current_row)
        return {"rows": data}

    def describe(self, kex: Kex):
        """Describe specified kex

        Arguments:
            kex {Kex}

        Returns:
            dictionary with basic information about BQ dataset
        """
        dataset_id = kex.get_id()
        details = self.bq_client.get_dataset(dataset_id)
        tables = []
        for table in self.list_tables(kex):
            tables.append(table.get_full_id())
        return {
            "name": kex.kex,
            "full_name": details.full_dataset_id,
            "created": details.created.strftime("%Y-%m-%d %H:%M:%S"),
            "modified": details.modified.strftime("%Y-%m-%d %H:%M:%S"),
            "description": details.description,
            "location": details.location,
            "tables": tables,
        }

    def set_kex_metadata(self, kex: Kex, metadata: ObjectMetadata):
        """Set kex metadata as dataset's description text"""
        dataset = self.bq_client.get_dataset(kex.get_id())
        dataset.description = metadata.payload
        self.bq_client.update_dataset(dataset, ["description"])

    def get_kex_metadata(self, kex: Kex) -> Optional[ObjectMetadata]:
        """Get kex metadata from dataset's description text"""
        dataset = self.bq_client.get_dataset(kex.get_id())
        if dataset.description:
            try:
                metadata = ObjectMetadata.from_payload(dataset.description)
                return metadata
            except ValueError:
                logger.error("Failed to deserialize kex (%s) metadata", kex.kex, exc_info=True)
        return None

    def set_table_metadata(self, table: Table, metadata: ObjectMetadata):
        """Set table metadata as table's description text"""
        table_ref = self.bq_client.get_table(table.get_id())
        table_ref.description = metadata.payload
        self.bq_client.update_table(table_ref, ["description"])

    def get_table_metadata(self, table: Table) -> Optional[ObjectMetadata]:
        """Get table metadata from table's description text"""
        table_ref = self.bq_client.get_table(table.get_id())
        if table_ref.description:
            try:
                metadata = ObjectMetadata.from_payload(table_ref.description)
                return metadata
            except ValueError:
                logger.error("Failed to deserialize table (%s) metadata", table.get_id(), exc_info=True)
        return None

    def export_to_file_storage(self, table: Table, path: str, file_storage_manager: BaseFileStorageManager):
        if isinstance(file_storage_manager, GcsFileStorageManager):
            self.export_to_google_cloud_storage(table, path, file_storage_manager)
        else:
            super().export_to_file_storage(table, path, file_storage_manager)

    def export_to_google_cloud_storage(self, table: Table, path: str, file_storage_manager: GcsFileStorageManager):
        """Export specified table to .csv in Google cloud storage

        Arguments:
            table {Table}

            path {str} -- path to table in uri format
        """
        path = file_storage_manager.get_absolute_path(path)
        table_ref = self.bq_client.get_table(table.get_full_id())
        job_config = bigquery.ExtractJobConfig()
        job_config.field_delimiter = ","
        job_config.compression = bigquery.Compression.GZIP
        job_config.destination_format = bigquery.DestinationFormat.CSV
        path = path.replace(".csv", ".csv*.gz")
        logger.info("Exporting table %s to %s", table.get_full_id(), path)
        extract_job = self.bq_client.extract_table(table_ref, path, job_config=job_config, location=self.location)
        extract_job.result()
        logger.info("Table %s exported successfully.", table.get_full_id())

    def list_kexes(self):
        kexes = []
        kxs = list(self.bq_client.list_datasets(self.project_id))
        for kex in kxs:
            kexes.append(Kex(kex.dataset_id, kex.project))
        return kexes

    def create_kex(self, kex: Kex):
        kex_id = kex.get_id()
        if kex_id in [k.get_id() for k in self.list_kexes()]:
            logger.warning("Kex with following id '%s' already exists", kex_id)
        else:
            dataset = bigquery.Dataset(kex_id)
            dataset.location = self.location
            self.bq_client.create_dataset(dataset)
            logger.info("Created dataset '%s'", kex_id)

    def delete_kex(self, kex: Kex):
        dataset_id = kex.get_id()
        self.bq_client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
        logger.info("Deleted kex '%s'.", dataset_id)

    @staticmethod
    def _escaped_full_table_name(table: Table):
        return f"`{table.project}`.`{table.kex.kex}`.`{table.table}`"

    def _incremental_load(self, table, destination, primary_keys, mark_deletes):

        all_columns_names = [
            column for column in self.get_table_columns(table).keys() if column not in self.RESERVED_COLUMNS
        ]

        all_columns_not_equal_condition = " OR ".join(
            (f"IFNULL(S.`{column}` != D.`{column}`, TRUE)" for column in all_columns_names)
        )

        columns_assign = ", ".join((f"`{column}` = S.`{column}`" for column in all_columns_names))

        match_statement = f"WHEN MATCHED AND ({all_columns_not_equal_condition}) THEN UPDATE SET  {columns_assign}, `{self.TIMESTAMP_COLUMN}`={self.get_current_timestamp_value()}, `{self.LAST_OPERATION_COLUMN}`= '{self.LAST_OPERATION_UPDATE}' "

        destination_all_columns = ", ".join((f"`{column}`" for column in [*all_columns_names, *self.RESERVED_COLUMNS]))
        source_all_columns = ", ".join((f"S.`{column}`" for column in all_columns_names))
        not_match_statement = f"WHEN NOT MATCHED THEN INSERT ({destination_all_columns}) VALUES ({source_all_columns}, {self.get_current_timestamp_value()}, '{self.LAST_OPERATION_INSERT}')"

        primary_keys_equal_condition = " AND ".join((f"S.`{column}` = D.`{column}`" for column in primary_keys))

        if mark_deletes:
            not_match_statement_by_source = f"WHEN NOT MATCHED BY SOURCE AND D.`{self.LAST_OPERATION_COLUMN}` != '{self.LAST_OPERATION_DELETE}' THEN UPDATE SET `{self.TIMESTAMP_COLUMN}`={self.get_current_timestamp_value()}, `{self.LAST_OPERATION_COLUMN}`= '{self.LAST_OPERATION_DELETE}' "
        else:
            not_match_statement_by_source = ""

        query = f"MERGE INTO {self._escaped_full_table_name(destination)} D USING {self._escaped_full_table_name(table)} S ON {primary_keys_equal_condition} {match_statement} {not_match_statement} {not_match_statement_by_source};"
        job = self.bq_client.query(query)
        job.result()

    def _filter_table(self, table, destination, filter_query):
        source_full_id = table.get_full_id()
        destination_full_id = destination.get_full_id()
        source_table_info = self.bq_client.get_table(source_full_id)
        query = f"""
                CREATE OR REPLACE TABLE {self._escaped_full_table_name(destination)} AS
                    SELECT * FROM `{source_full_id}`
                WHERE {filter_query};
                """
        logger.debug(query)
        filter_result = self.bq_client.query(query)
        filter_result.result()
        filter_table_info = self.bq_client.get_table(destination_full_id)
        filtered_rows = source_table_info.num_rows - filter_table_info.num_rows
        logger.info(
            f"Filtered {filtered_rows} rows from {source_table_info.num_rows} rows from table by 'WHERE {filter_query}': '{source_full_id}' to '{destination_full_id}', {filter_table_info.num_rows} rows left"
        )

    def _whitelist_table(self, table, destination, columns):
        columns_string = ", ".join(columns)
        source_full_id = table.get_full_id()
        destination_full_id = destination.get_full_id()
        query = f"""
                CREATE OR REPLACE TABLE {self._escaped_full_table_name(destination)} AS 
                    SELECT {columns_string}
                FROM `{source_full_id}`;
                """
        logger.debug(query)
        whitelist_table = self.bq_client.query(query)
        whitelist_table.result()
        number_columns = len(columns)
        logger.info(
            "Whitelist %d columns: %s from table: '%s' to '%s'",
            number_columns,
            columns_string,
            source_full_id,
            destination_full_id,
        )

    def _union_table(self, tables, destination, distinct):
        log_message = f"Union tables {tables} to '{destination}'"
        union_type = "UNION" if distinct else "UNION ALL"
        first_table = tables[0]
        fields = ", ".join(self.get_table_columns(first_table).keys())
        unions = f"""SELECT {fields} FROM `{first_table.get_full_id()}`  """
        for table in tables[1:]:
            unions += f"""{union_type} SELECT {fields} FROM {self._escaped_full_table_name(table)} """
        query = f"""CREATE OR REPLACE TABLE  {self._escaped_full_table_name(destination)} AS {unions};"""

        logger.debug(query)
        union_table = self.bq_client.query(query)
        union_table.result()
        logger.info(log_message)

    def is_shared_table(self, table: Table):
        logger.warning(
            "Bigquery storage manager do not support shared tables."
            "It will work only if you set up manually service account to have access to proper dataset."
            "It will we deprecated, once there will full support for shared tables"
        )
        return False

    def link_shared_table(self, table: Table, destination: Table):
        logger.warning(
            "Bigquery storage manager do not support shared tables."
            "It will work only if you set up manually service account to have access to proper dataset."
            "It will we deprecated, once there will full support for shared tables"
        )
        return destination

    def unlink_shared_table(self, table: Table):
        logger.warning(
            "Bigquery storage manager do not support shared tables."
            "It will work only if you set up manually service account to have access to proper dataset."
            "It will we deprecated, once there will full support for shared tables"
        )
        return

    def list_shared_out_tables(self):
        # TODO: add table sharing logic once BQ manager supports sharing
        return []

    def shared_out_table_destinations(self, table: Table):
        # TODO: add table sharing logic once BQ manager supports sharing
        return []
