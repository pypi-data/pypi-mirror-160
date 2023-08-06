"""Class for vault management.
Parent class for various platform vault managers, e.g. AirflowVaultManager.
"""

import os
from base64 import b64encode
from typing import List


class BaseVaultManager:
    """Class for vault management.
    Parent class for various platform vault managers, e.g. AirflowVaultManager.

    Raises:
        NotImplementedError: If any of methods is not imlemented in the child class.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_credentials(self, *args, **kwargs):
        """Get credentials."""
        raise NotImplementedError("This method must be overriden.")

    def store_credentials(self, *args, **kwargs):
        """Store credentials."""
        raise NotImplementedError("This method must be overriden.")

    def delete_credential(self, key: str):
        """Delete credentials."""
        raise NotImplementedError("This method must be overridden.")

    def list_credentials(self) -> List[str]:
        """Get list of credential keys available in the vault"""
        raise NotImplementedError("This method must be overridden.")

    @classmethod
    def build_default(cls):
        """Create default instance of a Vault Manager"""
        raise NotImplementedError("This method must be overriden.")

    @classmethod
    def generate_password(cls, minlength=24):
        """Generate password string of at least {minleght} characters

        Args:
            length (int, optional): Password length. Defaults to 24.
        """
        return b64encode(os.urandom(minlength)).decode("ascii")
