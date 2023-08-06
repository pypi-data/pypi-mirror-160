"""Storage Manager

Module for managing all storage managers on different platforms.
"""
import os
import uuid
from logging import getLogger
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from toolkit.base import Kex, ObjectMetadata, Table
from toolkit.managers.file_storage import (
    ABSFileStorageManager,
    GcsFileStorageManager,
    LocalFileStorageManager,
    S3FileStorageManager,
)
from toolkit.managers.file_storage.base import BaseFileStorageManager

logger = getLogger(__name__)


class BaseStorageManager:
    """Abstract class for all storage managers on different platforms, e.g. BqStorageManager.

    Raises:
        NotImplementedError: If any of methods is not imlemented in the child class.
    """

    TIMESTAMP_COLUMN = "__timestamp"
    LAST_OPERATION_COLUMN = "__last_operation"
    LAST_OPERATION_COLUMN_TYPE = NotImplemented
    TIMESTAMP_COLUMN_COLUMN_TYPE = NotImplemented
    RESERVED_COLUMNS = (TIMESTAMP_COLUMN, LAST_OPERATION_COLUMN)
    LAST_OPERATION_INSERT = "I"
    LAST_OPERATION_UPDATE = "U"
    LAST_OPERATION_DELETE = "D"
    DEFAULT_COLUMN_TYPE = NotImplemented
    QUOTATION_MARK = NotImplemented
    TRANSLATION_INPUT = "áéěíýóúůžščřďťň .-():"
    TRANSLATION_OUTPUT = "aeeiyouuzscrdtn______"

    def get_current_timestamp_value(self):
        raise NotImplementedError

    @classmethod
    def normalize_string(cls, input_string, keep_case=False):
        """Removes diacritcs and then replaces bad characters by '_'.

        Arguments:
            s {str} -- string to be normalized
            keep_case {bool, optional} -- keep input string case, Default: False

        Returns:
            norm_s {str} -- normalized string
        """
        if not keep_case:
            input_string = input_string.lower()
        translation = str.maketrans(cls.TRANSLATION_INPUT, cls.TRANSLATION_OUTPUT)
        clear_s = input_string.translate(translation)
        return clear_s

    @property
    def project(self) -> str:
        """Return kex project name"""
        raise NotImplementedError("This method must be overridden")

    def list_kexes(self):
        """List all kexes for project.

        Returns:
            kexes {list} -- List of Kex objects
        """
        raise NotImplementedError("This method must be overriden")

    def create_kex(self, kex: Kex):
        """Create specified kex

        Arguments:
            kex {Kex}
        """
        raise NotImplementedError("This method must be overriden")

    def delete_kex(self, kex: Kex):
        """Delete specified kex

        Arguments:
            kex {Kex}
        """
        raise NotImplementedError("This method must be overriden")

    def describe(self, kex: Kex):
        """Describe kex."""
        raise NotImplementedError("This method must be overriden")

    def set_kex_metadata(self, kex: Kex, metadata: ObjectMetadata):
        """Update kex metadata"""
        raise NotImplementedError("This method must be overriden")

    def get_kex_metadata(self, kex: Kex) -> Optional[ObjectMetadata]:
        """Get kex metadata if they were previously stored"""
        raise NotImplementedError("This method must be overriden")

    def list_tables(self, kex: Kex) -> List[Table]:
        """List all tables in specified {kex}."""
        raise NotImplementedError("This method must be overriden")

    def create_table(self, table: Table, fields: List[Union[str, Tuple[str, str]]]):
        """Crate table with specified name and structure

        Arguments:
            fields {list} --  List of columns definitions consisting of a name
            and optional data type (e. g. ("name", "varchar(255)") or "name"
            table {Table}
        """
        raise NotImplementedError("This method must be overridden")

    def delete_table(self, table: Table):
        raise NotImplementedError("This method must be overridden")

    def truncate_table(self, table: Table):
        """Truncate {table}."""
        raise NotImplementedError("This method must be overriden")

    def list_input_tables(self, inputs: list):
        """Return set of input tables based on both input kexes and input tables specification

        Keyword Arguments:
            input {list} -- List of input kex/tables objects or their names
        """

        in_kexes = []
        in_tables = []
        for input_name in inputs:
            if "." in input_name:
                in_tables.append(input_name)
            else:
                in_kexes.append(input_name)
        kexes = [kex if isinstance(kex, Kex) else Kex.kex_from_str(kex) for kex in in_kexes]
        tables = [table if isinstance(table, Table) else Table.table_from_str(table) for table in in_tables]
        kex_tables = (table for kex in kexes for table in self.list_tables(kex))
        return list({*tables, *kex_tables})

    def load_table(self, table: Table, path: str, file_storage_manager: BaseFileStorageManager):
        """Load {table} from specified {path}."""
        logger.info("Loading %s to %s", file_storage_manager.get_absolute_path(path), table.get_full_id())

        logger.info("Getting fields for table %s", table)
        fields = file_storage_manager.get_fields_names_from_csv(path)
        if not fields:
            logger.warning("Truncating table %s - source csv is empty", table.table)
            try:
                self.truncate_table(table)
            except Exception as error:
                logger.error("Could not truncate table %s - %s", table.table, str(error))
            logger.warning("Skipping loading of %s - source csv is empty", path)
        else:
            self.delete_table(table)
            self.create_table(table, fields)
            logger.info(f"Loading data from {file_storage_manager.get_absolute_path(path)} into table: {table}")

            if isinstance(file_storage_manager, GcsFileStorageManager):
                self.load_table_from_gcs_storage(table, path, file_storage_manager)
            elif isinstance(file_storage_manager, S3FileStorageManager):
                self.load_table_from_s3_storage(table, path, file_storage_manager)
            elif isinstance(file_storage_manager, ABSFileStorageManager):
                self.load_table_from_azure_blob_storage(table, path, file_storage_manager)
            elif isinstance(file_storage_manager, LocalFileStorageManager):
                self.load_table_from_local_storage(table, path, file_storage_manager)
            else:
                raise NotImplementedError("Unknown file storage manager")
            self.append_timestamp(table)

    def load_table_from_gcs_storage(self, table: Table, path: str, file_storage_manager: GcsFileStorageManager):
        raise NotImplementedError(f"{self.__class__.__name__} does not support loading from Google Cloud Storage")

    def load_table_from_s3_storage(self, table: Table, path: str, file_storage_manager: S3FileStorageManager):
        raise NotImplementedError(f"{self.__class__.__name__} does not support loading from S3 Storage")

    def load_table_from_azure_blob_storage(self, table: Table, path: str, file_storage_manager: ABSFileStorageManager):
        raise NotImplementedError(f"{self.__class__.__name__} does not support loading from Azure BLOB Storage")

    def load_table_from_local_storage(self, table: Table, path: str, file_storage_manager: LocalFileStorageManager):
        raise NotImplementedError(f"{self.__class__.__name__} does not support loading from Local Storage")

    def table_exists(self, table: Table):
        """test if table with given name already exists"""
        return table.get_full_id() in (t.get_full_id() for t in self.list_tables(table.kex))

    def copy_table(self, table: Table, destination_table: Table, exists_ok: bool = True):
        """Copy table."""
        with both_normal_or_shared_table(self, table) as source:
            self._copy_table(source, destination_table, exists_ok)

    def _copy_table(self, source_table: Table, destination_table: Table, exists_ok: bool = True):
        """Copy table."""
        raise NotImplementedError("This method must be overriden")

    def get_table_columns(self, table: Table) -> dict:
        raise NotImplementedError("This method must be overridden")

    def preview(self, table: Table, number_results: int):
        """Preview random specified number of rows from specified table."""
        with both_normal_or_shared_table(self, table) as source:
            return self._preview(source, number_results)

    def _preview(self, table: Table, number_results: int):
        raise NotImplementedError("This method must be overridden")

    def get_table_details(self, table: Table):
        """Describe table details and store it as attribute detail of table."""
        raise NotImplementedError("This method must be overridden")

    def set_table_metadata(self, table: Table, metadata: ObjectMetadata):
        """Update table metadata"""
        raise NotImplementedError("This method must be overriden")

    def get_table_metadata(self, table: Table) -> Optional[ObjectMetadata]:
        """Get table metadata if they were previously stored"""
        raise NotImplementedError("This method must be overriden")

    def export_to_file_storage(self, table: Table, path: str, file_storage_manager: BaseFileStorageManager):
        """Export table to file storage as single file (table.csv)
        or as multiple files compressed by gzip (table.csv*.gz), if table is too big."""
        data = self.get_lines_from_table(table)
        file_storage_manager.write_to_csv_file(path, data)

    def get_lines_from_table(self, table: Table) -> Iterable[Dict[str, Any]]:
        """Return iterator iterating all rows from table as dict"""
        raise NotImplementedError("This method must be overridden")

    def export_to_worker(self, table, target_path, worker_manager, file_storage_manager):
        """Export table to .csv. and store it on worker"""
        tmp_dir = file_storage_manager.get_tmp_dir().rstrip("/")
        file_name = f"{table.table}.csv"
        # Remove prefix in from input table - it's already in the input folder on worker
        if file_name.startswith("in_"):
            file_name = file_name[3:]
        self.export_to_file_storage(table, os.path.join(tmp_dir, file_name), file_storage_manager)
        logger.info(
            "Using %s to export input to worker (%s => %s)", worker_manager.__class__.__name__, tmp_dir, target_path
        )
        file_storage_manager.download_file_to_worker(worker_manager, f"{tmp_dir}/*", target_path)
        file_storage_manager.clean_folder(tmp_dir)
        final_csv_name = os.path.join(target_path, file_name)
        partition_wildcard = os.path.join(target_path, f"{file_name}*.gz")
        # create output file from the first partition (test if output file already exists)
        # for other (if exists) skip header and merge
        worker_manager.run(
            f"""
            for f in {partition_wildcard}; do
                if ! [[ -e "$f" ]]; then 
                    echo "No files for decompress and merge";
                    break
                fi
                if [ -s {final_csv_name} ]; then
                    echo "Merging file $f into {final_csv_name}";
                    gzip -cd $f | tail -n +2 >> {final_csv_name};
                else
                    echo "Creating output file {final_csv_name} from $f";
                    gzip -cd $f > {final_csv_name};
                fi
                rm $f;
            done
            """
        )

    def append_columns(self, table: Table, columns: List[Tuple[str, str, Optional[str]]]):
        """
        Append columns to table
        Args:
            table: Table for
            columns: List of tuples (column_name, column_type, value)
        Returns:

        """
        raise NotImplementedError("This method must be overridden")

    def check_tables_columns_compatibility(self, source_table: Table, destination_table: Table):
        source_table_columns = self.get_table_columns(source_table)
        destination_table_columns = self.get_table_columns(destination_table)

        extra_columns = source_table_columns.keys() - destination_table_columns.keys()
        if extra_columns:
            logger.info(
                f"Extra columns in {source_table.get_id()} in comparison of destination table {destination_table.get_full_id()}, Extra columns: {extra_columns}"
            )

        missing_columns = destination_table_columns.keys() - source_table_columns.keys() - set(self.RESERVED_COLUMNS)
        if missing_columns:
            if len(missing_columns) == 1 and "last_operation" in missing_columns:
                # TODO: This is only so that after upgrade to 2.0.0 all projects fix themself
                logger.warning("Dropping obsolete 'last_operation' column from table %s", destination_table)
                self.drop_column(destination_table, "last_operation")
            else:
                logger.error(
                    (
                        f"Missing columns in {source_table.get_id()}, Expected: {destination_table_columns}, "
                        f"Got: {source_table_columns}, Missing: {missing_columns}"
                    )
                )
                raise KeyError(
                    (
                        f"Missing columns in {source_table.get_id()}, Expected: {destination_table_columns}, "
                        f"Got: {source_table_columns}, Missing: {missing_columns}"
                    )
                )

        same_columns = source_table_columns.keys() & destination_table_columns.keys()
        type_mismatch = False
        for name in same_columns:
            s_type = source_table_columns[name]
            d_type = destination_table_columns[name]
            if s_type != d_type:
                logger.error(
                    f"Mismatch in type for column {name} in {source_table.get_id()}, Expected: {d_type}, Got: {s_type}"
                )
                type_mismatch = True
        if type_mismatch:
            raise ValueError("There is a mismatch in column type")
        return {name: source_table_columns[name] for name in extra_columns}

    def merge_tables_columns(self, table, destination):
        extra_columns = self.check_tables_columns_compatibility(table, destination)
        columns_to_add = []
        for column, column_type in extra_columns.items():
            columns_to_add.append((column, column_type, None))
        if columns_to_add:
            self.append_columns(destination, columns_to_add)

    def incremental_copy_table(self, table, destination, primary_keys, mark_deletes):
        assert primary_keys, "At least on primary key is required"
        if not self.table_exists(destination):
            logger.info(f"Table {destination} does not exists, creating it")
            self.create_table(destination, list(self.get_table_columns(table).items()))
        self.append_incremental_columns(destination)
        self.merge_tables_columns(table, destination)
        logger.info(f"Incremental load of {table} to {destination}")
        self.incremental_load(table, destination, primary_keys, mark_deletes)

    def append_timestamp(self, table):
        self.append_columns(
            table, [(self.TIMESTAMP_COLUMN, self.TIMESTAMP_COLUMN_COLUMN_TYPE, self.get_current_timestamp_value())]
        )

    def append_incremental_columns(self, table):
        self.append_columns(
            table,
            [
                (self.TIMESTAMP_COLUMN, self.TIMESTAMP_COLUMN_COLUMN_TYPE, self.get_current_timestamp_value()),
                (self.LAST_OPERATION_COLUMN, self.LAST_OPERATION_COLUMN_TYPE, f"'{self.LAST_OPERATION_INSERT}'"),
            ],
        )

    def incremental_load(self, table, destination, primary_keys, mark_deletes):
        with both_normal_or_shared_table(self, table) as source:
            self._incremental_load(source, destination, primary_keys, mark_deletes)

    def _incremental_load(self, table, destination, primary_keys, mark_deletes):
        raise NotImplementedError("This method must be overridden")

    def filter_table(self, table, destination, filter_query: str):
        """Copy only specified rows from source table to destination table.

        Arguments:
            source {Table} -- Source table object
            destination {Table} -- Destination table object
            filter_query {str} -- filter to apply
        """
        with both_normal_or_shared_table(self, table) as source:
            self._filter_table(source, destination, filter_query)

    def _filter_table(self, table, destination, filter_query: str):
        raise NotImplementedError("This method must be overridden")

    def whitelist_table(self, table: Table, destination: Table, columns):
        with both_normal_or_shared_table(self, table) as source:
            self._whitelist_table(source, destination, columns)

    def _whitelist_table(self, table, destination, columns):
        raise NotImplementedError("This method must be overridden")

    def union_table(self, tables, destination, distinct):
        with both_normal_or_shared_table(self, tables) as sources:
            return self._union_table(sources, destination, distinct)

    def _union_table(self, tables, destination, distinct):
        raise NotImplementedError("This method must be overridden")

    def drop_column(self, table: Table, column_name: str):
        """Drop column from table"""
        raise NotImplementedError(f"{self.__class__.__name__} does not implement drop_column")

    def link_shared_table(self, table: Table, destination: Table):
        """Link shared table to destination table"""
        raise NotImplementedError(f"{self.__class__.__name__} does not implement link_shared_table")

    def unlink_shared_table(self, table: Table):
        """Unlink shared table from destination table"""
        raise NotImplementedError(f"{self.__class__.__name__} does not implement unlink_shared_table")

    def list_shared_out_tables(self) -> List[Table]:
        """List all tables to be shared"""
        raise NotImplementedError(f"{self.__class__.__name__} does not implement list_shared_out_tables")

    def shared_out_table_destinations(self, table: Table) -> List[str]:
        """Check if table should be shared"""
        raise NotImplementedError(f"{self.__class__.__name__} does not implement shared_out_table_destinations")

    def is_shared_table(self, table: Table):
        """Check if table is shared"""
        return table.project != self.project


class both_normal_or_shared_table:
    def __init__(self, storage_manager: BaseStorageManager, tables: Union[Iterable[Table], Table]):
        self.storage_manager = storage_manager
        self.single_table = False
        if isinstance(tables, Table):
            self.tables = [tables]
            self.single_table = True
        else:
            self.tables = tables
        self.shared_tables = []
        self.project_tables = []
        for table in self.tables:
            if self.storage_manager.is_shared_table(table):
                # Create separate Kex for each table to prevent conflicts in table names
                kex = Kex(f"shared_{uuid.uuid4().hex}")
                self.storage_manager.create_kex(kex)
                shared_table = Table(table.table, kex)
                self.shared_tables.append(shared_table)
                self.storage_manager.link_shared_table(table, shared_table)
            else:
                self.project_tables.append(table)
        self.all_tables = self.shared_tables + self.project_tables

    def __enter__(self):
        if self.single_table:
            return self.all_tables[0]
        else:
            return self.all_tables

    def __exit__(self, exc_type, exc_val, exc_tb):
        for shared_table in self.shared_tables:
            self.storage_manager.unlink_shared_table(shared_table)
            self.storage_manager.delete_kex(shared_table.kex)
