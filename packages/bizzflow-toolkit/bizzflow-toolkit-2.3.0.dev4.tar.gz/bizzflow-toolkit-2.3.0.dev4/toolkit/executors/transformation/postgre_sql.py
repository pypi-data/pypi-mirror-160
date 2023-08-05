"""Class for executing transformation in Azure SQL.
"""

import logging
from typing import Optional

from toolkit.executors.transformation.base_sql import SqlTransformationExecutor
from toolkit.managers.component.sql import SQLTransformationComponentManager
from toolkit.managers.credentials import PostgreSQLCredentialManager
from toolkit.managers.storage import PostgreSQLStorageManager
from toolkit.utils.postre_sql import PostgreSQLConnector
from toolkit.utils.stopwatch import stopwatch

logger = logging.getLogger(__name__)


class PostgreSQLTransformationExecutor(SqlTransformationExecutor):
    """Class for executing transformation in PostreSQL."""

    def __init__(
        self,
        storage_manager: PostgreSQLStorageManager,
        component_manager: SQLTransformationComponentManager,
        step,
        credentials_manager: PostgreSQLCredentialManager,
        inputs: list,
        output: str,
    ):
        super().__init__(storage_manager, component_manager, step, credentials_manager, inputs, output)

    @stopwatch("Run transformation", __qualname__)
    def run(self, skip_files: Optional[list] = None, **kwargs):
        """Run transformation.
        Switch to transformation user for current transformation with default schema.

        Raises:
            ValueError: If a query fails.
        """

        logger.info("Start run transformation")
        credentials = self.credentials_manager.get_user_credentials(self.transformation_user)
        connector = PostgreSQLConnector(
            host=credentials["host"],
            database=credentials["database"],
            username=credentials["user"],
            password=credentials["password"],
            timeout=self.component_manager.query_timeout,
            port=credentials["port"],
        )
        with connector:
            for query in self.component_manager.get_queries(skip_files):
                query = query.replace('"tr"', '"{}"'.format(self.working_kex.kex))
                logger.info(query)
                connector.execute(query)
        logger.info("Transformation finish")
