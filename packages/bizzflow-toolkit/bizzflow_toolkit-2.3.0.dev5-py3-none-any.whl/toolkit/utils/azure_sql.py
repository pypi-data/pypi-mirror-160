import logging

from toolkit.utils.odbc_connector import PyODBCSQLConnector

logger = logging.getLogger(__name__)


class AzureSQLConnector(PyODBCSQLConnector):
    driver = "{ODBC Driver 17 for SQL Server}"
    default_port = 1433
    connection_string_format = "Driver={driver};Server=tcp:{host},{port};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout={timeout};"
