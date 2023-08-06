"""Class for Snowflake account/user credentials management.
"""

import logging

import toolkit.utils.helpers
from toolkit.base.kex import Kex
from toolkit.managers.credentials.base import BaseCredentialsManager
from toolkit.managers.vault.base import BaseVaultManager

logger = logging.getLogger(__name__)
try:
    from snowflake.connector import SnowflakeConnection
except ImportError:
    logger.info("Snowflake support are not installed.")


class SnowflakeCredentialsManager(BaseCredentialsManager):
    """Class for Snowflake account/user credentials management."""

    def __init__(self, vault_manager: BaseVaultManager, account, warehouse, database):
        self.vault_manager = vault_manager
        self.account = account
        self.warehouse = warehouse
        self.database = database

        # TODO: Move this user and password handling to configuration manager instead to have hardcoded name here
        username = "ROLE_CREATOR"
        password = self.vault_manager.get_credentials("snowflake-ROLE_CREATOR")
        if password is None:
            logger.error("Could not find password for Snowflake User %s", username)
            raise ValueError(f"Could not find password for Snowflake SQL User {username}")
        self.role_creator = self.RoleCreator(self.account, self.warehouse, self.database, username, password)

        # TODO: Move this user and password handling to configuration manager instead to have hardcoded name here
        username = "ROLE_MANAGER"
        password = self.vault_manager.get_credentials("snowflake-ROLE_MANAGER")
        if password is None:
            logger.error("Could not find password for Snowflake User %s", username)
            raise ValueError(f"Could not find password for Snowflake User {username}")
        self.role_manager = self.RoleManager(self.account, self.warehouse, self.database, username, password)

        # TODO: Move this user and password handling to configuration manager instead to have hardcoded name here
        username = "USER_MANAGER"
        password = self.vault_manager.get_credentials("snowflake-USER_MANAGER")
        if password is None:
            logger.error("Could not find password for Snowflake User %s", username)
            raise ValueError(f"Could not find password for Snowflake User {username}")
        self.user_manager = self.UserManager(self.account, self.warehouse, self.database, username, password)

    def user_exists(self, user_name: str) -> bool:
        return user_name in self.role_manager.show_users()

    def delete_user(self, user_name: str):
        self.user_manager.drop_user(user_name)
        self.role_manager.drop_role(user_name)
        self.vault_manager.delete_credential(user_name)

    def create_kex_user(self, kex: Kex, user_name: str):
        """Create sandbox user and grant it access to its sandbox schema.
        User name is guessed from schema_name, if you need to override this behavior, you can pass optional user name parameter.
        The new user's password will be stored in project's vault using VaultManager.

        Args:
            kex: sandbox kex
            user_name (str, optional): Name of the user to be created (guessed from sandbox_kex by default)
        """
        schema_name = kex.kex
        user_name = user_name or schema_name
        self.role_creator.create_role(user_name)
        password = toolkit.utils.helpers.generate_password(24)
        self.user_manager.create_user(
            user_name=user_name, password=password, default_schema=schema_name, default_role=user_name
        )
        self.role_manager.grant_role(user_name, user_name)
        self.vault_manager.store_credentials(user_name, password)

    def grant_kex_permission_to_user(self, kex: Kex, user_name: str, read_only: bool = False):
        """Re-grants sandbox user access to its sandbox schema.

        Args:
            kex: sandbox kex
            user_name (str, optional): Name of the user to be created (guessed from sandbox_kex by default)
        """
        schema_name = kex.kex
        user_name = user_name or schema_name
        self.role_manager.grant_warehouse(role=user_name)
        self.role_manager.grant_database(role=user_name)
        if read_only:
            self.role_manager.grant_schema_usage(schema=schema_name, role=user_name)
            self.role_manager.grant_select_schema_tables(schema=schema_name, role=user_name)
            self.role_manager.grant_select_schema_tables_future(schema=schema_name, role=user_name)
        else:
            self.role_manager.grant_schema(schema=schema_name, role=user_name)
            self.role_manager.grant_schema_tables_ownership(schema=schema_name, role=user_name)
            self.role_manager.grant_schema_tables(schema=schema_name, role=user_name)
            self.role_manager.grant_schema_tables_future(schema=schema_name, role=user_name)

    def get_user_credentials(self, user_name: str):
        """Return sandbox credentials for specified kex.

        Args:
            sandbox_name ([str, Kex]): Sandbox name or Sandbox kex instance
        """
        return {
            "database": self.database,
            "warehouse": self.warehouse,
            "account": self.account,
            "user": user_name,
            "password": self.vault_manager.get_credentials(user_name),
            "url": "https://{}.snowflakecomputing.com".format(self.account),
        }

    class RoleCreator:
        def __init__(self, account, warehouse, database, username, password):
            self.snf_connection = SnowflakeConnection(
                user=username,
                password=password,
                account=account,
                warehouse=warehouse,
                database=database,
                client_session_keep_alive=True,
            )

        def create_role(self, role_name: str):
            """Create a new role

            Args:
                role_name (str): Role name
            """
            logger.info("Creating role %s", role_name)
            cur = self.snf_connection.cursor()
            cur.execute(f"""CREATE ROLE "{role_name}";""")

    class RoleManager:
        def __init__(self, account, warehouse, database, username, password, role=None):
            self.warehouse = warehouse
            self.database = database
            self.role_name = role or f"{username}_ROLE"
            self.snf_connection = SnowflakeConnection(
                user=username,
                password=password,
                account=account,
                warehouse=warehouse,
                database=database,
                client_session_keep_alive=True,
            )

        def drop_role(self, role_name: str):
            """Drop a role

            Args:
                role_name (str): Role name
            """
            # Dropping role with future privilege require role with MANAGE GRANTS privilege so this method is part of
            # RoleManger instead of RoleCreator
            logger.info("Dropping role %s", role_name)
            cur = self.snf_connection.cursor()
            cur.execute(f"""GRANT OWNERSHIP ON ROLE "{role_name}" TO ROLE "{self.role_name}";""")
            cur.execute(f"""DROP ROLE "{role_name}";""")

        def grant_role(self, role: str, user_name: str):
            logger.info(f"Grant role {role} to user {user_name}")
            cur = self.snf_connection.cursor()
            cur.execute(f"""GRANT ROLE "{role}" TO USER "{user_name}";""")

        def show_users(self):
            # TODO: this probably should be in UserManager but previously it was called as ROLE_MANAGER
            cur = self.snf_connection.cursor()
            result = cur.execute("""SHOW USERS;""")
            users = [line[0] for line in result.fetchall()]
            return users

        def grant_warehouse(self, role: str):
            cur = self.snf_connection.cursor()
            cur.execute(f"""GRANT USAGE ON WAREHOUSE "{self.warehouse}" TO ROLE "{role}";""")

        def grant_database(self, role):
            cur = self.snf_connection.cursor()
            cur.execute(f"""GRANT USAGE ON DATABASE "{self.database}" TO ROLE "{role}";""")

        def grant_schema_tables_ownership(self, schema, role):
            cur = self.snf_connection.cursor()
            cur.execute(
                f"""GRANT OWNERSHIP ON ALL TABLES IN SCHEMA "{self.database}"."{schema}" TO ROLE "{role}" REVOKE CURRENT GRANTS"""
            )

        def grant_schema_tables(self, schema, role):
            cur = self.snf_connection.cursor()
            cur.execute(
                f"""GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "{self.database}"."{schema}" TO ROLE "{role}" """
            )

        def grant_schema_tables_future(self, schema, role):
            cur = self.snf_connection.cursor()
            cur.execute(
                f"""GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA "{self.database}"."{schema}" TO ROLE "{role}" """
            )

        def grant_schema(self, schema, role):
            cur = self.snf_connection.cursor()
            cur.execute(f"""GRANT ALL PRIVILEGES ON SCHEMA "{self.database}"."{schema}" TO ROLE "{role}" """)

        def grant_schema_usage(self, schema, role):
            cur = self.snf_connection.cursor()
            cur.execute(f"""GRANT USAGE ON SCHEMA "{self.database}"."{schema}" TO ROLE "{role}" """)

        def grant_select_schema_tables(self, schema, role):
            cur = self.snf_connection.cursor()
            cur.execute(f"""GRANT SELECT ON ALL TABLES IN SCHEMA "{self.database}"."{schema}" TO ROLE "{role}" """)

        def grant_select_schema_tables_future(self, schema, role):
            cur = self.snf_connection.cursor()
            cur.execute(f"""GRANT SELECT ON FUTURE TABLES IN SCHEMA "{self.database}"."{schema}" TO ROLE "{role}" """)

    class UserManager:
        def __init__(self, account, warehouse, database, username, password):
            self.warehouse = warehouse
            self.database = database
            self.snf_connection = SnowflakeConnection(
                user=username,
                password=password,
                account=account,
                warehouse=warehouse,
                database=database,
                client_session_keep_alive=True,
            )

        def create_user(self, user_name: str, password: str, default_schema: str, default_role: str):
            """Create user in database

            Args:
                user_name (str): User name to be created
                password (str): user password
                default_schema (str): default database schema
                default_role (str): default role
            """

            logger.info("Creating User %s", user_name)
            cur = self.snf_connection.cursor()
            cur.execute(
                f"""CREATE USER "{user_name}"
                PASSWORD = '{password}'
                LOGIN_NAME = '{user_name}'
                DISPLAY_NAME = '{user_name}'
                MUST_CHANGE_PASSWORD = FALSE
                DEFAULT_WAREHOUSE = '{self.warehouse}'
                DEFAULT_NAMESPACE = "{self.database}"."{default_schema}"
                DEFAULT_ROLE = '{default_role}'"""
            )

        def drop_user(self, user_name: str):
            """Drop user from database

            Args:
                user_name (str): User name to be dropped
            """

            logger.info("Dropping User %s", user_name)
            cur = self.snf_connection.cursor()
            cur.execute(f"""DROP USER "{user_name}";""")
