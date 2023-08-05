import os
from logging import getLogger
from typing import TYPE_CHECKING

from toolkit.managers.configuration.validators import BaseConfigValidator
from toolkit.managers.datamart.datamart_manager import DatamartManager

if TYPE_CHECKING:
    from toolkit.managers.configuration.loader import BaseConfigurationLoader

logger = getLogger(__name__)


class BaseDatamartLoader:
    validatorClass = BaseConfigValidator

    def __init__(self, project_loader: "BaseConfigurationLoader"):
        self.project_loader = project_loader
        self.validator = self.validatorClass(self.project_loader.file_loader)
        self._datamarts = None
        self.project_path = self.project_loader.project_path
        self.config_file_format = self.project_loader.config_file_format
        self.project_config = self.project_loader.project_config

    def _load_datamarts_file(self) -> dict:
        datamarts = {}
        logger.info("Creating list of datamarts")
        path = os.path.join(self.project_path, f"datamarts.{self.config_file_format}")
        config = self.project_loader.load_file(self.config_file_format, path) or []
        self.validator.validate(config)
        for dm_config in config:
            datamarts[dm_config["id"]] = dm_config
        return datamarts

    @property
    def datamarts(self):
        if self._datamarts is None:
            self._datamarts = self._load_datamarts_file()
        return self._datamarts

    def get_datamarts(self):
        return self.datamarts.keys()

    def get_datamart_manager(self, datamart_id):
        config = self.datamarts[datamart_id]
        return DatamartManager(
            storage_manager=self.project_loader.get_storage_manager(),
            credentials_manager=self.project_loader.get_credentials_manager(),
            out_kex=config["out_kex"],
            dm_kex=config["dm_kex"],
            allowed_tables=config.get("allowed_tables"),
        )

    def validate(self):
        # just access datamarts validation is included
        self.get_datamarts()
