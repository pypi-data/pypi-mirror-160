from typing import TYPE_CHECKING

from toolkit.managers.configuration.transformations import BaseTransformationsLoader
from toolkit.managers.configuration.v1.component_manager import ComponentManagerLoader
from toolkit.managers.configuration.v1.helpers import get_input
from toolkit.managers.configuration.v1.validators import TransformationsValidator

if TYPE_CHECKING:
    from toolkit.managers.configuration.v1.loader import V1ConfigurationLoader



class TransformationsLoader(BaseTransformationsLoader):
    validatorClass = TransformationsValidator
    component_manager_loader_class = ComponentManagerLoader

    def __init__(self, project_loader: "V1ConfigurationLoader"):
        super().__init__(project_loader)

    def _get_inputs(self, config: dict):
        return get_input(config)

    def _get_output(self, config: dict):
        return config["out_kex"]

    def _get_storage_backend(self):
        storage_manager_class = self.project_config["classes"]["storage_manager"]
        if storage_manager_class == "AzureSQLStorageManager":
            return "azuresql"
        elif storage_manager_class == "BqStorageManager":
            return "bigquery"
        elif storage_manager_class == "SnowflakeStorageManager":
            return "snowflake"
        elif storage_manager_class == "PostgreSQLStorageManager":
            return "postgresql"
        elif storage_manager_class == "RedshiftStorageManager":
            return "redshift"
        raise NotImplementedError

    def _get_default_query_timeout(self):
        return self.project_config["query_timeout"]
