import logging

from toolkit import current_config
from toolkit.dags.helpers.base import PythonTaskCreator

logger = logging.getLogger(__name__)


class RefreshSharingTaskCreator(PythonTaskCreator):
    def __init__(self):
        super().__init__("refresh_sharing", notify=False)

    def python_callable(self):
        credentials_manager = current_config.get_credentials_manager()
        storage_manager = current_config.get_storage_manager()

        for table in storage_manager.list_shared_out_tables():
            for destination_project in storage_manager.shared_out_table_destinations(table):
                logger.info(f"Sharing table {table.table} to project {destination_project}")
                user_name = f"sh_{destination_project}"
                credentials_manager.create_sharing_user(user_name)
                credentials_manager.share_table_to_user(user_name, table)
