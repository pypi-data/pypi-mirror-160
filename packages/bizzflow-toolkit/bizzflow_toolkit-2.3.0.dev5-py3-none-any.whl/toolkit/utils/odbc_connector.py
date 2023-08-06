import logging

from retry_helper import RetryManager

logger = logging.getLogger(__name__)

try:
    import pyodbc
except ImportError:
    logger.info("PyODBC libraries are not installed, install azure or onprem extras.")


class PyODBCSQLConnector:
    driver = NotImplemented
    default_port = NotImplemented
    connection_string_format: str = NotImplemented

    def __init__(self, host, database, username, password, timeout=30, port=None):
        self._connection = None
        self._cursor = None
        port = port or self.default_port
        self.connection_string = self.get_connection_string(host, port, database, username, password, timeout)

    def get_connection_string(self, host, port, database, username, password, timeout, **kwargs):
        if self.connection_string_format is NotImplemented:
            raise NotImplementedError(f"{self.__class__.__name__} does not implement connection")
        return self.connection_string_format.format(
            driver=self.driver,
            host=host,
            port=port,
            database=database,
            username=username,
            password=password,
            timeout=timeout,
            **kwargs,
        )

    @property
    def connection(self):
        with RetryManager(
            max_attempts=10,
            wait_seconds=10,
            exceptions=pyodbc.Error,
        ) as retry:
            while retry:
                with retry.attempt:
                    if self._connection is None:
                        self._connection = pyodbc.connect(self.connection_string, autocommit=True)
                        # Set connection-wide transaction isolation level based on this issue:
                        # https://github.com/mkleehammer/pyodbc/issues/135
                        self._connection.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
                        logger.info("Connection established")
                    return self._connection

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.connection.cursor()
            logger.debug("Creating cursor")
        return self._cursor

    def close_cursor(self):
        if self._cursor:
            self._cursor.close()
            logger.debug("Cursor closed")
            self._cursor = None

    def close_cursor_and_connection(self):
        self.close_cursor()
        if self._connection:
            self._connection.close()
            self._connection = None
        logger.info("Connection closed")

    def _execute(self, query):
        logger.debug(f'Execute query "{query}"')
        with RetryManager(
            max_attempts=3,
            wait_seconds=5,
            exceptions=pyodbc.OperationalError,
            reset_func=self.close_cursor_and_connection,
        ) as retry:
            while retry:
                with retry.attempt:
                    cursor = self.cursor.execute(query)
            return cursor

    def execute(self, query, generator=False, chunk_size=None):
        """Execute and return result as list (or generator) of dicts"""
        try:
            cursor = self._execute(query)
        except Exception:
            logger.error(f"An error occur when execute query. '''{query}'''")
            raise
        # non-select query
        if cursor.description is None:
            return
        columns = [info[0] for info in cursor.description]
        gen = (
            {column: line[cid] for cid, column in enumerate(columns)}
            for line in self._generate_result(cursor, chunk_size)
        )
        if generator:
            return gen
        return list(gen)

    def _generate_result(self, cursor, chunk_size=None):
        try:
            if chunk_size:
                while True:
                    with RetryManager(
                        max_attempts=3,
                        wait_seconds=5,
                        exceptions=pyodbc.OperationalError,
                        reset_func=self.close_cursor_and_connection,
                    ) as retry:
                        while retry:
                            with retry.attempt:
                                result = cursor.fetchmany(chunk_size)
                    if result:
                        yield from result
                    else:
                        break
            else:
                with RetryManager(
                    max_attempts=3,
                    wait_seconds=5,
                    exceptions=pyodbc.OperationalError,
                    reset_func=self.close_cursor_and_connection,
                ) as retry:
                    while retry:
                        with retry.attempt:
                            result = cursor.fetchall()
            yield from result
        except pyodbc.ProgrammingError:
            logger.debug(f"No result set")

    def __del__(self):
        self.close_cursor_and_connection()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_cursor()
