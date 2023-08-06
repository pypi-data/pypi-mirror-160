import logging
import os

from toolkit.base import Step, Table
from toolkit.executors.base.base import BaseExecutor, InputMixin, OutputMixin
from toolkit.managers.component.docker import BaseDockerComponentManager
from toolkit.managers.file_storage.base import BaseFileStorageManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.managers.worker.base import BaseWorkerManager
from toolkit.utils.stopwatch import stopwatch

logger = logging.getLogger(__name__)


class DockerExecutor(BaseExecutor):
    def __init__(
        self,
        worker_manager: BaseWorkerManager,
        storage_manager: BaseStorageManager,
        file_storage_manager: BaseFileStorageManager,
        component_manager: BaseDockerComponentManager,
        step: Step,
    ):
        super().__init__(storage_manager, component_manager, step)
        self.file_storage_manager = file_storage_manager
        self.worker_manager = worker_manager

    def create_environment(self):
        with stopwatch("Create environment", __class__.__name__):
            super().create_environment()
            self.file_storage_manager.clean_up_live_storage()
            self.worker_manager.ensure_virtual_machine_is_running()
            self.component_manager.init_component()
            self.component_manager.get_docker_image()
            self.component_manager.create_config_dir()
            self.component_manager.load_config_file_to_worker()

    def run(self, **kwargs):
        volumes = " -v ".join(self.get_docker_volumes())
        docker_command = f"docker run --rm -v {volumes} {self.component_manager.component_name}"
        with stopwatch(log_msg=docker_command, caller_class=__class__.__name__):
            result = self.worker_manager.run(docker_command, hide=False)
            if not result.ok:
                logger.error("Error occurred during job")
                logger.error(result.stdout)
                logger.error(result.stderr)
                raise Exception("Error occurred during job. See log above for more details.")
            logger.info("Job finished successfully")

    @stopwatch("Clean environment", __qualname__)
    def clean_environment(self):
        """Clean worker machine Shutdown worker if specified.

        Keyword Arguments:
            shutdown_worker {bool} -- Whether to shutdown worker afterwards (default: {True})
        """
        self.component_manager.clean_component()
        super().clean_environment()

        self.file_storage_manager.clean_up_live_storage()

    def get_docker_volumes(self):
        volumes = []
        volumes.append(f"{self.component_manager.host_volume_config_path}:/config/")
        return volumes


class DockerInputMixin(InputMixin):
    @stopwatch("Create environment", __qualname__)
    def create_environment(self):
        super().create_environment()
        self.create_input_dir()

    def create_input_dir(self):
        result = self.worker_manager.run(f"mkdir -p '{self.component_manager.worker_component_input_path}'", hide=True)
        if not result.ok:
            raise Exception("Could not create component input dir.\n{}\n{}".format(result.stdout, result.stderr))

    @stopwatch("Process input table", __qualname__)
    def process_input_table(self, table):
        destination = super().process_input_table(table)
        logger.info(
            f"Unloading table {destination.get_id()} -> to worker machine folder {self.component_manager.worker_component_input_path}"
        )
        self.storage_manager.export_to_worker(
            destination,
            self.component_manager.worker_component_input_path,
            self.worker_manager,
            self.file_storage_manager,
        )

    def get_docker_volumes(self) -> list:
        volumes = super().get_docker_volumes()
        volumes.append(f"{self.component_manager.host_volume_input_path}:/data/in/tables/")
        return volumes


class DockerOutputMixin(OutputMixin):
    @stopwatch("Create output mapping", __qualname__)
    def create_output_mapping(self):
        self.file_storage_manager.upload_files_from_worker(
            self.worker_manager, self.component_manager.worker_component_output_path
        )
        self.load_output_to_storage()
        super().create_output_mapping()

    def load_output_to_storage(self):
        blobs = self.file_storage_manager.list_files("")
        for blob in blobs:
            logger.info("About to load blob %s", blob)
            basename = os.path.basename(blob)
            table_name = self.storage_manager.normalize_string(os.path.splitext(basename)[0])
            table = Table(kex=self.working_kex, table_name=table_name)
            self.storage_manager.load_table(table, basename, self.file_storage_manager)

    @stopwatch("Create docker environment", __qualname__)
    def create_environment(self):
        super().create_environment()
        self.create_output_dir()

    def get_docker_volumes(self) -> list:
        volumes = super().get_docker_volumes()
        volumes.append(f"{self.component_manager.host_volume_output_path}:/data/out/tables/")
        return volumes

    def create_output_dir(self):
        result = self.worker_manager.run(f"mkdir -p '{self.component_manager.worker_component_output_path}'", hide=True)
        if not result.ok:
            raise Exception("Could not create component output dir.\n{}\n{}".format(result.stdout, result.stderr))


class DockerInputOutputMixin(DockerInputMixin, DockerOutputMixin):
    pass
