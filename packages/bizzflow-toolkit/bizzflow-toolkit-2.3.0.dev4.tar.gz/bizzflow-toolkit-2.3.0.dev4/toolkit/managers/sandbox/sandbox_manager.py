"""Class for sandbox management.
Parent class for abstract sandbox managers of various types, e.g SqlSandboxManager.
"""
import logging
from typing import Optional, Union

from toolkit.base.kex import Kex
from toolkit.executors.transformation.base_sql import SqlTransformationExecutor
from toolkit.executors.transformation.docker import DockerTransformationExecutor

logger = logging.getLogger(__name__)


class SandboxManager:
    """Class for sandbox management.
    Parent class for abstract sandbox managers of various types, e.g SqlSandboxManager.

    Raises:
        NotImplementedError: If any of methods is not imlemented in the child class.
    """

    def __init__(
        self,
        sandbox_user_email: str,
        transformation_executor: Union[SqlTransformationExecutor, DockerTransformationExecutor],
    ):
        self.transformation_executor = transformation_executor
        self.sandbox_name = self.sandbox_from_email(sandbox_user_email)
        self.transformation_executor.working_kex = Kex(self.sandbox_name)
        self.transformation_executor.transformation_user = self.sandbox_name

    def create_sandbox(self, *args, **kwargs):
        """Provisioning.
        Create sandbox environment.
        """
        self.transformation_executor.create_environment()

    def load(
        self,
        load_transformation=True,
        additional_kexes: Optional[list] = None,
        additional_tables: Optional[list] = None,
    ):
        """Load fresh sandbox.
        Switch transformation kex to sandbox kex.
        Delete all the tables present in sandbox.
        Perform transformation executor input_mapping().
        Switch back to original transformation kex.
        """

        if load_transformation:
            self.transformation_executor.create_input_mapping()
        if additional_kexes or additional_tables:
            self.transformation_executor.create_input_mapping([*additional_kexes, *additional_tables])

    def dry_run(self, **options):
        """Perform dry run.
        Run transformation without output mapping.
        """
        self.transformation_executor.run(**options)

    def clean_sandbox(self):
        """Clean all existing tables from the sandbox"""
        logger.info("Dropping tables from the sandbox")
        table_list = self.transformation_executor.storage_manager.list_tables(self.transformation_executor.working_kex)
        for t in table_list:
            self.transformation_executor.storage_manager.delete_table(t)
        logger.info(f"Sandbox {self.sandbox_name} should be empty now")

    def destroy_sandbox(self):
        self.transformation_executor.clean_environment()

    def sandbox_from_email(self, email: str):
        """Get sandbox name from user's email
        E.g.: tomas.votava@bizztreat.com => dev_tomvot

        Args:
            email (str): User's e-mail
        """
        if "@" not in email:
            raise ValueError("Input must contain @ character")
        base = email.split("@")[0]
        first_name = base.split(".")[0]
        rest = "".join(base.split(".")[1:])
        sandbox_name = "dev_{a}{b}".format(a=first_name[:3], b=rest[:3])
        return self.transformation_executor.storage_manager.normalize_string(sandbox_name)
