from logging import getLogger

from toolkit.executors.writer.docker import DockerWriterExecutor
from toolkit.managers.configuration.component import ComponentLoader

logger = getLogger(__name__)


class BaseWriterLoader(ComponentLoader):
    component_type = "writer"

    def get_writers_ids(self):
        return self.get_components_ids()

    def get_writer_name(self, writer_id):
        raise NotImplementedError

    def get_writer_executor(self, writer_id):
        worker_manager = self.project_loader.get_worker_manager()
        component_manager = self.get_docker_component_manager(writer_id)

        file_storage_manager = self.project_loader.get_file_storage_manager(
            prefix=component_manager.component_relative_path
        )

        return DockerWriterExecutor(
            storage_manager=self.project_loader.get_storage_manager(),
            worker_manager=worker_manager,
            file_storage_manager=file_storage_manager,
            component_manager=component_manager,
            step=self.project_loader.get_step(),
            inputs=self._get_inputs(self.get_component_config(writer_id)),
        )

    def _get_inputs(self, config):
        raise NotImplementedError
