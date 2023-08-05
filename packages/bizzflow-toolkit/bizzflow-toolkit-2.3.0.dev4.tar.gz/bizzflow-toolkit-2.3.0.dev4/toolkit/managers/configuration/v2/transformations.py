from logging import getLogger
from typing import TYPE_CHECKING

from toolkit.managers.configuration.transformations import BaseTransformationsLoader
from toolkit.managers.configuration.v2.component_manager import ComponentManagerLoader
from toolkit.managers.configuration.v2.validators import TransformationsValidator

if TYPE_CHECKING:
    from toolkit.managers.configuration.v2.loader import V2ConfigurationLoader

logger = getLogger(__name__)


class TransformationsLoader(BaseTransformationsLoader):
    validatorClass = TransformationsValidator
    component_manager_loader_class = ComponentManagerLoader

    def __init__(self, project_loader: "V2ConfigurationLoader"):
        super().__init__(project_loader)

    def _get_inputs(self, config: dict):
        return config["input"]

    def _get_output(self, config: dict):
        return config["output"]

    def _get_storage_backend(self):
        return self.project_config["storage"]["backend"]

    def _get_default_query_timeout(self):
        return self.project_config["storage"].get("query_timeout")
