import logging
import uuid
from typing import Optional

import toolkit
from toolkit.base import Kex, Step, Table
from toolkit.managers.component.base import BaseComponentManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.utils.stopwatch import stopwatch

logger = logging.getLogger(__name__)


class BaseExecutor:
    should_delete_working_kex = True

    def __init__(self, storage_manager: BaseStorageManager, component_manager: BaseComponentManager, step: Step):
        logger.info(f"Init {self.__class__}, using Bizzflow Toolkit version {toolkit.__version__}")
        self.storage_manager = storage_manager
        self.component_manager = component_manager
        self.step = step
        self.working_kex = Kex(self._create_working_kex_name())

    @stopwatch("Create environment/kex", __qualname__)
    def create_environment(self):
        self.storage_manager.create_kex(self.working_kex)

    def run(self, **kwargs):
        raise NotImplementedError

    @stopwatch("Clean environment/delete kex", __qualname__)
    def clean_environment(self):
        if self.should_delete_working_kex:
            self.storage_manager.delete_kex(self.working_kex)

    def _create_working_kex_name(self):
        return f"tmp_{uuid.uuid4().hex}"


class InputMixin:
    @stopwatch("Create input mapping", __qualname__)
    def create_input_mapping(self, inputs: Optional[list] = None):
        logger.info("Running input mapping")
        inputs = inputs or self.inputs
        in_tables = self.storage_manager.list_input_tables(inputs)
        logger.info("Input mapping tables: %s", str(in_tables))
        for table in in_tables:
            self.process_input_table(table)

    def process_input_table(self, table):
        logger.info("Processing input for table %s", table.get_id())
        destination_table = Table(table_name="in_{}".format(table.table), kex=self.working_kex)
        return self.step.process(table=table, default_destination=destination_table)

    @property
    def inputs(self):
        try:
            return self._inputs
        except AttributeError:
            return []


class OutputMixin:
    @stopwatch("Create output mapping", __qualname__)
    def create_output_mapping(self):
        if self.output_kex.get_id() not in [kex.get_id() for kex in self.storage_manager.list_kexes()]:
            logger.info("Output kex %s does not exist, creating", self.output_kex.get_id())
            self.storage_manager.create_kex(self.output_kex)
        for table in self.storage_manager.list_tables(self.working_kex):
            self.process_output_table(table)

    def process_output_table(self, table, output_table_name=None):
        output_table_name = output_table_name or table.table
        with stopwatch(f"Process output table {output_table_name}", __class__.__name__):
            default_output_table = Table(table_name=output_table_name, kex=self.output_kex)
            logger.info(f"Processing output for table {table.table}")
            return self.step.process(table, default_destination=default_output_table)

    def _create_output_kex_name(self) -> str:
        raise NotImplementedError

    @property
    def output_kex(self):
        try:
            return self._output_kex
        except AttributeError:
            self._output_kex = Kex(self._create_output_kex_name())
        return self._output_kex
