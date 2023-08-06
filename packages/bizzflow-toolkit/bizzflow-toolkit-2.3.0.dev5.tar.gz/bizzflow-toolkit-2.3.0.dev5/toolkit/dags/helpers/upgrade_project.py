import logging
import os

from airflow.settings import conf as airflow_conf

from toolkit import current_config
from toolkit.dags.helpers.base import PythonTaskCreator
from toolkit.managers.configuration.base import ConfigurationManager
from toolkit.managers.configuration.exceptions import ConfigurationNotValid
from toolkit.utils.git import Git, GitCommandError

logger = logging.getLogger(__name__)


class UpdateProjectTaskCreator(PythonTaskCreator):
    def __init__(self):
        super().__init__("pull_project", notify=False)

    def python_callable(self):
        """Check validity of all configurations for specific project"""
        git = Git(current_config.project_path)
        commit_hash = git.execute("rev-parse", "HEAD")

        try:
            logger.info(f"Updating project by git pull in {current_config.project_path}")
            git.execute("pull", "--ff-only", "--recurse-submodules")
        except GitCommandError as error:
            logger.error("Cannot update project - Stdout: %s\nStderr: %s", error.stdout, error.stderr)
            raise
        try:
            tmp_conf_manager = ConfigurationManager(current_config.project_path)
            tmp_conf_manager.validate()
        except ConfigurationNotValid:
            logger.error("Cannot update project - reverting last working configuration (%s)", commit_hash)
            try:
                git.execute("reset", commit_hash, "--hard")
            except GitCommandError:
                logger.error(
                    (
                        "Failed to revert commit, this is a critical error "
                        "and may result in your project being in unstable state"
                    )
                )
                raise
            raise
        finally:
            current_config.refresh()
