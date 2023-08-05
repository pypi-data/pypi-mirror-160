import os
from logging import getLogger
from typing import TYPE_CHECKING

from toolkit.managers.configuration.utils import reveal_credentials
from toolkit.managers.configuration.validators import BaseConfigValidator

if TYPE_CHECKING:
    from toolkit.managers.configuration.loader import BaseConfigurationLoader

logger = getLogger(__name__)


class ComponentLoader:
    component_type = NotImplemented
    validatorClass = BaseConfigValidator
    component_manager_loader_class = NotImplemented

    def __init__(self, project_loader: "BaseConfigurationLoader"):
        self.project_loader = project_loader
        self.validator = self.validatorClass(self.project_loader.file_loader)
        self.component_manager_loader = self.component_manager_loader_class(self.project_loader)
        self._components = None
        self.project_path = self.project_loader.project_path
        self.config_file_format = self.project_loader.config_file_format
        self.project_config = self.project_loader.project_config

    @property
    def components(self):
        if self._components is None:
            self._components = self.discover()
        return self._components

    def get_components_ids(self):
        return self.components.keys()

    def discover(self):
        logger.info(f"Creating list of {self.component_type}")
        path = os.path.join(self.project_path, f"{self.component_type}s")
        components = {}
        try:
            components_files = self.project_loader.file_loader.list_directory(path)
        except FileNotFoundError:
            logger.warning(f"Missing folder {path}")
        else:
            for name in [c for c in components_files if c.lower().endswith(self.config_file_format)]:
                component_id = str(os.path.splitext(name)[0])
                component_config_file = str(os.path.join(path, name))
                components[component_id] = component_config_file
        return components

    def get_component_config(self, component_id):
        component_config = self.components[component_id]
        if isinstance(component_config, str):
            # config not loaded yet (str mean just path to config file) so load it first
            component_config = self.project_loader.load_file(self.config_file_format, component_config) or {}
            self.validator.validate(component_config)
            self.components[component_id] = component_config
        #  do not store component config with reveal secrets but to it every time
        #  - so it will be up-to-date even when you change it in vault
        vault_manager = self.project_loader.get_vault_manager()
        component_config = reveal_credentials(component_config, vault_manager)
        return component_config

    def get_docker_component_manager(self, component_id):
        return self.component_manager_loader.get_docker_component_manager(
            self.component_type, component_id, self.get_component_config(component_id)
        )

    def validate(self):
        for component_id in self.get_components_ids():
            # validation is during load
            self.get_component_config(component_id)
