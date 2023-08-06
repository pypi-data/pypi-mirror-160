
from toolkit.managers.configuration.v1.component_manager import ComponentManagerLoader
from toolkit.managers.configuration.v1.helpers import get_input
from toolkit.managers.configuration.v1.validators import WriterValidator
from toolkit.managers.configuration.writers import BaseWriterLoader



class WriterLoader(BaseWriterLoader):
    validatorClass = WriterValidator
    component_manager_loader_class = ComponentManagerLoader

    def _get_inputs(self, config: dict):
        return get_input(config)

    def get_writer_name(self, writer_id):
        return self.get_component_config(writer_id)["type"]
