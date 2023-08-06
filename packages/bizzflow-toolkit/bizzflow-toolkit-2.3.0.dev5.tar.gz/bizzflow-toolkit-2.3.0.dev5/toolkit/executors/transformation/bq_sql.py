"""Class for executing transformation in Google BigQuery.
"""

import logging
from typing import Optional

from airflow.utils.email import send_email

from toolkit.base import Step
from toolkit.executors.transformation.base_sql import SqlTransformationExecutor
from toolkit.managers.component.sql import SQLTransformationComponentManager
from toolkit.managers.credentials.gcp import GcpCredentialsManager
from toolkit.managers.storage.bq_sql import BqStorageManager
from toolkit.utils.stopwatch import stopwatch

logger = logging.getLogger(__name__)

try:
    from google.cloud import bigquery
    from google.oauth2 import service_account
except ImportError:
    logger.info("Google Cloud Platform libraries are not installed.")


class BqSqlTransformationExecutor(SqlTransformationExecutor):
    """Class for executing transformation in Google BigQuery."""

    def __init__(
        self,
        storage_manager: BqStorageManager,
        component_manager: SQLTransformationComponentManager,
        step: Step,
        credentials_manager: GcpCredentialsManager,
        inputs: list,
        output: str,
    ):
        super().__init__(storage_manager, component_manager, step, credentials_manager, inputs, output)
        self.transformation_user = (
            self.component_manager.component_config.get("transformation_service_account") or "transformation"
        )

    def _generate_message(self, mtype, message, subject=None):
        """Generate message subject and text.

        Arguments:
            mtype {str} -- type of message e. g. WARNING

            message {str} -- content of "message" column

            subject {str} -- subject of message, it can be None, so default text will be used

        Returns:
            dict -- dictionary with message subject and text
        """
        if mtype.upper() == "ERROR":
            logger.error("Error from SQL: %s", message)
            raise Exception("Error from SQL: {}".format(message))
        elif mtype.upper() == "WARNING":
            logger.warning("WARNING ABOUT CHANGES OF IMPORTANT DATA INDICATORS: %s", message)
            if not subject:
                subject = """Bizzflow SQL Warning"""
                mail_text = "<h1>Bizzflow SQL notification</h1><h2>Warning</h2><p>{0}</p>".format(
                    message.replace("\n", "<br>")
                )
            else:
                subject = subject
                mail_text = "<p>{0}</p>".format(message.replace("\n", "<br>"))
        else:
            logger.warning("Unexpected type of message: %s", mtype)
            # TODO: decide - warning vs. error?
            # self.logger.error("Unexpected type of message: %s", mtype)
            # raise Exception("Unexpected type of message: {}".format(mtype))
        return {"subject": subject, "text": mail_text}

    def _check_messages(self, result, query):
        """Check if there is a column with name "message" in query result and send message.

        Arguments:
            result {google.cloud.bigquery.table.RowIterator} -- query job result

            query {str} -- whole query as a string
        """
        result_output = list(result)
        if len(result_output) == 0:
            # Create table-like query
            pass
        else:
            try:
                # TODO: refactor configuration manager shouldn't be used here - it should be used just when creating DAGs
                from toolkit import current_config

                notification_email = current_config.notification_emails[0]
            except KeyError:
                logger.warning("Not notification email set up")
            if "message" in [column.name for column in result.schema]:
                for line in result_output:
                    freq = line.message.count("|")
                    if freq == 1:
                        mtype, message = line.message.split("|")
                        message_parameters = self._generate_message(mtype, message)
                        send_email(
                            notification_email,
                            message_parameters["subject"],
                            message_parameters["text"],
                            mime_charset="utf-8",
                        )
                    elif freq == 2:
                        mtype, message, subject = line.message.split("|")
                        message_parameters = self._generate_message(mtype, message, subject)
                        send_email(
                            notification_email,
                            message_parameters["subject"],
                            message_parameters["text"],
                            mime_charset="utf-8",
                        )
                    elif freq == 3:
                        mtype, message, subject, emails = line.message.split("|")
                        emails_list = emails.split(",")
                        message_parameters = self._generate_message(mtype, message, subject)
                        for email in emails_list:
                            send_email(
                                email, message_parameters["subject"], message_parameters["text"], mime_charset="utf-8"
                            )
                    else:
                        logger.warning("Unexpected length of message: %s (%d pipes)", line.message, freq)
                        # TODO: decide - warning vs. error?
                        # self.logger.error("Unexpected length of message: %s (%d pipes)", line.message, freq)
                        # raise Exception("Unexpected length of message: {} ({} pipes)".format(line.message, freq))

    @stopwatch("Run transformation", __qualname__)
    def run(self, skip_files: Optional[list] = None, **kwargs):
        """Run transformation.
        Swith service account to transformation service account
        by creating BigQuery client with corresponding credentials.
        Run queries specified in the BqSqlTransformationExecutor config.
        Switch service account back to the original one.

        Raises:
            ValueError: If a query fails.
        """
        json_key = self.credentials_manager.get_user_credentials(self.transformation_user)
        credentials = service_account.Credentials.from_service_account_info(json_key)
        bq_client = bigquery.Client(credentials=credentials, project=json_key["project_id"])
        logger.info("Transformation service account: %s", json_key["client_email"])

        for query in self.component_manager.get_queries(skip_files):
            query = query.replace("`tr`", "`{}`".format(self.working_kex.kex))
            with stopwatch(log_msg=query, caller_class=__class__.__name__):
                query_job = bq_client.query(query)
                result = query_job.result(timeout=self.component_manager.query_timeout)
            self._check_messages(result, query)
