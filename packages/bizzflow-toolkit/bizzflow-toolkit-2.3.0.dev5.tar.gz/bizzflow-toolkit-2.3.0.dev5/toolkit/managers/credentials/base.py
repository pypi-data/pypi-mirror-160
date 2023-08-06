"""Class for credentilas management.
Parent class for various platform credentials managers, e.g. GcpCredentialsManager.
"""
from toolkit.base.kex import Kex
from toolkit.base.table import Table


class BaseCredentialsManager:
    """Class for credentilas management.
    Parent class for various platform credentials managers, e.g. GcpCredentialsManager.

    Raises:
        NotImplementedError: If any of methods is not imlemented in the child class.
    """

    def create_kex_user(self, kex: Kex, user_name: str):
        raise NotImplementedError

    def grant_kex_permission_to_user(self, kex: Kex, user_name: str, read_only: bool = False):
        raise NotImplementedError

    def share_table_to_user(self, user_name: str, table: Table):
        """Share table based on sharing configuration"""
        raise NotImplementedError(f"{self.__class__.__name__} does not implement share_table_to_user")

    def create_sharing_user(self, user_name: str):
        """Share table based on sharing configuration"""
        raise NotImplementedError(f"{self.__class__.__name__} does not implement create_sharing_user")

    def get_user_credentials(self, user_name: str):
        raise NotImplementedError

    def delete_user(self, user_name: str):
        raise NotImplementedError

    def user_exists(self, user_name: str) -> bool:
        raise NotImplementedError
