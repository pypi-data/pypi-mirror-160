from logging import getLogger

from toolkit.managers.configuration.extractor import BaseExtractorLoader
from toolkit.managers.configuration.v2.component_manager import ComponentManagerLoader
from toolkit.managers.configuration.v2.validators import ExtractorValidator

logger = getLogger(__name__)


class ExtractorLoader(BaseExtractorLoader):
    validatorClass = ExtractorValidator
    component_manager_loader_class = ComponentManagerLoader

    def get_extractor_name(self, extractor_id):
        return self.get_component_config(extractor_id)["name"]
