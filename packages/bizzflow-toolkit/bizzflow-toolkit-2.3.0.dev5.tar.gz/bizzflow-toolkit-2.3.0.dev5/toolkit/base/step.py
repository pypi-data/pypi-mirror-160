"""Step
Module for set of primitive and configurable operations with data.
"""
import uuid
from logging import getLogger
from typing import TYPE_CHECKING, Dict, List, Optional

from toolkit.base.kex import Kex
from toolkit.base.table import Table
from toolkit.managers.credentials.base import BaseCredentialsManager

if TYPE_CHECKING:
    from toolkit.managers.storage.base import BaseStorageManager

logger = getLogger(__name__)


class UnionConf:
    def __init__(self, tables: List[Table], distinct):
        self.tables = tables
        self.distinct = distinct


class WhitelistConf:
    def __init__(self, columns: List[str]):
        self.columns = columns


class FilterColumn:
    def __init__(self, name: str, data_type: str, operator: str, value: str):
        self.name = name
        self.data_type = data_type.lower()
        self.operator = operator
        self.value = value

    def get_filter_query(self, quotation_mark):
        if self.data_type == "date":
            column = f"CAST({quotation_mark}{self.name}{quotation_mark} AS STRING)"
        else:
            column = f"{quotation_mark}{self.name}{quotation_mark}"
        return f"{column} {self.operator} '{self.value}'"


class FilterConf:
    def __init__(self, custom_query, columns: List[FilterColumn]):
        self.custom_query = custom_query
        self.columns = columns

    def get_filter_query(self, quotation_mark):
        if self.custom_query:
            return self.custom_query
        else:
            return " AND ".join((column.get_filter_query(quotation_mark) for column in self.columns))


class CopyConf:
    def __init__(
        self,
        destination: Optional[Table] = None,
        incremental: Optional[bool] = False,
        primary_keys: Optional[List[str]] = None,
        mark_deletes: Optional[bool] = False,
    ):
        self.destination = destination
        self.incremental = incremental
        self.primary_keys = primary_keys or []
        self.mark_deletes = mark_deletes


class Step:
    """Class for Step.
    Parent class for various Step implementations, e.g. BQStep.

    Raises:
        NotImplementedError: If any of methods is not imlemented in the child class.
    """

    def __init__(
        self,
        storage_manager: "BaseStorageManager",
        credentials_manager: "BaseCredentialsManager",
        unions: Dict[str, UnionConf],
        whitelists: Dict[str, WhitelistConf],
        filters: Dict[str, FilterConf],
        copies: Dict[str, CopyConf],
    ):
        self.storage_manager = storage_manager
        self.credentials_manager = credentials_manager
        self.kex = Kex(f"tmp_{uuid.uuid4().hex}")
        self.unions = unions
        self.whitelists = whitelists
        self.filters = filters
        self.copies = copies

    @staticmethod
    def get_table_id(table):
        project_name = table.project
        kex_name = table.kex.kex
        table_name = table.table
        if kex_name.startswith("tr_"):
            kex_name = "tr"
        return f"{project_name}.{kex_name}.{table_name}"

    def create_tmp_table(self):
        table = Table(uuid.uuid4().hex, self.kex)
        return table

    def union_table(self, table: Table, origin_table_id: str) -> Table:
        """Union multiple source tables to one destination table."""
        try:
            union = self.unions[origin_table_id]
        except KeyError:
            return table
        logger.info("Creating union for table %s", origin_table_id)
        destination = self.create_tmp_table()
        self.storage_manager.union_table(union.tables, destination, union.distinct)
        return destination

    def whitelist_columns(self, table: Table, origin_table_id: str):
        """Copy only specified columns from source table to destination table."""
        try:
            whitelist = self.whitelists[origin_table_id]
        except KeyError:
            return table
        logger.info("Whitelisting table %s", origin_table_id)
        destination = self.create_tmp_table()
        self.storage_manager.whitelist_table(table, destination, whitelist.columns)
        return destination

    def filter_rows(self, table: Table, origin_table_id: str):
        """Copy only specified rows from source table to destination table."""
        try:
            filter_conf = self.filters[origin_table_id]
        except KeyError:
            return table
        logger.info("Filtering table %s", origin_table_id)
        destination = self.create_tmp_table()
        self.storage_manager.filter_table(
            table, destination, filter_conf.get_filter_query(quotation_mark=self.storage_manager.QUOTATION_MARK)
        )
        return destination

    def copy_table(self, table: Table, default_destination: Table, origin_table_id: str):
        """Copy source table to destination table incrementally."""
        try:
            copy = self.copies[origin_table_id]
        except KeyError:
            copy = CopyConf()

        destination = copy.destination or default_destination
        self.storage_manager.create_kex(destination.kex)

        logger.info(
            f"Table {origin_table_id} will be copied with step configuration (incremental: {copy.incremental}, primary_keys: {copy.primary_keys}, mark_deletes: {copy.mark_deletes}"
        )

        if copy.incremental:
            self.storage_manager.incremental_copy_table(table, destination, copy.primary_keys, copy.mark_deletes)
        else:
            self.storage_manager.copy_table(table, destination)
        return destination

    def process(self, table: Table, default_destination: Table):
        """Execute steps in logical order."""
        origin_table_id = self.get_table_id(table)
        if self.should_be_skipped(origin_table_id):
            logger.info(f"Skipping table {origin_table_id} processing.")
            return
        try:
            self.storage_manager.create_kex(self.kex)
            united_table = self.union_table(table, origin_table_id)
            whitelisted_table = self.whitelist_columns(united_table, origin_table_id)
            filtered_table = self.filter_rows(whitelisted_table, origin_table_id)
            destination = self.copy_table(filtered_table, default_destination, origin_table_id)
            logger.info(f"Processed table {table.get_full_id()} => {destination.get_full_id()}.")
            for destination_project in self.storage_manager.shared_out_table_destinations(destination):
                logger.info(f"Sharing table {destination.table} to project {destination_project}")
                user_name = f"sh_{destination_project}"
                self.credentials_manager.create_sharing_user(user_name)
                self.credentials_manager.share_table_to_user(user_name, destination)
        finally:
            self.storage_manager.delete_kex(self.kex)
        return destination

    def should_be_skipped(self, origin_table_id):
        try:
            self.copies[origin_table_id]
        except KeyError:
            for key, union in self.unions.items():
                for table in union.tables:
                    if table.get_full_id() == origin_table_id:
                        # table is processed as part of the union, and have no explicit copy definition
                        # so let's consider it as processed and skip it
                        return True
        return False
