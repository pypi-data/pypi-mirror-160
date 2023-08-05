import json
import os
from io import StringIO
from logging import getLogger

from toolkit.managers.component.base import BaseComponentManager
from toolkit.managers.worker.base import BaseWorkerManager

logger = getLogger(__name__)


class BaseDockerComponentManager(BaseComponentManager):
    """
    Base class for obtaining docker image it can be download and build from git/storage or just pull from dockerhub
    """

    def __init__(
        self,
        component_type: str,
        component_name: str,
        component_id: str,
        component_config: dict,
        worker_manager: BaseWorkerManager,
    ):
        super().__init__(component_type, component_name, component_id, component_config)
        self.worker_manager = worker_manager
        self.worker_component_path = os.path.join(self.worker_manager.components_path, self.component_relative_path)
        self.worker_component_config_path = os.path.join(self.worker_manager.config_path, self.component_relative_path)
        self.worker_component_data_path = os.path.join(self.worker_manager.data_path, self.component_relative_path)
        self.worker_component_input_path = os.path.join(self.worker_component_data_path, "input")
        self.worker_component_output_path = os.path.join(self.worker_component_data_path, "output")
        worker_context = os.getenv("WORKER_CONTEXT")
        if worker_context is None:
            self.host_volume_config_path = self.worker_component_config_path
            self.host_volume_data_path = self.worker_component_data_path
            self.host_volume_input_path = self.worker_component_input_path
            self.host_volume_output_path = self.worker_component_output_path
        else:
            self.host_volume_config_path = os.path.join(worker_context, "config", self.component_relative_path)
            self.host_volume_data_path = os.path.join(worker_context, "data", self.component_relative_path)
            self.host_volume_input_path = os.path.join(self.host_volume_data_path, "input")
            self.host_volume_output_path = os.path.join(self.host_volume_data_path, "output")

    def init_component(self):
        result = self.worker_manager.run(
            f"echo {self.component_type}_{self.component_id} >> RUNNING_COMPONENTS", warn=True
        )
        if not result.ok:
            raise Exception(f"Could not set component running flag \n{result.stdout}\n{result.stderr}")
        self.clean_component_folder()

    def get_docker_image(self):
        raise NotImplementedError

    def create_config_dir(self):
        result = self.worker_manager.run(f"mkdir -p '{self.worker_component_config_path}'", warn=True)
        if not result.ok:
            raise Exception("Could not create component config dir.\n{}\n{}".format(result.stdout, result.stderr))

    def load_config_file_to_worker(self):
        logger.info("Loading component configuration")
        logger.info("Loading encrypted Airflow connection data...")
        config_fid = StringIO(json.dumps(self.component_config))
        config_target = os.path.join(self.worker_component_config_path, "config.json")
        logger.info("Transferring config file %s to worker machine", config_target)
        self.worker_manager.put(config_fid, config_target)

    def clean_component(self):
        try:
            self.worker_manager.run(
                f"sed -i '/^{self.component_type}_{self.component_id}$/d' RUNNING_COMPONENTS || echo 'Already unset'"
            )
        except Exception as error:
            logger.error(error)
            logger.error("Unsetting running flag failed for worker machine")
        self.clean_component_folder()

    def clean_component_folder(self):
        try:
            self.worker_manager.run(f"sudo rm -rf '{self.worker_component_path}' || echo 'Already empty'")
        except Exception as error:
            logger.error(error)
            logger.error("Cleaning component folder from worker machine")
        try:
            self.worker_manager.run(f"sudo rm -rf '{self.worker_component_config_path}' || echo 'Already empty'")
        except Exception as error:
            logger.error(error)
            logger.error("Cleaning component config folder from worker machine")
        try:
            self.worker_manager.run(f"sudo rm -rf '{self.worker_component_data_path}' || echo 'Already empty'")
        except Exception as error:
            logger.error(error)
            logger.error("Cleaning component data folder from worker machine")
