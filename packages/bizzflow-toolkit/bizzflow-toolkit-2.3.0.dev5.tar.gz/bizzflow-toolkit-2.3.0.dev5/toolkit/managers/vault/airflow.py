"""Class for Airflow credentials management.
"""

import datetime
import json
import logging
from typing import List

from airflow.models import Connection
from airflow.settings import Session

from toolkit.managers.vault.base import BaseVaultManager


class AirflowVaultManager(BaseVaultManager):
    """Class for Airflow credentials management."""

    def get_credentials(self, key: str):
        """Get password for given Airflow Connection.

        Arguments:
            key {str} -- Airflow connection id (conn_id)

        Reutrns:
            {str} -- Airflow connection password (password)
        """
        logger = logging.getLogger(__name__)
        s = Session()
        connections = list(s.query(Connection).filter(Connection.conn_id == key))
        if not connections:
            return None
        connection = connections[0]
        logger.info("Working with connection: %s", connection.conn_id)
        password = connection.password
        s.close()
        return password

    def list_credentials(self) -> List[str]:
        """Get list of credential keys available in the vault"""
        s = Session()
        connections = s.query(Connection).all()
        return [conn.conn_id for conn in connections]

    def store_credentials(self, key: str, value: str):
        """Store credentials to Airflow.
        Store credentials to Airflow, save current timestamp as connection.extra.
        If connection already exists, value is updated. If value is None, existing key is removed.

        Arguments:
            key {str} -- Airflow connection id (conn_id)

            value {str} -- Airflow connection password (password). If None, existing value is removed.
        """
        logger = logging.getLogger(__name__)
        extra = json.dumps(
            {
                "created_timestamp": datetime.datetime.now().timestamp(),
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        s = Session()
        clist = list(s.query(Connection).filter(Connection.conn_id == key))
        if clist:
            connection = clist[0]
            logger.info("Connection id: '%s' already exists, updating value.", connection.conn_id)
            # Remove key if value is None
            if value is None:
                logger.info("Deleting connection id '%s'", connection.conn_id)
                s.delete(connection)
                s.commit()
                s.close()
                return
            connection.password = value
            connection.extra = extra
        else:
            connection = Connection(conn_id=key, password=value, extra=extra)
        s.add(connection)
        s.commit()
        logger.info("Updated connection: %s", connection.conn_id)
        s.close()

    def delete_credential(self, key: str):
        self.store_credentials(key, None)

    @classmethod
    def build_default(cls):
        return AirflowVaultManager()
