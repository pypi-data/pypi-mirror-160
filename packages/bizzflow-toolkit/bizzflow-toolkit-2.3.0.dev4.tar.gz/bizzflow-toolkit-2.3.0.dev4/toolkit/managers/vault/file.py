"""Provides a class to access key-value storage inside of specified json file.
"""

import json
import os
from typing import List

from toolkit.managers.vault.base import BaseVaultManager


class FileVaultManager(BaseVaultManager):
    """Dummy class for credentials management testing."""

    def __init__(self, path: str):
        """FileVaultManager initializer.

        Arguments:
            path {str} -- path to temporary credentials json file
        """
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, mode="w") as fid:
                fid.write("{}")

    def get_credentials(self, key: str):
        """Get credentials for given credetials id.

        Arguments:
            key {str} -- credentials id, e.g. service account id

        Returns:
            {str} -- dictionary with credentials for given 'key' (e.g. service account id) in a form of str
        """
        with open(self.path, encoding="utf-8") as fid:
            creds = json.load(fid)
        if key not in creds:
            return None
        return creds[key]

    def list_credentials(self) -> List[str]:
        """List credential keys"""
        with open(self.path, encoding="utf-8") as fid:
            creds = json.load(fid)
        return list(creds.keys())

    def store_credentials(self, key: str, value: str):
        """Store credentials to key-value storage

        Arguments:
            key {str} -- credentials id

            value {str} -- dictionary with credentials for given 'key' (credential id) as a string

        """
        with open(self.path, encoding="utf-8") as fid:
            creds = json.load(fid)
        creds[key] = value

        with open(self.path, mode="w", encoding="utf-8") as fid:
            fid.write(json.dumps(creds))

    def delete_credential(self, key: str):
        with open(self.path, encoding="utf-8") as fid:
            creds = json.load(fid)
        creds.pop(key, None)

        with open(self.path, mode="w", encoding="utf-8") as fid:
            fid.write(json.dumps(creds))

    @classmethod
    def build_default(cls):
        return FileVaultManager("/tmp/vault.json")
