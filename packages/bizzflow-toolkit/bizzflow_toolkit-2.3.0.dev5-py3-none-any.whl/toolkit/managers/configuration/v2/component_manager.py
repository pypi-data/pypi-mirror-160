import os
from logging import getLogger

from toolkit.managers.configuration.component_manager import BaseComponentManagerLoader

logger = getLogger(__name__)


class ComponentManagerLoader(BaseComponentManagerLoader):
    def _get_sql_folder_path(self, config):
        component_source = self._get_component_source(config)
        return os.path.join(self.project_loader.project_path, component_source["path"])

    def _get_component_source(self, config, component_type=None) -> dict:
        return config["source"]

    def _get_component_name(self, config, component_type=None) -> str:
        return config["name"]
