"""PostgreSQL Credentials Manager

Provides functions to manage PostgreSQL storage credentials.
"""
import logging
from typing import List

from toolkit.base.kex import Kex
from toolkit.managers.credentials.base import BaseCredentialsManager
from toolkit.managers.vault.base import BaseVaultManager
from toolkit.utils.helpers import generate_password
from toolkit.utils.postre_sql import PostgreSQLConnector

logger = logging.getLogger(__name__)


class PostgreSQLCredentialManager(BaseCredentialsManager):
    def __init__(
        self,
        vault_manager: BaseVaultManager,
        host,
        database,
        user_manager_user,
        user_manager_password,
        schema_manager_user,
        schema_manager_password,
        port=5432,
        timeout=30,
    ):
        self.vault_manager = vault_manager
        self.host = host
        self.port = port
        self.database = database

        self.user_manager = self.UserManager(
            self.host,
            self.database,
            user_manager_user,
            user_manager_password,
            timeout=timeout,
            port=self.port,
            schema_manager_user=schema_manager_user,
        )
        self.schema_manager = self.SchemaManager(
            self.host, self.database, schema_manager_user, schema_manager_password, timeout=timeout, port=self.port
        )

    def create_kex_user(self, kex: Kex, user_name: str):
        password = generate_password(24)
        self.user_manager.create_user(user_name, password)
        self.vault_manager.store_credentials(user_name, password)

    def grant_kex_permission_to_user(self, kex: Kex, user_name: str, read_only: bool = False):
        schema = kex.kex
        if read_only:
            self.schema_manager.grant_schema_readonly(user_name, schema)
        else:
            self.schema_manager.grant_schema(user_name, schema)

    def delete_user(self, user_name: str):
        self.user_manager.drop_user(user_name)
        self.vault_manager.delete_credential(user_name)

    def user_exists(self, user_name: str) -> bool:
        return user_name in self.user_manager.list_users()

    def get_user_credentials(self, user_name: str):
        return {
            "database": self.database,
            "user": user_name,
            "password": self.vault_manager.get_credentials(user_name),
            "host": self.host,
            "port": self.port,
        }

    class UserManager:
        def __init__(
            self, host, database, username, password, timeout=30, port=5432, schema_manager_user="ORCHESTRATOR"
        ):
            self.schema_manager_user = schema_manager_user
            self.username = username
            self._connector = PostgreSQLConnector(host, database, username, password, timeout=timeout, port=port)

        def create_user(self, user_name: str, password: str):
            """Create user in database

            Args:
                user_name (str): User name to be created
                password (str): user password
            """

            logger.info("Creating User %s", user_name)
            with self._connector:
                self._connector.execute(
                    f"""CREATE USER "{user_name}" WITH ADMIN "{self.username}", "{self.schema_manager_user}" PASSWORD '{password}';"""
                )

        def drop_user(self, user_name: str):
            """Drop user from database

            Args:
                user_name (str): User name to be dropped
            """

            logger.info("Dropping User %s", user_name)
            with self._connector:
                self._connector.execute(f"""DROP USER IF EXISTS "{user_name}";""")

        def list_users(self) -> List[str]:
            """Return list of users existing in the database"""
            logger.info("Listing users in db")
            with self._connector:
                ret = self._connector.execute("SELECT usename FROM pg_user;")
            return [line["usename"] for line in ret]

    class SchemaManager:
        def __init__(self, host, database, username, password, timeout=30, port=5432, user_manager_user="USER_MANAGER"):
            self.user_manager_user = user_manager_user
            self.username = username
            self._connector = PostgreSQLConnector(host, database, username, password, timeout=timeout, port=port)

        def grant_schema(self, user: str, schema: str):
            logger.info(f"Grant schema {schema} to user {user}")
            with self._connector:
                self._connector.execute(
                    f"""ALTER DEFAULT PRIVILEGES IN SCHEMA "{schema}" GRANT ALL ON TABLES TO "{user}";"""
                )
                self._connector.execute(f"""GRANT ALL ON ALL TABLES IN SCHEMA "{schema}" TO "{user}";""")
                self._connector.execute(f"""GRANT CREATE ON SCHEMA "{schema}" TO "{user}";""")
                self._connector.execute(f"""GRANT USAGE ON SCHEMA "{schema}" TO "{user}";""")
                # Make sure tables not created by ORCHESTRATOR within the schema are granted to ORCHESTRATOR as well.
                # This is a workaround as there is no way to grant future schemas in postgresql, only future tables
                # within existing schemas.
                # TODO: Please review, this seems too complicated to be the only way.
                self._connector.execute(f"""GRANT "{user}" TO "{self.username}";""")
                self._connector.execute(f"""GRANT "{user}" TO "{self.user_manager_user}";""")
                self._connector.execute(
                    f"""ALTER DEFAULT PRIVILEGES FOR ROLE "{user}" IN SCHEMA "{schema}" GRANT ALL ON TABLES TO "{self.username}";"""
                )

        def grant_schema_readonly(self, user: str, schema: str):
            logger.info(f"Grant schema {schema} to user {user} in readonly mode")
            with self._connector:
                self._connector.execute(
                    f"""ALTER DEFAULT PRIVILEGES IN SCHEMA "{schema}" GRANT SELECT ON TABLES TO "{user}";"""
                )
                self._connector.execute(f"""GRANT SELECT ON ALL TABLES IN SCHEMA "{schema}" TO "{user}";""")
                self._connector.execute(f"""GRANT USAGE ON SCHEMA "{schema}" TO "{user}";""")
