import logging
import urllib.parse
from typing import Optional

import invoke
from retry_helper import RetryManager

from toolkit.managers.component.docker_build import BaseDockerBuildComponentManager
from toolkit.managers.worker.base import BaseWorkerManager

logger = logging.getLogger(__name__)


class CannotDownloadRepositoryError(Exception):
    pass


class GitDockerComponentManager(BaseDockerBuildComponentManager):
    def __init__(
        self,
        component_type: str,
        component_name: str,
        component_id: str,
        component_config: dict,
        worker_manager: BaseWorkerManager,
        git_repository: str,
        git_checkout: Optional[str] = None,
        git_username: Optional[str] = None,
        git_password: Optional[str] = None,
    ):
        super().__init__(component_type, component_name, component_id, component_config, worker_manager)
        self.git_checkout = git_checkout
        self.use_git_login = bool(git_username and git_password)
        self.git_url = self._join_url_with_login(git_repository, git_username, git_password)

    def _join_url_with_login(self, url, username=None, password=None):
        if username is None or password is None:
            return url
        split_result = urllib.parse.urlsplit(url)
        username = username or split_result.username
        password = password or split_result.password
        if username and password:
            netloc = f"{username}:{password}@"
        else:
            netloc = ""
        netloc = f"{netloc}{split_result.hostname}"
        if split_result.port:
            netloc = f"{netloc}:{split_result.port}"
        return urllib.parse.urlunsplit(
            (split_result.scheme, netloc, split_result.path, split_result.query, split_result.fragment)
        )

    @RetryManager(
        max_attempts=10,
        wait_seconds=5,
        exceptions=(CannotDownloadRepositoryError,),
    )
    def _docker_download(self):
        """
        Download component from git repository
        Raises:
            Exception: Repository could not cloned
        """
        logger.info("Downloading component %s", self.component_name)
        try:
            self.worker_manager.run(
                f"git clone '{self.git_url}' '{self.worker_component_path}'",
                show_command_in_logs=(not self.use_git_login),
                hide=True,
            )
            if self.git_checkout:
                self.worker_manager.run(
                    f"cd '{self.worker_component_path}' && git checkout {self.git_checkout}", hide=True
                )
        except invoke.UnexpectedExit as e:
            raise CannotDownloadRepositoryError(
                f"Error cloning {self.component_type} repository '{self.component_name}'"
            ) from e
        else:
            logger.info("Repository successfully cloned")
