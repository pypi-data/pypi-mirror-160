import os
from logging import getLogger
from typing import TYPE_CHECKING

from toolkit.managers.component.bizztreat_gitlab_docker import BizztreatGitLabDockerComponentManager
from toolkit.managers.component.docker_pull import DockerComponentManager
from toolkit.managers.component.git_docker import GitDockerComponentManager
from toolkit.managers.component.local_storage_docker import LocalStorageDockerComponentManager
from toolkit.managers.component.sql import LocalSQLTransformationComponentManager

if TYPE_CHECKING:
    from toolkit.managers.configuration.loader import BaseConfigurationLoader

logger = getLogger(__name__)


class BaseComponentManagerLoader:
    def __init__(self, project_loader: "BaseConfigurationLoader"):
        self.project_loader = project_loader

    def get_sql_transformation_component_manager(self, transformation_id, config, query_timeout):
        component_source = self._get_component_source(config, "transformation")
        return LocalSQLTransformationComponentManager(
            transformation_id=transformation_id,
            transformation_name=self._get_component_name(config, "transformation"),
            sql_folder_path=component_source["path"],
            query_timeout=config.get("query_timeout", query_timeout),
        )

    def get_docker_component_manager(self, component_type: str, component_id: str, config: dict):
        component_type = component_type
        component_config = config.get("config", {})
        component_source = self._get_component_source(config, component_type)
        component_name = self._get_component_name(config, component_type)

        if component_source["type"] == "bizztreat-gitlab":
            return BizztreatGitLabDockerComponentManager(
                component_type=component_type,
                component_name=component_name,
                component_id=component_id,
                component_config=component_config,
                worker_manager=self.project_loader.get_worker_manager(),
            )
        elif component_source["type"] == "git":
            return GitDockerComponentManager(
                component_type=component_type,
                component_name=component_name,
                component_id=component_id,
                component_config=component_config,
                worker_manager=self.project_loader.get_worker_manager(),
                git_repository=component_source["repository"],
                git_checkout=component_source.get("checkout"),
                git_username=component_source.get("username"),
                git_password=component_source.get("password"),
            )
        elif component_source["type"] == "local":
            return LocalStorageDockerComponentManager(
                component_type=component_type,
                component_name=component_name,
                component_id=component_id,
                component_config=component_config,
                worker_manager=self.project_loader.get_worker_manager(),
                file_storage_manager=self.project_loader.get_file_storage_manager("tmp"),
                component_source_path=os.path.join(self.project_loader.project_path, component_source["path"]),
            )
        elif component_source["type"] == "docker":
            return DockerComponentManager(
                component_type=component_type,
                component_name=component_name,
                component_id=component_id,
                component_config=component_config,
                worker_manager=self.project_loader.get_worker_manager(),
                docker_registry=component_source["registry"],
                docker_image=component_source["image"],
                docker_registry_username=component_source.get("username"),
                docker_registry_password=component_source.get("password"),
            )
        else:
            raise NotImplementedError("Unsupported source type")

    def _get_component_source(self, config, component_type=None) -> dict:
        raise NotImplementedError

    def _get_component_name(self, config, component_type=None) -> str:
        raise NotImplementedError
