import logging

from airflow import DAG
from airflow.settings import conf as airflow_conf

from toolkit import current_config
from toolkit.dags.helpers.base import StopWorkerTaskCreator, TaskGenerator
from toolkit.dags.helpers.datamarts import DatamartTaskCreator
from toolkit.dags.helpers.extractors import ExtractorTaskCreator
from toolkit.executors.extractor import DockerExtractorExecutor
from toolkit.managers.component.docker_pull import DockerComponentManager
from toolkit.managers.datamart import DatamartManager

logger = logging.getLogger(__name__)


class TelemetryOrchestrationTaskGenerator(TaskGenerator):
    def generate(self, dag: DAG):
        extractor = TelemetryExtractorTaskCreator().create(dag)
        datamart = TelemetryDatamartTaskCreator().create(dag)
        stop_worker_task = StopWorkerTaskCreator().create(dag)
        extractor >> datamart >> stop_worker_task


class TelemetryExtractorTaskCreator(ExtractorTaskCreator):
    def __init__(self, **kwargs) -> None:
        super().__init__("bizzflow_telemetry", **kwargs)

    def python_callable(self):
        extractor_executor = self.get_extractor_executor()
        try:
            extractor_executor.create_environment()
            extractor_executor.run()
            extractor_executor.create_output_mapping()
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise
        finally:
            extractor_executor.clean_environment()

    def get_extractor_executor(self):
        worker_manager = current_config.loader.get_worker_manager()
        username, password, host, database = self.parse_sql_alchemy_conn()
        component_manager = DockerComponentManager(
            component_type="extractor",
            component_name="ex-postgres",
            component_id="bizzflow_telemetry",
            component_config={
                "user": username,
                "password": password,
                "host": host,
                "database": database,
                "query": {
                    "task_instance": """SELECT
task_id, dag_id, execution_date, start_date, end_date, duration, state, try_number, hostname, unixname, job_id, pool,
queue, priority_weight, operator, queued_dttm, pid, max_tries, executor_config, pool_slots 
                                                    FROM task_instance""",
                    "users": """SELECT 
                                id, username, email, superuser 
                                            FROM users""",
                    "ab_users": """SELECT
                                id, first_name, last_name, username, active, email, last_login, login_count,
                                fail_login_count, created_on, changed_on, created_by_fk, changed_by_fk 
                                                FROM ab_user""",
                    "dag": """SELECT
dag_id, is_paused, is_subdag, is_active, last_scheduler_run, last_pickled, last_expired, scheduler_lock, pickle_id,
fileloc, owners, description, default_view, schedule_interval, root_dag_id 
                                            FROM dag""",
                    "dag_run": """SELECT
                                id, dag_id, execution_date, state, run_id, external_trigger, conf, end_date, start_date 
                                                FROM dag_run""",
                },
            },
            worker_manager=worker_manager,
            docker_registry="registry.gitlab.com",
            docker_image="registry.gitlab.com/bizzflow-extractors/ex-postgres:latest",
            docker_registry_username="",
            docker_registry_password="",
        )
        file_storage_manager = current_config.loader.get_file_storage_manager(
            prefix=component_manager.component_relative_path
        )

        return DockerExtractorExecutor(
            storage_manager=current_config.loader.get_storage_manager(),
            worker_manager=worker_manager,
            file_storage_manager=file_storage_manager,
            component_manager=component_manager,
            step=current_config.loader.get_step(),
        )

    @staticmethod
    def parse_sql_alchemy_conn():
        sql_alchemy_conn = airflow_conf.get("core", "sql_alchemy_conn")
        # e.g. postgresql+psycopg2://username:password@host:port/database
        _, after_double_slash = sql_alchemy_conn.split("://")
        # e.g. postgresql+psycopg2, username:password@host:port/database
        username, after_colon = after_double_slash.split(":", 1)
        # e.g. username, password@host:port/database
        password, after_at_sign = after_colon.split("@", 1)
        # e.g. password, host:port/database
        host_port, database = after_at_sign.split("/", 1)
        # e.g. host:port, database
        host = host_port.split(":", 1)[0]
        logger.debug(f"Bizzflow telemetry extractor connection: username:{username}, host:{host}, database:{database}")
        return username, password, host, database


class TelemetryDatamartTaskCreator(DatamartTaskCreator):
    def __init__(self, **kwargs) -> None:
        super().__init__("bizzflow_telemetry", **kwargs)

    def python_callable(self):
        datamart_manager = DatamartManager(
            storage_manager=current_config.loader.get_storage_manager(),
            credentials_manager=current_config.loader.get_credentials_manager(),
            out_kex="in_ex_postgres_bizzflow_telemetry",
            dm_kex="dm_bizzflow_telemetry",
            allowed_tables=None,
        )
        datamart_manager.create_environment()
        datamart_manager.get_credentials()
        datamart_manager.write()
