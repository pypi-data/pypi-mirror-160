import logging

from toolkit.managers.component.git_docker import CannotDownloadRepositoryError, GitDockerComponentManager
from toolkit.managers.worker.base import BaseWorkerManager

logger = logging.getLogger(__name__)


class BizztreatGitLabDockerComponentManager(GitDockerComponentManager):
    def __init__(
        self,
        component_type: str,
        component_name: str,
        component_id: str,
        component_config: dict,
        worker_manager: BaseWorkerManager,
    ):
        super().__init__(component_type, component_name, component_id, component_config, worker_manager, "")
        self.bizzflow_gitlab_component_type = f"bizzflow-{self.component_type}s"

    def _docker_download(self):
        """
        Download component from git repository
        Raises:
            Exception: Repository could not cloned
        """

        # First try it with public repository and then with private one
        self.git_url = f"https://gitlab.com/{self.bizzflow_gitlab_component_type}/{self.component_name}.git"
        try:
            super(BizztreatGitLabDockerComponentManager, self)._docker_download()
        except CannotDownloadRepositoryError:
            self.git_url = f"git@gitlab.com:bizztreat/{self.component_type}/{self.component_name}.git"
            super(BizztreatGitLabDockerComponentManager, self)._docker_download()
