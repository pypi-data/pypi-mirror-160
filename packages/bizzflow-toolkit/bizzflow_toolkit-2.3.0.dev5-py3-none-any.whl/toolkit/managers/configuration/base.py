import os
from typing import List

from toolkit.managers.configuration.exceptions import ConfigurationNotValid
from toolkit.managers.configuration.file_loader import LocalFileLoader, S3FileLoader
from toolkit.managers.configuration.loader import BaseConfigurationLoader
from toolkit.managers.configuration.orchestration import Orchestration
from toolkit.managers.configuration.v1.loader import V1ConfigurationLoader
from toolkit.managers.configuration.v2.loader import V2ConfigurationLoader
from toolkit.managers.sandbox.sandbox_manager import SandboxManager
from toolkit.managers.storage.base import BaseStorageManager


class ConfigurationManager:
    def __init__(self, project_path=None):
        self._project_path = project_path
        self._loader = None

    @property
    def project_path(self):
        return self._project_path or os.getenv("BIZZFLOW_PROJECT_PATH") or os.path.join(os.getenv("HOME"), "project")

    def get_file_loader(self):
        if self.project_path.startswith("s3://"):
            return S3FileLoader()
        return LocalFileLoader()

    def refresh(self):
        self.__init__(self.project_path)

    def validate(self):
        self.loader.validate()

    @property
    def loader(self) -> BaseConfigurationLoader:
        if self._loader is None:
            self._loader = self._get_project_loader()
        return self._loader

    def _get_project_loader(self):
        """
        Load project configuration.

        Raises:
            Exception: If configuration not specified
            ConfigurationNotValid: If invalid format of config file
        """
        file_loader = self.get_file_loader()
        for file_format in ["yaml", "json"]:
            file_path = os.path.join(self.project_path, f"project.{file_format}")
            if file_loader.file_exists(file_path):
                config = BaseConfigurationLoader.load_file(file_format, file_path, file_loader) or {}
                version = config.get("version", 1)
                if version == 1:
                    return V1ConfigurationLoader(self.project_path, config, file_format, file_loader)
                elif version == 2:
                    return V2ConfigurationLoader(self.project_path, config, file_format, file_loader)
                else:
                    raise ConfigurationNotValid(f"Unsupported config version: {version}")
        else:
            raise ConfigurationNotValid(f"Configuration not specified, not found at {self.project_path}")

    @property
    def project_id(self):
        return self.loader.project_id

    @property
    def telemetry(self) -> dict:
        return self.loader.telemetry

    @property
    def notification_emails(self) -> List[str]:
        return self.loader.notification_emails

    def get_transformations_ids(self):
        return self.loader.get_transformations_ids()

    def get_extractors_ids(self):
        return self.loader.get_extractors_ids()

    def get_writers_ids(self):
        return self.loader.get_writers_ids()

    def get_datamarts_ids(self):
        return self.loader.get_datamarts_ids()

    def get_orchestrations_ids(self):
        return self.loader.get_orchestrations_ids()

    def get_storage_manager(self) -> BaseStorageManager:
        return self.loader.get_storage_manager()

    def get_credentials_manager(self):
        return self.loader.get_credentials_manager()

    def get_vault_manager(self):
        return self.loader.get_vault_manager()

    def get_step(self):
        return self.loader.get_step()

    def get_extractor_name(self, extractor_id):
        return self.loader.get_extractor_name(extractor_id)

    def get_extractor_executor(self, extractor_id):
        return self.loader.get_extractor_executor(extractor_id)

    def get_transformation_executor(self, transformation_id):
        return self.loader.get_transformation_executor(transformation_id)

    def _get_blank_transformation_executor(self, type):
        return self.loader.get_blank_transformation_executor(type)

    def get_writer_name(self, writer_id):
        return self.loader.get_writer_name(writer_id)

    def get_writer_executor(self, writer_id):
        return self.loader.get_writer_executor(writer_id)

    def get_datamart_manager(self, datamart_id):
        return self.loader.get_datamart_manager(datamart_id)

    def get_sandbox_manager(self, sandbox_user_email, transformation_id=None):
        if transformation_id is not None:
            transformation_executor = self.get_transformation_executor(transformation_id)
        else:
            transformation_executor = self._get_blank_transformation_executor(type="sql")
        return SandboxManager(sandbox_user_email=sandbox_user_email, transformation_executor=transformation_executor)

    def get_orchestration(self, orchestration_id) -> Orchestration:
        return self.loader.get_orchestration(orchestration_id)
