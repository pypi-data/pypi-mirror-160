"""Redshift Credentials Manager

Provides functions to manage Redshift storage credentials.
"""
import logging
from typing import List

from toolkit.base.kex import Kex
from toolkit.managers.credentials.base import BaseCredentialsManager
from toolkit.managers.vault.base import BaseVaultManager
from toolkit.utils.helpers import generate_password
from toolkit.utils.redshift_connector import RedshiftConnectorIAM

logger = logging.getLogger(__name__)


class RedshiftCredentialManager(BaseCredentialsManager):
    def __init__(
        self,
        vault_manager: BaseVaultManager,
        database,
        db_user,
        cluster_identifier,
        aws_access_key_id,
        aws_secret_access_key,
        session_token,
        region,
    ):
        self.database = database
        self.host = f"{cluster_identifier}.redshift.amazonaws.com"
        self._connector = RedshiftConnectorIAM(
            database=database,
            db_user=db_user,
            cluster_identifier=cluster_identifier,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            session_token=session_token,
            region=region,
        )

        self.vault_manager = vault_manager

    def create_kex_user(self, kex: Kex, user_name: str):
        password = generate_password(24)
        self._create_user(user_name, password)
        self.vault_manager.store_credentials(user_name, password)

    def grant_kex_permission_to_user(self, kex: Kex, user_name: str, read_only: bool = False):
        schema = kex.kex
        if read_only:
            self._grant_schema_readonly(user_name, schema)
        else:
            self._grant_schema(user_name, schema)

    def delete_user(self, user_name: str):
        self._drop_user(user_name)
        self.vault_manager.delete_credential(user_name)

    def user_exists(self, user_name: str) -> bool:
        return user_name in self._list_users()

    def get_user_credentials(self, user_name: str):
        return {
            "host": self.host,
            "database": self.database,
            "user": user_name,
            "password": self.vault_manager.get_credentials(user_name),
        }

    def _create_user(self, user_name: str, password: str):
        """Create user in database

        Args:
            user_name (str): User name to be created
            password (str): user password
        """

        logger.info("Creating User %s", user_name)
        with self._connector:
            self._connector.execute(f"""CREATE USER "{user_name}" WITH PASSWORD '{password}';""")

    def _drop_user(self, user_name: str):
        """Drop user from database

        Args:
            user_name (str): User name to be dropped
        """

        logger.info("Dropping User %s", user_name)
        with self._connector:
            self._connector.execute(f"""DROP USER IF EXISTS "{user_name}";""")

    def _list_users(self) -> List[str]:
        """Return list of users existing in the database"""
        logger.info("Listing users in db")
        with self._connector:
            ret = self._connector.execute("SELECT usename FROM pg_user;")
        return [line["usename"] for line in ret]

    def _grant_schema(self, user: str, schema: str):
        logger.info(f"Grant schema {schema} to user {user}")
        with self._connector:
            self._connector.execute(
                f"""ALTER DEFAULT PRIVILEGES IN SCHEMA "{schema}" GRANT ALL ON TABLES TO "{user}";"""
            )
            self._connector.execute(f"""GRANT ALL ON ALL TABLES IN SCHEMA "{schema}" TO "{user}";""")
            self._connector.execute(f"""GRANT ALL ON SCHEMA "{schema}" TO "{user}";""")

    def _grant_schema_readonly(self, user: str, schema: str):
        logger.info(f"Grant schema {schema} to user {user} in readonly mode")
        with self._connector:
            self._connector.execute(
                f"""ALTER DEFAULT PRIVILEGES IN SCHEMA "{schema}" GRANT SELECT ON TABLES TO "{user}";"""
            )
            self._connector.execute(f"""GRANT SELECT ON ALL TABLES IN SCHEMA "{schema}" TO "{user}";""")
            self._connector.execute(f"""GRANT USAGE ON SCHEMA "{schema}" TO "{user}";""")
