import logging

from toolkit.base import Step
from toolkit.base.table import Table
from toolkit.executors.base.base import BaseExecutor, InputMixin, OutputMixin
from toolkit.managers.component.sql import SQLTransformationComponentManager
from toolkit.managers.credentials.base import BaseCredentialsManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.utils.stopwatch import stopwatch

logger = logging.getLogger(__name__)


class SQLExecutor(BaseExecutor):
    def __init__(
        self,
        storage_manager: BaseStorageManager,
        component_manager: SQLTransformationComponentManager,
        step: Step,
        credentials_manager: BaseCredentialsManager,
    ):
        super().__init__(storage_manager, component_manager, step)
        self.credentials_manager = credentials_manager
        self.schema_name = self.working_kex.kex


class SQLInputMixin(InputMixin):
    pass


class SQLOutputMixin(OutputMixin):
    def process_output_table(self, table: Table, table_name=None):
        if table.table.startswith("out_"):
            with stopwatch(f"Process output table {table.full_id}", __class__.__name__):
                super().process_output_table(table, table.table[4:])


class SQLInputOutputMixin(SQLInputMixin, SQLOutputMixin):
    pass
