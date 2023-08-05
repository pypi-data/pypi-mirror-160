from logging import getLogger

from toolkit.executors.extractor import DockerExtractorExecutor
from toolkit.managers.configuration.component import ComponentLoader

logger = getLogger(__name__)


class BaseExtractorLoader(ComponentLoader):
    component_type = "extractor"

    def get_extractors_ids(self):
        return self.get_components_ids()

    def get_extractor_name(self, extractor_id):
        raise NotImplementedError

    def get_extractor_executor(self, extractor_id):
        worker_manager = self.project_loader.get_worker_manager()
        component_manager = self.get_docker_component_manager(extractor_id)
        file_storage_manager = self.project_loader.get_file_storage_manager(
            prefix=component_manager.component_relative_path
        )

        return DockerExtractorExecutor(
            storage_manager=self.project_loader.get_storage_manager(),
            worker_manager=worker_manager,
            file_storage_manager=file_storage_manager,
            component_manager=component_manager,
            step=self.project_loader.get_step(),
        )
