from logging import getLogger

from toolkit.managers.component.docker import BaseDockerComponentManager

logger = getLogger(__name__)


class BaseDockerBuildComponentManager(BaseDockerComponentManager):
    """
    Base class for building docker image from repository it can be download and build from git, any url or local folder
    """

    def get_docker_image(self):
        self._create_components_base_dir()
        self._docker_download()
        self._docker_build()

    def _create_components_base_dir(self):
        result = self.worker_manager.run(f"mkdir -p '{self.worker_component_path}'", warn=True)
        if not result.ok:
            raise Exception(f"Could not create components dir\n{result.stdout}\n{result.stderr}")

    def _docker_build(self):
        logger.info("Building docker image for component %s", self.component_name)
        result = self.worker_manager.run(
            f"docker build -t '{self.component_name}' '{self.worker_component_path}'", warn=True
        )
        if not result.ok:
            logger.error("Error occurred during building docker image")
            logger.error(result.stdout)
            logger.error(result.stderr)
            raise Exception("Error occurred during building docker image. See log above for more details.")
        logger.info("Docker image built successfully")

    def _docker_download(self):
        raise NotImplementedError
