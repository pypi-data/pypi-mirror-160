import os
from logging import getLogger

from toolkit.executors.transformation.azure_sql import AzureSQLTransformationExecutor
from toolkit.executors.transformation.bq_sql import BqSqlTransformationExecutor
from toolkit.executors.transformation.docker import DockerTransformationExecutor
from toolkit.executors.transformation.postgre_sql import PostgreSQLTransformationExecutor
from toolkit.executors.transformation.redshift_sql import RedshiftTransformationExecutor
from toolkit.executors.transformation.snowflake_sql import SnowflakeSqlTransformationExecutor
from toolkit.managers.component.sql import BlankTransformationSQLComponentManager
from toolkit.managers.configuration.component import ComponentLoader
from toolkit.managers.configuration.utils import reveal_credentials
from toolkit.managers.configuration.validators import BaseConfigValidator

logger = getLogger(__name__)


class BaseTransformationsLoader(ComponentLoader):
    component_type = "transformation"

    TRANSFORMATION_EXECUTORS = {
        "snowflake": SnowflakeSqlTransformationExecutor,
        "bigquery": BqSqlTransformationExecutor,
        "azuresql": AzureSQLTransformationExecutor,
        "postgresql": PostgreSQLTransformationExecutor,
        "redshift": RedshiftTransformationExecutor,
    }

    def discover(self) -> dict:
        transformations = {}
        logger.info("Creating list of transformations")
        path = os.path.join(self.project_path, f"transformations.{self.config_file_format}")
        config = self.project_loader.load_file(self.config_file_format, path) or []
        self.validator.validate(config, self.project_path)
        for tr_config in config:
            transformations[tr_config["id"]] = tr_config
        return transformations

    def get_transformations_ids(self):
        return self.get_components_ids()

    def get_transformation_executor(self, transformation_id):
        config = self.get_component_config(transformation_id)
        vault_manager = self.project_loader.get_vault_manager()
        config = reveal_credentials(config, vault_manager)
        if config["type"] == "sql":
            component_manager = self.component_manager_loader.get_sql_transformation_component_manager(
                transformation_id=transformation_id,
                config=config,
                query_timeout=self._get_default_query_timeout(),
            )
            return self._get_sql_transformation_executor(
                component_manager=component_manager, inputs=self._get_inputs(config), output=self._get_output(config)
            )
        elif config["type"] == "docker":
            component_manager = self.get_docker_component_manager(transformation_id)
            return DockerTransformationExecutor(
                storage_manager=self.project_loader.get_storage_manager(),
                worker_manager=self.project_loader.get_worker_manager(),
                file_storage_manager=self.project_loader.get_file_storage_manager(
                    prefix=component_manager.component_relative_path
                ),
                component_manager=component_manager,
                step=self.project_loader.get_step(),
                inputs=self._get_inputs(config),
                output=self._get_output(config),
            )

    def get_component_config(self, component_id):
        return self.components[component_id]

    def validate(self):
        # just access transformations validation is included
        self.get_transformations_ids()

    def _get_sql_transformation_executor(self, component_manager, inputs, output):
        storage_backend = self._get_storage_backend()
        try:
            TransformationExecutor = self.TRANSFORMATION_EXECUTORS[storage_backend]
        except KeyError:
            raise NotImplementedError(f"Unsupported transformation for {storage_backend}")
        return TransformationExecutor(
            storage_manager=self.project_loader.get_storage_manager(),
            credentials_manager=self.project_loader.get_credentials_manager(),
            component_manager=component_manager,
            step=self.project_loader.get_step(),
            inputs=inputs,
            output=output,
        )

    def get_blank_transformation_executor(self, type):
        if type == "sql":
            return self._get_sql_transformation_executor(
                component_manager=BlankTransformationSQLComponentManager(), inputs=[], output=""
            )

    def _get_inputs(self, config: dict):
        raise NotImplementedError

    def _get_output(self, config: dict):
        raise NotImplementedError

    def _get_storage_backend(self):
        raise NotImplementedError

    def _get_default_query_timeout(self):
        raise NotImplementedError
