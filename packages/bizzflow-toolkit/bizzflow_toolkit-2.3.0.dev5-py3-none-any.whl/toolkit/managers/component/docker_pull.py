from logging import getLogger

from toolkit.managers.component.docker import BaseDockerComponentManager
from toolkit.managers.worker.base import BaseWorkerManager

logger = getLogger(__name__)


class DockerComponentManager(BaseDockerComponentManager):
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
        docker_registry: str,
        docker_image: str,
        docker_registry_username: str,
        docker_registry_password: str,
    ):
        super().__init__(component_type, component_name, component_id, component_config, worker_manager)
        self.docker_registry = docker_registry
        self.docker_image = docker_image
        self.docker_registry_username = docker_registry_username
        self.docker_registry_password = docker_registry_password
        self.use_docker_login = bool(self.docker_registry_username and self.docker_registry_password)

    def _docker_login(self):
        if self.docker_registry_username and self.docker_registry_password:
            logger.info("Login to docker repository")
            result = self.worker_manager.run(
                f"docker login {self.docker_registry} -u {self.docker_registry_username} -p {self.docker_registry_password}",
                show_command_in_logs=False,
                warn=True,
            )
            if not result.ok:
                logger.error("Error occurred during docker login")
                raise Exception("Error occurred during docker login. See log above for more details.")
            logger.info("Docker login successfully")

    def _pull_docker_image(self):
        logger.info("Pull docker image for component %s", self.docker_image)
        result = self.worker_manager.run(f"docker pull '{self.docker_image}'", warn=True)
        if not result.ok:
            logger.error("Error occurred during pull docker image")
            logger.error(result.stdout)
            logger.error(result.stderr)
            raise Exception("Error occurred during pull image. See log above for more details.")
        result = self.worker_manager.run(f"docker tag '{self.docker_image}' '{self.component_name}'", warn=True)
        if not result.ok:
            logger.error("Error occurred during tagging docker image")
            logger.error(result.stdout)
            logger.error(result.stderr)
            raise Exception("Error occurred during tagging image. See log above for more details.")
        logger.info("Docker image pull successfully")

    def get_docker_image(self):
        if self.use_docker_login:
            self._docker_login()
        self._pull_docker_image()
