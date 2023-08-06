import logging
import os

from airflow import DAG

from toolkit import current_config

logger = logging.getLogger(__name__)


dags_folder = os.path.join(current_config.project_path, "dags")

try:
    custom_dags = os.listdir(dags_folder)
except FileNotFoundError:
    logger.info(f"Missing custom dags folder {dags_folder}")
else:
    for dag_file_name in custom_dags:
        if not dag_file_name.endswith(".py"):
            continue
        dag_file_path = os.path.join(dags_folder, dag_file_name)

        try:
            with open(dag_file_path) as dag_file:
                script_globals = {}
                exec(dag_file.read(), script_globals)
                for key, value in script_globals.items():
                    if isinstance(value, DAG):
                        dag_prefix = dag_file_name[:-3]
                        globals()[f"{dag_prefix}__{key}"] = value
        except Exception:
            logger.error(f"Unable to load dags from file {dag_file_path}")
            raise
