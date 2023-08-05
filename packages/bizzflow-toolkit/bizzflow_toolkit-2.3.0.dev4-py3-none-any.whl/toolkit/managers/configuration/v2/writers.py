from logging import getLogger

from toolkit.managers.configuration.v2.component_manager import ComponentManagerLoader
from toolkit.managers.configuration.v2.validators import WriterValidator
from toolkit.managers.configuration.writers import BaseWriterLoader

logger = getLogger(__name__)


class WriterLoader(BaseWriterLoader):
    validatorClass = WriterValidator
    component_manager_loader_class = ComponentManagerLoader

    def _get_inputs(self, config: dict):
        return config["input"]

    def get_writer_name(self, writer_id):
        return self.get_component_config(writer_id)["name"]
