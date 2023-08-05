"""Class for executing transformation in Google BigQuery.
"""

import logging
from typing import Optional

from toolkit.executors.transformation.base_sql import SqlTransformationExecutor
from toolkit.utils.stopwatch import stopwatch

logger = logging.getLogger(__name__)

try:
    from snowflake.connector import SnowflakeConnection
except ImportError:
    logger.info("Snowflake libraries are not installed, install snowflake extras.")


class SnowflakeSqlTransformationExecutor(SqlTransformationExecutor):
    """Class for executing transformation in Snowflake."""

    @stopwatch("Create environment", __qualname__)
    def create_environment(self):
        super().create_environment()
        # Need to refresh permission to OPERATOR
        self.credentials_manager.grant_kex_permission_to_user(self.working_kex, "ORCHESTRATOR_ROLE")

    @stopwatch("Run transformation", __qualname__)
    def run(self, skip_files: Optional[list] = None, **kwargs):
        """Run transformation.
        Swith to transformation user for cuirrent transformation with default schema.

        Raises:
            ValueError: If a query fails.
        """

        # Switch credentials (reatrict client permissions for transformation run)
        logger.info("Switching to transformation user: %s", self.transformation_user)
        credentials = self.credentials_manager.get_user_credentials(self.transformation_user)
        snf_connection = SnowflakeConnection(
            user=credentials["user"],
            password=credentials["password"],
            account=credentials["account"],
            warehouse=credentials["warehouse"],
            database=credentials["database"],
            role=f'"{self.transformation_user}"',
            schema=self.working_kex.kex,
            client_session_keep_alive=True,
        )

        for query in self.component_manager.get_queries(skip_files):
            query = query.replace('"tr"', '"{}"'.format(self.working_kex.kex))
            with stopwatch(log_msg=query, caller_class=__class__.__name__):
                resultset = snf_connection.cursor().execute(query)
                result = resultset.fetchall()
            self._chek_message(result, resultset, query)

    def _chek_message(self, result, resultset, query):
        if not result:
            # Empty result = CREATE TABLE-like query
            pass
        else:
            if "message" in [c[0] for c in resultset.description]:
                # Our special SELECT containing debug data
                line = result[0][0]
                mtype, message = line.split(":")
                if mtype.upper() == "ERROR":
                    logger.error("Error from SQL: %s", message)
                    raise Exception(message)
                elif mtype.upper() == "WARNING":
                    logger.warning("Warning from SQL: %s", message)
                    mail_text = """{0}\n\nPreceding warning was generated from following query:\n{1}""".format(
                        message, query.replace("`", "\\`")
                    )
                    # TODO: error message elsewhere already
                    print(mail_text)
