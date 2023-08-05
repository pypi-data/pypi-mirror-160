import json
import logging
from contextlib import closing

import yaml

from toolkit.managers.configuration.datamarts import BaseDatamartLoader
from toolkit.managers.configuration.exceptions import ConfigurationNotValid
from toolkit.managers.configuration.extractor import BaseExtractorLoader
from toolkit.managers.configuration.file_loader import BaseFileLoader
from toolkit.managers.configuration.orchestration import BaseOrchestrationLoader
from toolkit.managers.configuration.sharing import BaseSharingLoader
from toolkit.managers.configuration.step import BaseStepLoader
from toolkit.managers.configuration.transformations import BaseTransformationsLoader
from toolkit.managers.configuration.validators import BaseConfigValidator
from toolkit.managers.configuration.writers import BaseWriterLoader
from toolkit.managers.vault.airflow import AirflowVaultManager



logger = logging.getLogger(__name__)

class BaseConfigurationLoader:
    validatorClass = BaseConfigValidator
    TransformationLoaderClass = BaseTransformationsLoader
    ExtractorLoaderClass = BaseExtractorLoader
    WriterLoaderClass = BaseWriterLoader
    DatamartLoaderClass = BaseDatamartLoader
    OrchestrationLoaderClass = BaseOrchestrationLoader
    StepLoaderClass = BaseStepLoader
    SharingLoaderClass = BaseSharingLoader

    def __init__(self, project_path, project_config, config_file_format, file_loader: BaseFileLoader):
        self.project_path = project_path
        self.config_file_format = config_file_format
        self.project_config = project_config
        self.file_loader = file_loader
        self.validator = self.validatorClass(self.file_loader)
        self.transformation_loader = self.TransformationLoaderClass(self)
        self.extractor_loader = self.ExtractorLoaderClass(self)
        self.writer_loader = self.WriterLoaderClass(self)
        self.datamart_loader = self.DatamartLoaderClass(self)
        self.orchestration_loader = self.OrchestrationLoaderClass(self)
        self.sharing_loader = self.SharingLoaderClass(self)
        self.step_loader = self.StepLoaderClass(self)
        self._vault_manager = None
        self._storage_manager = None
        self._credential_manager = None
        self._worker_manager = None

    @classmethod
    def _load_json_file(cls, path, file_loader: BaseFileLoader):
        with closing(file_loader.get_file(path)) as conf:
            try:
                config = json.load(conf)
                return config or None
            except ValueError as e:
                logger.error("Invalid format of config file: %s", e)
                raise ConfigurationNotValid("Invalid format of config file: {}".format(e))

    @classmethod
    def _load_yaml_file(cls, path, file_loader: BaseFileLoader):
        with closing(file_loader.get_file(path)) as conf:
            try:
                config = yaml.safe_load(conf)
                return config or None
            except yaml.YAMLError as e:
                logger.error("Invalid format of config file: %s", e)
                raise ConfigurationNotValid("Invalid format of config file: {}".format(e))

    @classmethod
    def load_file(cls, file_format: str, path: str, file_loader: BaseFileLoader):
        if file_format == "yaml":
            return cls._load_yaml_file(path, file_loader)
        elif file_format == "json":
            return cls._load_json_file(path, file_loader)
        else:
            raise NotImplementedError

    def validate(self):
        self.validator.validate(self.project_config)
        self.transformation_loader.validate()
        self.extractor_loader.validate()
        self.writer_loader.validate()
        self.datamart_loader.validate()
        self.orchestration_loader.validate()
        self.step_loader.validate()
        self.sharing_loader.validate()

    @property
    def project_id(self):
        return self.project_config["project_id"]

    @property
    def telemetry(self):
        return self.project_config.get("telemetry", {"generate": False})

    @property
    def notification_emails(self):
        raise NotImplementedError

    def get_transformations_ids(self):
        return self.transformation_loader.get_transformations_ids()

    def get_extractors_ids(self):
        return self.extractor_loader.get_extractors_ids()

    def get_writers_ids(self):
        return self.writer_loader.get_writers_ids()

    def get_datamarts_ids(self):
        return self.datamart_loader.get_datamarts()

    def get_orchestrations_ids(self):
        return self.orchestration_loader.get_orchestrations()

    def get_storage_manager(self):
        raise NotImplementedError

    def get_worker_manager(self):
        raise NotImplementedError

    def get_file_storage_manager(self, prefix):
        raise NotImplementedError

    def get_credentials_manager(self):
        raise NotImplementedError

    def get_vault_manager(self):
        if self._vault_manager is None:
            self._vault_manager = AirflowVaultManager().build_default()
        return self._vault_manager

    def get_step(self):
        return self.step_loader.get_step()

    def get_extractor_name(self, extractor_id):
        return self.extractor_loader.get_extractor_name(extractor_id)

    def get_extractor_executor(self, extractor_id):
        return self.extractor_loader.get_extractor_executor(extractor_id)

    def get_transformation_executor(self, transformation_id):
        return self.transformation_loader.get_transformation_executor(transformation_id)

    def get_blank_transformation_executor(self, type):
        return self.transformation_loader.get_blank_transformation_executor(type)

    def get_writer_name(self, writer_id):
        return self.writer_loader.get_writer_name(writer_id)

    def get_writer_executor(self, writer_id):
        return self.writer_loader.get_writer_executor(writer_id)

    def get_datamart_manager(self, datamart_id):
        return self.datamart_loader.get_datamart_manager(datamart_id)

    def get_orchestration(self, orchestration_id):
        return self.orchestration_loader.get_orchestration(orchestration_id)
