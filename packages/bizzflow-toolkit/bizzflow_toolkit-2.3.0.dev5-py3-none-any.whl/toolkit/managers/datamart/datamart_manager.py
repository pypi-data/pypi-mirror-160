"""Datamart Manager

Module for managing all datamart managers on different platforms.
"""
import logging
from typing import List, Optional

from toolkit.base.kex import Kex
from toolkit.base.table import Table
from toolkit.managers.credentials.base import BaseCredentialsManager
from toolkit.managers.storage.base import BaseStorageManager

logger = logging.getLogger(__name__)


class DatamartManager:
    """Class for all datamart managers on different platforms,."""

    def __init__(
        self,
        storage_manager: BaseStorageManager,
        credentials_manager: BaseCredentialsManager,
        out_kex: str,
        dm_kex: str,
        allowed_tables: Optional[List] = None,
    ):
        self.storage_manager = storage_manager
        self.credentials_manager = credentials_manager
        self.out_kex = Kex.kex_from_str(out_kex)
        self.dm_kex = Kex.kex_from_str(dm_kex)
        self.allowed_tables = allowed_tables or []

    def create_environment(self):
        """Provision datamart kex"""
        logger.info("Creating datamart kex '%s'", self.dm_kex.get_id())
        self.storage_manager.create_kex(self.dm_kex)

    def get_credentials(self):
        """Get credentials."""
        # create datamart user
        if self.credentials_manager.user_exists(self.dm_kex.kex):
            logger.info("User for kex '%s' already exists", self.dm_kex.kex)
        else:
            logger.info("Creating user for kex '%s'", self.dm_kex.kex)
            self.credentials_manager.create_kex_user(self.dm_kex, self.dm_kex.kex)
            self.credentials_manager.grant_kex_permission_to_user(self.dm_kex, self.dm_kex.kex, read_only=True)

    def write(self):
        """Run datamart writer."""
        # copy tables from out to dm
        logger.info("Writing output tables to datamart %s", self.dm_kex.get_id())
        out_tables = self.storage_manager.list_tables(self.out_kex)
        for table in out_tables:
            if (
                (not self.allowed_tables)
                or (table.table in self.allowed_tables)
                or (table.get_full_id() in self.allowed_tables)
            ):
                table_dm = Table(table.table, self.dm_kex)
                self.storage_manager.copy_table(table, table_dm)
            else:
                logger.info("Skipping '%s' => not allowed", table.get_full_id())
