"""Azure SQL Credentials Manager

Provides functions to manage Azure SQL storage credentials.
"""
import logging
from typing import List, Optional

from toolkit.base.kex import Kex
from toolkit.base.table import Table
from toolkit.managers.credentials.base import BaseCredentialsManager
from toolkit.managers.vault.base import BaseVaultManager
from toolkit.utils.azure_sql import AzureSQLConnector
from toolkit.utils.helpers import generate_password

logger = logging.getLogger(__name__)


class AzureSQLCredentialManager(BaseCredentialsManager):
    def __init__(self, vault_manager: BaseVaultManager, host, database, port=1433, timeout=30):
        self.vault_manager = vault_manager
        self.host = host
        self.port = port
        self.database = database

        # TODO: Move this user and password handling to configuration manager instead to have hardcoded name here
        username = "ROLE_CREATOR"
        password = self.vault_manager.get_credentials("azure-sql-ROLE_CREATOR")
        if password is None:
            logger.error("Could not find password for Azure SQL User %s", username)
            raise ValueError(f"Could not find password for Azure SQL User {username}")
        self.role_creator = self.RoleCreator(
            self.host, self.database, username, password, timeout=timeout, port=self.port
        )

        # TODO: Move this user and password handling to configuration manager instead to have hardcoded name here
        username = "ROLE_MANAGER"
        password = self.vault_manager.get_credentials("azure-sql-ROLE_MANAGER")
        if password is None:
            logger.error("Could not find password for Azure SQL User %s", username)
            raise ValueError(f"Could not find password for Azure SQL User {username}")
        self.role_manager = self.RoleManager(
            self.host, self.database, username, password, timeout=timeout, port=self.port
        )

        # TODO: Move this user and password handling to configuration manager instead to have hardcoded name here
        username = "USER_MANAGER"
        password = self.vault_manager.get_credentials("azure-sql-USER_MANAGER")
        if password is None:
            logger.error("Could not find password for Azure SQL User %s", username)
            raise ValueError(f"Could not find password for Azure SQL User {username}")
        self.user_manager = self.UserManager(
            self.host, self.database, username, password, timeout=timeout, port=self.port
        )

        # TODO: Move this user and password handling to configuration manager instead to have hardcoded name here
        username = "ORCHESTRATOR"
        role_name = "ORCHESTRATOR__role"
        password = self.vault_manager.get_credentials("azure-sql-ORCHESTRATOR")
        if password is None:
            logger.error("Could not find password for Azure SQL User %s", username)
            raise ValueError(f"Could not find password for Azure SQL User {username}")
        self.schema_manager = self.SchemaManager(
            self.host, self.database, username, password, role_name, timeout=timeout, port=self.port
        )

    def create_kex_user(self, kex: Kex, user_name: str):
        password = generate_password(24)
        role = f"{user_name}__role"
        schema = kex.kex
        self.user_manager.create_user(user_name, password, schema)
        self.vault_manager.store_credentials(user_name, password)

        self.role_creator.create_role(role)

    def create_sharing_user(self, user_name: str):
        if self.user_exists(user_name):
            logger.info(f"User {user_name} already exists, skipping")
        else:
            password = generate_password(24)
            role = f"{user_name}__role"
            self.user_manager.create_user(user_name, password)
            self.vault_manager.store_credentials(user_name, password)
            self.role_creator.create_role(role)

    def share_table_to_user(self, user_name: str, table: Table):
        role = f"{user_name}__role"
        self.schema_manager.grant_table_readonly(role, table)
        self.role_manager.grant_role(role, user_name)

    def grant_kex_permission_to_user(self, kex: Kex, user_name: str, read_only: bool = False):
        role = f"{user_name}__role"
        schema = kex.kex
        if read_only:
            self.schema_manager.grant_schema_readonly(role, schema)
        else:
            self.schema_manager.grant_schema(role, schema)
        self.role_manager.grant_role(role, user_name)

    def delete_user(self, user_name: str):
        role = f"{user_name}__role"
        self.user_manager.drop_user(user_name)
        self.role_creator.drop_role(role)
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

    class RoleCreator:
        def __init__(self, host, database, username, password, timeout=30, port=1433):
            self._connector = AzureSQLConnector(host, database, username, password, timeout=timeout, port=port)

        def create_role(self, role_name: str):
            """Create a new role

            Args:
                role_name (str): Role name
            """
            logger.info("Creating role %s", role_name)
            with self._connector:
                self._connector.execute(f"""CREATE ROLE "{role_name}";""")

        def drop_role(self, role_name: str):
            """Drop a role

            Args:
                role_name (str): Role name
            """
            logger.info("Dropping role %s", role_name)
            with self._connector:
                self._connector.execute(f"""DROP ROLE "{role_name}";""")

    class RoleManager:
        def __init__(self, host, database, username, password, timeout=30, port=1433):
            self._connector = AzureSQLConnector(host, database, username, password, timeout=timeout, port=port)

        def grant_role(self, role: str, user_name: str):
            logger.info(f"Grant role {role} to user {user_name}")
            with self._connector:
                self._connector.execute(f"""ALTER ROLE "{role}" ADD MEMBER "{user_name}";""")

    class UserManager:
        def __init__(self, host, database, username, password, timeout=30, port=1433):
            self._connector = AzureSQLConnector(host, database, username, password, timeout=timeout, port=port)

        def create_user(self, user_name: str, password: str, default_schema: Optional[str] = None):
            """Create user in database

            Args:
                user_name (str): User name to be created
                password (str): user password
                default_schema (str): default database schema
            """

            logger.info("Creating User %s", user_name)
            with self._connector:
                if default_schema:
                    self._connector.execute(
                        f"""CREATE USER "{user_name}" WITH PASSWORD = '{password}', DEFAULT_SCHEMA="{default_schema}";"""
                    )
                else:
                    self._connector.execute(f"""CREATE USER "{user_name}" WITH PASSWORD = '{password}';""")

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
                ret = self._connector.execute("SELECT name FROM sys.database_principals WHERE type_desc = 'SQL_USER'")
            return [line["name"] for line in ret]

    class SchemaManager:
        def __init__(self, host, database, username, password, role_name, timeout=30, port=1433):
            self.role_name = role_name
            self._connector = AzureSQLConnector(host, database, username, password, timeout=timeout, port=port)

        def grant_schema(self, role: str, schema: str):
            logger.info(f"Grant schema {schema} to role {role}")
            with self._connector:
                self._connector.execute(f"""GRANT CONTROL ON SCHEMA::"{schema}" TO "{role}";""")
                self._connector.execute(f"""GRANT CREATE TABLE TO "{role}" as "{self.role_name}";""")

        def grant_schema_readonly(self, role: str, schema: str):
            logger.info(f"Grant schema {schema} to role {role}")
            with self._connector:
                self._connector.execute(f"""GRANT SELECT ON SCHEMA::"{schema}" TO "{role}";""")

        def grant_table_readonly(self, role: str, table: Table):
            logger.info(f"Grant table {table} to role {role}")
            with self._connector:
                self._connector.execute(f"""GRANT SELECT ON OBJECT::"{table.kex.kex}"."{table.table}" TO "{role}";""")
