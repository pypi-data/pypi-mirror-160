import logging

from retry_helper import RetryManager

logger = logging.getLogger(__name__)

try:
    import redshift_connector
except ImportError:
    logger.info("Redshift libraries are not installed.")


class RedshiftConnectorBase:
    def __init__(self):
        self._connection = None
        self._cursor = None

    @property
    def connection(self) -> "redshift_connector.Connection":
        raise NotImplementedError

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
            exceptions=Exception,
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
                        exceptions=redshift_connector.Error,
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
                    exceptions=redshift_connector.OperationalError,
                    reset_func=self.close_cursor_and_connection,
                ) as retry:
                    while retry:
                        with retry.attempt:
                            result = cursor.fetchall()
            yield from result
        except redshift_connector.ProgrammingError:
            logger.debug(f"No result set")

    def __del__(self):
        self.close_cursor_and_connection()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_cursor()


class RedshiftConnector(RedshiftConnectorBase):
    def __init__(self, host, database, username, password):
        super().__init__()
        self._host = host
        self._database = database
        self._username = username
        self._password = password

    @property
    def connection(self):
        with RetryManager(
            max_attempts=10,
            wait_seconds=10,
            exceptions=redshift_connector.OperationalError,
        ) as retry:
            while retry:
                with retry.attempt:

                    if self._connection is None:
                        self._connection = redshift_connector.connect(
                            host=self._host,
                            database=self._database,
                            user=self._username,
                            password=self._password,
                        )
                        logger.info("Connection established")
                    return self._connection


class RedshiftConnectorIAM(RedshiftConnectorBase):
    def __init__(
        self, database, db_user, cluster_identifier, aws_access_key_id, aws_secret_access_key, session_token, region
    ):
        super().__init__()
        self._database = database
        self._db_user = db_user
        self._cluster_identifier = cluster_identifier
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._session_token = session_token
        self._region = region

    @property
    def connection(self):
        with RetryManager(
            max_attempts=10,
            wait_seconds=10,
            exceptions=redshift_connector.OperationalError,
        ) as retry:
            while retry:
                with retry.attempt:

                    if self._connection is None:
                        self._connection = redshift_connector.connect(
                            iam=True,
                            database=self._database,
                            db_user=self._db_user,
                            cluster_identifier=self._cluster_identifier,
                            access_key_id=self._aws_access_key_id,
                            secret_access_key=self._aws_secret_access_key,
                            session_token=self._session_token,
                            region=self._region,
                        )
                        logger.info("Connection established")
                    return self._connection
