import os
from logging import getLogger
from typing import TYPE_CHECKING, Dict

from toolkit.base.step import CopyConf, FilterConf, Step, UnionConf, WhitelistConf
from toolkit.managers.configuration.validators import BaseConfigValidator

if TYPE_CHECKING:
    from toolkit.managers.configuration.loader import BaseConfigurationLoader

logger = getLogger(__name__)


class BaseStepLoader:
    validatorClass = BaseConfigValidator

    def __init__(self, project_loader: "BaseConfigurationLoader"):
        self.project_loader = project_loader
        self.validator = self.validatorClass(self.project_loader.file_loader)
        self.project_path = self.project_loader.project_path
        self.config_file_format = self.project_loader.config_file_format
        self.project_config = self.project_loader.project_config
        self._step_config = None
        self._step = None

    @property
    def step_config(self):
        if self._step_config is None:
            self._step_config = self._load_step_file()
        return self._step_config

    def _load_step_file(self) -> dict:
        logger.info("Loading step config")
        path = os.path.join(self.project_path, f"step.{self.config_file_format}")
        config = self.project_loader.load_file(self.config_file_format, path) or {}
        self.validator.validate(config)
        return config

    def get_step(self):
        if self._step is None:
            self._step = Step(
                storage_manager=self.project_loader.get_storage_manager(),
                credentials_manager=self.project_loader.get_credentials_manager(),
                unions=self._get_unions(),
                whitelists=self._get_whitelists(),
                filters=self._get_filters(),
                copies=self._get_copies(),
            )
        return self._step

    def _get_unions(self) -> Dict[str, UnionConf]:
        raise NotImplementedError

    def _get_whitelists(self) -> Dict[str, WhitelistConf]:
        raise NotImplementedError

    def _get_filters(self) -> Dict[str, FilterConf]:
        raise NotImplementedError

    def _get_copies(self) -> Dict[str, CopyConf]:
        raise NotImplementedError

    def validate(self):
        # just access step_config validation is included
        self.step_config  # noqa
