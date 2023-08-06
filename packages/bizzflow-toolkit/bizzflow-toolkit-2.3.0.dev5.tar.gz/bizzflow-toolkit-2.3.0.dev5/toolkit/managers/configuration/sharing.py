import os
from logging import getLogger
from typing import TYPE_CHECKING

from toolkit.managers.configuration.utils import reveal_credentials
from toolkit.managers.configuration.validators import BaseConfigValidator
from toolkit.managers.storage.azure_sql import AzureSQLSharedSourceConfig, AzureSQLSharingConfig

if TYPE_CHECKING:
    from toolkit.managers.configuration.loader import BaseConfigurationLoader

logger = getLogger(__name__)


class BaseSharingLoader:
    validatorClass = BaseConfigValidator

    def __init__(self, project_loader: "BaseConfigurationLoader"):
        self.project_loader = project_loader
        self.validator = self.validatorClass(self.project_loader.file_loader)
        self._sources = None
        self._destinations = None
        self.project_path = self.project_loader.project_path
        self.config_file_format = self.project_loader.config_file_format
        self.project_config = self.project_loader.project_config
        self._is_loaded = False

    def _load_sharing_file(self):
        logger.info("Creating list of sharing")
        path = os.path.join(self.project_path, f"sharing.{self.config_file_format}")
        try:
            config = self.project_loader.load_file(self.config_file_format, path)
        except FileNotFoundError:
            config = {}
        self.validator.validate(config)
        vault_manager = self.project_loader.get_vault_manager()
        config = reveal_credentials(config, vault_manager)
        self._sources = config.get("sources", {})
        self._destinations = config.get("destinations", {})
        self._is_loaded = True

    @property
    def destinations(self):
        if not self._is_loaded:
            self._load_sharing_file()
        return self._destinations

    @property
    def sources(self):
        if not self._is_loaded:
            self._load_sharing_file()
        return self._sources

    def get_azure_sharing(self):
        sources = {}
        for project_name, config in self.sources.items():
            project = AzureSQLSharedSourceConfig(
                project_name=project_name,
                hostname=config["hostname"],
                database=config["database"],
                username=config["username"],
                password=config["password"],
            )
            sources[project_name] = project
        destinations = {}
        for project_name, config in self.destinations.items():
            for table_name in config["tables"]:
                if table_name in destinations:
                    destinations[table_name] = [*destinations[table_name], project_name]
                else:
                    destinations[table_name] = [project_name]
        return AzureSQLSharingConfig(sources, destinations)

    def validate(self):
        # just access sources validation is included
        self.sources  # noqa
