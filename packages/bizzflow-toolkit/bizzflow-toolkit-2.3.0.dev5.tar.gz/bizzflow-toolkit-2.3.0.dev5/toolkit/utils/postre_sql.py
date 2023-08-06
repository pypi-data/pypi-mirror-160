from toolkit.utils.odbc_connector import PyODBCSQLConnector


class PostgreSQLConnector(PyODBCSQLConnector):
    driver = "{PostgreSQL Unicode};"
    default_port = 5432
    connection_string_format = (
        "Driver={driver};Server={host};Port={port};Database={database};Uid={username};Pwd={password};"
    )
