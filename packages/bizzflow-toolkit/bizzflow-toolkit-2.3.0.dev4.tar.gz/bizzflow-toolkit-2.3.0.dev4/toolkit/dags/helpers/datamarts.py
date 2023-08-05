import logging

from toolkit import current_config
from toolkit.dags.helpers.base import PythonTaskCreator

logger = logging.getLogger(__name__)


class DatamartTaskCreator(PythonTaskCreator):
    def __init__(self, datamart_id: str, **kwargs) -> None:
        super().__init__(f"dm_{datamart_id}", **kwargs)
        self.datamart_id = datamart_id

    def python_callable(self):
        datamart_manager = current_config.get_datamart_manager(self.datamart_id)
        datamart_manager.create_environment()
        datamart_manager.get_credentials()
        datamart_manager.write()
