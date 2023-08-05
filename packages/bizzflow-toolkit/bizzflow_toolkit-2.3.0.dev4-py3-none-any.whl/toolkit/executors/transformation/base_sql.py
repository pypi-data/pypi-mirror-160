"""Class for SQL transformation execution.
Parent class for various SQL transformation executor classes, e.g. BqSqlTransformationExecutor.
"""
import logging
import uuid
from typing import Optional

from toolkit.base import Step
from toolkit.executors.base.sql import SQLExecutor, SQLInputOutputMixin
from toolkit.managers.component.sql import SQLTransformationComponentManager
from toolkit.managers.credentials.base import BaseCredentialsManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.utils.stopwatch import stopwatch

logger = logging.getLogger(__name__)


class SqlTransformationExecutor(SQLInputOutputMixin, SQLExecutor):
    def __init__(
        self,
        storage_manager: BaseStorageManager,
        component_manager: SQLTransformationComponentManager,
        step: Step,
        credentials_manager: BaseCredentialsManager,
        inputs: list,
        output: str,
    ):

        super().__init__(storage_manager, component_manager, step, credentials_manager)
        self.transformation_user = self.working_kex.kex
        self.connector = None
        self.output = output
        self._inputs = inputs

    def _create_working_kex_name(self):
        return f"tr_{uuid.uuid4().hex}"

    def _create_output_kex_name(self):
        return self.output

    @stopwatch("Create environment", __qualname__)
    def create_environment(self):
        """Create environment for transformation run.
        Update transformation account with permissions to temporary schema.
        Store transformation service account credentials in vault manager (if not stored already).
        """
        logger.info("Environment is being created")
        super().create_environment()
        if self.credentials_manager.user_exists(self.transformation_user):
            logger.info(f"Transformation user {self.transformation_user} already exists, using it")
        else:
            self.credentials_manager.create_kex_user(self.working_kex, self.transformation_user)
        self.credentials_manager.grant_kex_permission_to_user(self.working_kex, self.transformation_user)

    @stopwatch("Clean environment", __qualname__)
    def clean_environment(self):
        logger.info("Cleaning environment")
        super().clean_environment()
        logger.info("Deleting temporary transformation user %s", self.transformation_user)
        self.credentials_manager.delete_user(self.transformation_user)
        logger.info("Environment cleaned")

    def run(self, skip_files: Optional[list] = None, **kwargs):
        """Run transformation.
        Switch to transformation user for current transformation with default schema.

        Raises:
            ValueError: If a query fails.
        """

        raise NotImplementedError
