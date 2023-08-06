import os
from logging import getLogger
from typing import TYPE_CHECKING, List

from toolkit.managers.configuration.validators import BaseConfigValidator

if TYPE_CHECKING:
    from toolkit.managers.configuration.loader import BaseConfigurationLoader

logger = getLogger(__name__)


class BaseTask:
    type = NotImplemented

    def __init__(self, id, continue_on_error, notify, timeout=None):
        self.id = id
        self.continue_on_error = bool(continue_on_error)
        self.notify = bool(notify)
        if timeout is None:
            timeout = 0
        try:
            self.timeout = int(timeout)
        except ValueError as error:
            raise ValueError(f"'timeout' has invalid value '{timeout}' for task id {id}") from error

    @property
    def config(self):
        return {
            "continue_on_error": self.continue_on_error,
            "notify": self.notify,
            "timeout": self.timeout,
        }


class ExtractorTask(BaseTask):
    type = "extractor"


class WriterTask(BaseTask):
    type = "writer"


class TransformationTask(BaseTask):
    type = "transformation"


class DatamartTask(BaseTask):
    type = "datamart"


class DummyTask(BaseTask):
    type = "dummy"

    def __init__(self, id, continue_on_error, notify, success, duration):
        super().__init__(id, continue_on_error, notify)
        self.success = success
        self.duration = duration

    @property
    def config(self):
        config = super().config
        config["success"] = self.success
        config["duration"] = self.duration
        return config


class OrchestrationTask(BaseTask):
    type = "orchestration"

    def __init__(self, id, continue_on_error, notify, data_age, poke_interval, timeout, dependency_mode):
        super().__init__(id, continue_on_error, notify)
        self.data_age = data_age
        self.poke_interval = poke_interval
        self.timeout = timeout
        self.dependency_mode = dependency_mode

    @property
    def config(self):
        config = super().config
        config["data_age"] = self.data_age
        config["poke_interval"] = self.poke_interval
        config["timeout"] = self.timeout
        config["dependency_mode"] = self.dependency_mode
        return config


class Orchestration:
    def __init__(self, id, tasks: List[List[BaseTask]], schedule: str):
        self.id = id
        self.tasks = tasks
        self.schedule = schedule


class BaseOrchestrationLoader:
    validatorClass = BaseConfigValidator

    def __init__(self, project_loader: "BaseConfigurationLoader"):
        self.project_loader = project_loader
        self.validator = self.validatorClass(self.project_loader.file_loader)
        self._orchestrations = None
        self.project_path = self.project_loader.project_path
        self.config_file_format = self.project_loader.config_file_format
        self.project_config = self.project_loader.project_config

    def _load_orchestration_file(self) -> dict:
        orchestrations = {}
        logger.info("Creating list of orchestrations")
        path = os.path.join(self.project_path, f"orchestrations.{self.config_file_format}")
        config = self.project_loader.load_file(self.config_file_format, path) or []
        self.validator.validate(
            config,
            available_extractors=self.project_loader.get_extractors_ids(),
            available_writers=self.project_loader.get_writers_ids(),
            available_transformations=self.project_loader.get_transformations_ids(),
        )
        for or_config in config:
            orchestrations[or_config["id"]] = self._init_orchestration_from_config(or_config)
        return orchestrations

    @classmethod
    def _init_task_from_config(cls, config, default_notify):
        if config["type"] == "extractor":
            return ExtractorTask(
                id=config["id"],
                notify=config.get("notify", default_notify),
                continue_on_error=config.get("continue_on_error", False),
                timeout=config.get("timeout"),
            )
        elif config["type"] == "transformation":
            return TransformationTask(
                id=config["id"],
                notify=config.get("notify", default_notify),
                continue_on_error=config.get("continue_on_error", False),
                timeout=config.get("timeout"),
            )
        elif config["type"] == "writer":
            return WriterTask(
                id=config["id"],
                notify=config.get("notify", default_notify),
                continue_on_error=config.get("continue_on_error", False),
                timeout=config.get("timeout"),
            )
        elif config["type"] == "datamart":
            return DatamartTask(
                id=config["id"],
                notify=config.get("notify", default_notify),
                continue_on_error=config.get("continue_on_error", False),
                timeout=config.get("timeout"),
            )
        elif config["type"] == "orchestration":
            return OrchestrationTask(
                id=config["id"],
                notify=config.get("notify", default_notify),
                continue_on_error=config.get("continue_on_error", False),
                data_age=config["data_age"],
                poke_interval=config.get("poke_interval", 10 * 60),
                dependency_mode=config.get("dependency_mode", "reschedule"),
                timeout=config.get("timeout", 6 * 3600),
            )
        elif config["type"] == "dummy":
            return DummyTask(
                id=config["id"],
                notify=config.get("notify", default_notify),
                continue_on_error=config.get("continue_on_error", False),
                success=config.get("success", True),
                duration=config.get("duration", 1),
            )

    @classmethod
    def _init_orchestration_from_config(cls, config):
        tasks = []
        orchestration_notify = config.get("notify", True)
        for task_config in config["tasks"]:
            task_group = []
            if task_config["type"] == "group":
                for group_task_config in task_config["tasks"]:
                    task_group.append(
                        cls._init_task_from_config(group_task_config, default_notify=orchestration_notify)
                    )
            else:
                task_group.append(cls._init_task_from_config(task_config, default_notify=orchestration_notify))
            tasks.append(task_group)

        return Orchestration(
            id=config["id"],
            tasks=tasks,
            schedule=config.get("schedule"),
        )

    @property
    def orchestrations(self):
        if self._orchestrations is None:
            self._orchestrations = self._load_orchestration_file()
        return self._orchestrations

    def get_orchestrations(self):
        return self.orchestrations.keys()

    def validate(self):
        # just access transformations validation is included
        self.get_orchestrations()

    def get_orchestration(self, orchestration_id):
        return self.orchestrations[orchestration_id]
