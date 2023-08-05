import logging
from datetime import timedelta
from typing import List

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.trigger_rule import TriggerRule

from toolkit.dags.helpers.base import BaseTaskCreator, StopWorkerTaskCreator, TaskGenerator
from toolkit.dags.helpers.datamarts import DatamartTaskCreator
from toolkit.dags.helpers.dummies import DummyTaskCreator
from toolkit.dags.helpers.extractors import ExtractorTaskCreator
from toolkit.dags.helpers.transformations import TransformationTaskCreator
from toolkit.dags.helpers.writers import WriterTaskCreator
from toolkit.managers.configuration.orchestration import BaseTask

logger = logging.getLogger(__name__)

try:
    from airflow.sensors import ExternalDAGSensor

    DAG_DEPENDENCY_ENABLED = True
except ImportError:
    DAG_DEPENDENCY_ENABLED = False
    logger.warning(
        "Could not import ExternalDAGSensor. You are probably using pre-dag-dependency Bizzflow plugins. "
        "See https://wiki.bizzflow.net on how to update your Bizzflow plugins. "
        "Understand that this is not an error until you try to use DAG Dependency functionality in orchestrations."
    )


class SubOrchestratorTaskCreator(BaseTaskCreator):
    def __init__(
        self, orchestration_id: str, data_age=None, timeout=None, poke_interval=None, dependency_mode=None, **kwargs
    ):
        super().__init__(f"required_{orchestration_id}", **kwargs)
        self.orchestration_id = orchestration_id
        self.timeout = timeout
        if self.timeout is None:
            logger.warning(f"-> Sub-orchestration {orchestration_id} has no timeout set, default is 6 hours")
            self.timeout = 6 * 3600
        self.poke_interval = poke_interval
        if self.poke_interval is None:
            logger.warning(f"-> Sub-orchestration {orchestration_id} has no poke interval set, default is 10 minutes")
            self.poke_interval = 10 * 60
        self.dependency_mode = dependency_mode
        if self.dependency_mode is None:
            logger.warning(f"-> Sub-orchestration {orchestration_id} has no dependency mode, default is reschedule")
            self.dependency_mode = "reschedule"
        self.data_age = data_age

    def get_operator_class(self):
        if not DAG_DEPENDENCY_ENABLED:
            logger.error(
                "Orchestration %s has requirements and DAG Dependency is not enabled. "
                "Make sure you have latest Bizzflow Plugins installed. "
                "For more information on updating Bizzflow Plugins, "
                "see https://wiki.bizzflow.net"
            )
            raise NameError("ExternalDAGSensor is not installed. See above for details.")
        return ExternalDAGSensor

    def get_operator_kwargs(self):
        kwargs = super().get_operator_kwargs()
        kwargs["external_dag_id"] = f"00_Orchestration_{self.orchestration_id}"
        kwargs["data_age"] = timedelta(seconds=self.data_age)
        kwargs["poke_interval"] = self.poke_interval
        kwargs["mode"] = self.dependency_mode
        kwargs["timeout"] = self.timeout
        return kwargs


class TaskCreatorFactory:
    TASK_DICT = {
        "extractor": ExtractorTaskCreator,
        "transformation": TransformationTaskCreator,
        "datamart": DatamartTaskCreator,
        "writer": WriterTaskCreator,
        "orchestration": SubOrchestratorTaskCreator,
        "dummy": DummyTaskCreator,
    }

    @classmethod
    def get_task_creator(cls, task: BaseTask):
        try:
            return cls.TASK_DICT[task.type](task.id, **task.config)
        except KeyError:
            logger.error(f"Executor of type {task.type} is not implemented")
            raise NotImplementedError(f"Executor of type {task.type} is not implemented")


class OrchestrationTaskGenerator(TaskGenerator):
    def __init__(self, tasks: List[List[BaseTask]]) -> None:
        super().__init__()
        self.tasks = tasks

    def generate(self, dag: DAG):
        previous_tasks = []
        last_mandatory_tasks = []
        stop_worker_task = StopWorkerTaskCreator().create(dag)
        for task_group in self.tasks:
            current_tasks = []
            current_mandatory_tasks = []
            for task in task_group:
                current_task = TaskCreatorFactory.get_task_creator(task).create(dag)

                for previous_task in previous_tasks:
                    previous_task >> current_task
                for last_mandatory_task in last_mandatory_tasks:
                    last_mandatory_task >> current_task
                current_task >> stop_worker_task

                if task.continue_on_error:
                    # if continue on error - make a group of tasks - add a dummy always success task after the real one
                    # this will cause that this group of tasks will be always successful independently on the task itself
                    task_id = f"{current_task.task_id}_continue_on_error"
                    dummy_task = DummyOperator(task_id=task_id, dag=dag, trigger_rule=TriggerRule.ALL_DONE)
                    current_task >> dummy_task
                    current_task = dummy_task
                else:
                    current_mandatory_tasks.append(current_task)
                current_tasks.append(current_task)
            previous_tasks = current_tasks
            last_mandatory_tasks = current_mandatory_tasks or last_mandatory_tasks
