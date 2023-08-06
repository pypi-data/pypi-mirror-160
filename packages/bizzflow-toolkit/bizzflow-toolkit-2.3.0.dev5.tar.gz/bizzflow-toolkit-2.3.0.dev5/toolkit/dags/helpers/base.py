import logging
from abc import ABC
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import BaseOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

from toolkit import current_config
from toolkit.dags.helpers.pools import PoolCreator
from toolkit.dags.helpers.utils import notify_email
from toolkit.utils.stopwatch import stopwatch

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 36000


class BaseTaskCreator(ABC):
    operator_class = BaseOperator

    def __init__(self, task_id: str, **kwargs) -> None:
        self.task_id = task_id
        params = {}
        notify = kwargs.pop("notify", None)
        continue_on_error = kwargs.pop("continue_on_error", False)
        task_type = kwargs.pop("task_type", None)
        if notify is not None:
            params["notify"] = notify
        if task_type is not None:
            params["task_type"] = task_type
        params["continue_on_error"] = continue_on_error
        timeout = kwargs.pop("timeout", DEFAULT_TIMEOUT) or DEFAULT_TIMEOUT
        try:
            timeout = int(timeout)
        except ValueError as error:
            raise ValueError(
                f"'timeout' parameter must be a valid integer, got '{timeout}' for task '{task_id}'"
            ) from error
        if timeout == -1:
            # no timeout
            execution_timeout = None
        elif timeout < 0:
            logger.warning(
                "Invalid timeout parameter value %d (must be -1, unset or positive) for task '%s'. Using default %d s",
                timeout,
                task_id,
                DEFAULT_TIMEOUT,
            )
            execution_timeout = timedelta(seconds=DEFAULT_TIMEOUT)
        else:
            execution_timeout = timedelta(seconds=timeout)
            logger.info("Task %s's timeout is set to %d s", task_id, timeout)
        kwargs["execution_timeout"] = execution_timeout
        kwargs["params"] = params
        self.kwargs = kwargs
        self.kwargs["on_failure_callback"] = self.on_failure_callback = kwargs.get("on_failure_callback", notify_email)
        PoolCreator().create_pool_if_not_exists(task_id)
        self.kwargs["pool"] = self.task_id

    def get_operator_class(self):
        return self.operator_class

    def get_operator_kwargs(self):
        return self.kwargs

    def create(self, dag) -> get_operator_class:
        Operator = self.get_operator_class()
        return Operator(task_id=self.task_id, dag=dag, **self.get_operator_kwargs())


class BashTaskCreator(BaseTaskCreator):
    operator_class = BashOperator

    def __init__(self, task_id: str, **kwargs) -> None:
        super().__init__(task_id, **kwargs)

    def get_operator_kwargs(self):
        kwargs = super().get_operator_kwargs()
        kwargs["bash_command"] = self.bash_command
        return kwargs

    @property
    def bash_command(self) -> str:
        raise NotImplementedError


class PythonTaskCreator(BaseTaskCreator):
    operator_class = PythonOperator

    def __init__(self, task_id: str, **kwargs) -> None:
        super().__init__(task_id, **kwargs)

    def get_operator_kwargs(self):
        kwargs = super().get_operator_kwargs()
        kwargs["python_callable"] = self.python_callable
        return kwargs

    def python_callable(self):
        raise NotImplementedError


class StopWorkerTaskCreator(PythonTaskCreator):
    def __init__(self, **kwargs) -> None:
        super().__init__("stop_worker", trigger_rule=TriggerRule.ALL_DONE, **kwargs)

    def python_callable(self):
        logger.info("Shutting down worker machine")
        with stopwatch("Shut down worker machine attempt", __class__.__name__):
            worker_manager = current_config.loader.get_worker_manager()
            if worker_manager.keep_running:
                logger.info("Not stopping worker, keep_running is True")
                return
            if worker_manager.get_running():
                result = worker_manager.run("[ ! -s RUNNING_COMPONENTS ]", warn=True)
                if result.ok:
                    logger.info("Shutting down worker machine")
                    worker_manager.stop()
                else:
                    logger.info("At least one docker component is running on worker, do not shut it down")
            else:
                logger.info("Not stopping, no running worker detected")


class TaskGenerator(ABC):
    def generate(self, dag: DAG):
        raise NotImplementedError


class SingleTaskGenerator(TaskGenerator):
    def __init__(self, task_creator: BaseTaskCreator):
        self.task_creator = task_creator

    def generate(self, dag: DAG) -> None:
        main_task = self.task_creator.create(dag)
        stop_worker_task = StopWorkerTaskCreator().create(dag)
        main_task >> stop_worker_task


class DagCreator:
    DEFAULT_ARGS = {
        "owner": "bizzflow",
        "depends_on_past": False,
        "start_date": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=31),
        "email_on_failure": False,
        "email": current_config.notification_emails[0] if current_config.notification_emails else None,
        "retries": 0,
        "retry_delay": timedelta(seconds=30),
        "catchup": False,
        "schedule_interval": None,
    }
    DEFAULT_DAG_KWARGS = {
        "schedule_interval": None,
        "catchup": False,
        "start_date": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=31),
    }

    def __init__(self, dag_id: str, task_generator: TaskGenerator, **kwargs) -> None:
        self.dag_id = dag_id
        self.task_generator = task_generator
        self.default_args = {**self.DEFAULT_ARGS, **kwargs.pop("default_args", {})}
        self.dag_kwargs = {**self.DEFAULT_DAG_KWARGS, **kwargs}

    def create(self):
        dag = DAG(dag_id=self.dag_id, default_args=self.default_args, **self.dag_kwargs)
        self.task_generator.generate(dag)
        return dag
