import os
from glob import glob
from logging import getLogger
from typing import Optional

import sqlparse

from toolkit.managers.component.base import BaseComponentManager

logger = getLogger(__name__)


class SQLTransformationComponentManager(BaseComponentManager):
    def __init__(self, component_id: str, component_name, query_timeout: int):
        super().__init__("transformation", component_name, component_id, {})
        self.query_timeout = query_timeout

    def get_queries(self, skip_files: Optional[list] = None):
        raise NotImplementedError


class BlankTransformationSQLComponentManager(SQLTransformationComponentManager):
    def __init__(self):
        super().__init__("blank_sql", "blank_sql", 0)

    def get_queries(self, skip_files: Optional[list] = None):
        logger.info("No queries to run")


class LocalSQLTransformationComponentManager(SQLTransformationComponentManager):
    def __init__(self, transformation_id: str, transformation_name, query_timeout: int, sql_folder_path: str):
        super().__init__(transformation_id, transformation_name, query_timeout)
        self.sql_folder_path = sql_folder_path.encode()

    def _get_sql_files(self):
        search_path = os.path.join(self.sql_folder_path, b"*.sql")
        logger.info("SQL files should be in %s", search_path)
        return sorted(glob(search_path))

    def get_queries(self, skip_files: Optional[list] = None):
        skip_files = skip_files or []
        for file_name in self._get_sql_files():
            if os.path.split(file_name)[1] in skip_files:
                logger.warning(f"Skipping {file_name}")
                continue
            with open(file_name, "r", encoding="utf-8") as fid:
                logger.info("reading script: %s", file_name)
                sql = fid.read()

                sql_lines = sql.split("\n")
                output_lines = []
                for line in sql_lines:
                    if line.strip().startswith("--"):
                        continue
                    if line.strip() == "":
                        continue
                    else:
                        output_lines.append(line)
                sql = "\n".join(output_lines)

                query_list = sqlparse.parse(sql)
                for query_n, statement in enumerate(query_list):
                    if statement.get_type() == "UNKNOWN":
                        if statement.token_first().value.upper() not in (
                            "WITH",
                            "SET",
                        ):
                            logger.warning("Skipping UNKNOWN query\n%s", statement.value)
                            continue
                    query = statement.value
                    if not query.strip():
                        logger.info("Skipping empty query")
                        continue
                    logger.info("sql query: %s", query)
                    yield query
                    logger.info("query: #%d/%d successfully done!", query_n + 1, len(query_list))
            logger.info("script: %s successfully done!", file_name)
