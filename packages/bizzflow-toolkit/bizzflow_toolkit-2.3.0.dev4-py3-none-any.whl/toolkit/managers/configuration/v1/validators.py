import os

from toolkit.managers.configuration.exceptions import ConfigurationNotValid
from toolkit.managers.configuration.utils import Graph
from toolkit.managers.configuration.validators import BaseConfigValidator



class ProjectValidator(BaseConfigValidator):
    schema_file = "project.schema.json"
    schema_version = "v1"


class OrchestrationValidator(BaseConfigValidator):
    schema_file = "orchestrations.schema.json"
    schema_version = "v1"

    def validate(self, config, available_extractors, available_writers, available_transformations):
        super().validate(config)
        self._validate_acyclic(config)
        for orchestration in config:
            for task in orchestration["tasks"]:
                if task["type"] == "group":
                    for sub_task in task["tasks"]:
                        self._component_exists(
                            sub_task, available_extractors, available_writers, available_transformations
                        )
                self._component_exists(task, available_extractors, available_writers, available_transformations)

    def _validate_acyclic(self, config):
        orchestration_dependency_graph = Graph([o["id"] for o in config])
        for orchestration in config:
            for task in orchestration["tasks"]:
                if task["type"] == "group":
                    for sub_task in task["tasks"]:
                        if sub_task["type"] == "orchestration":
                            try:
                                orchestration_dependency_graph.add_edge(orchestration["id"], sub_task["id"])
                            except AssertionError:
                                raise ConfigurationNotValid(
                                    f"Orchestration {sub_task['id']} not defined cannot be part task of orchestration {orchestration['id']}"
                                )
                elif task["type"] == "orchestration":
                    try:
                        orchestration_dependency_graph.add_edge(orchestration["id"], task["id"])
                    except AssertionError:
                        raise ConfigurationNotValid(
                            f"Orchestration {task['id']} not defined cannot be part task of orchestration {orchestration['id']}"
                        )
        if orchestration_dependency_graph.detect_cycle():
            raise ConfigurationNotValid("Orchestration dependencies cannot be cyclic")

    def _component_exists(self, task, available_extractors, available_writers, available_transformations):
        if task["type"] == "extractor":
            if task["id"] not in available_extractors:
                raise ConfigurationNotValid(f"Configuration of extractor {task['id']} is missing")
        elif task["type"] == "writer":
            if task["id"] not in available_writers:
                raise ConfigurationNotValid(f"Configuration of witer {task['id']} is missing")
        elif task["type"] == "transformation":
            if task["id"] not in available_transformations:
                raise ConfigurationNotValid(f"Configuration of transformation {task['id']} is missing")


class TransformationsValidator(BaseConfigValidator):
    schema_file = "transformations.schema.json"
    schema_version = "v1"

    def validate(self, config, project_path):
        super().validate(config)
        for i in config:
            source_path = os.path.join(project_path, "transformations", i["source"])
            logger.info("Looking for source directory in %s", source_path)
            if not os.path.exists(source_path):
                logger.error("For transformation '%s': path '%s' not exists", i["id"], source_path)
                raise ConfigurationNotValid(
                    "For transformation '{}': path '{}' not exists".format(i["id"], source_path)
                )


class DatamartsValidator(BaseConfigValidator):
    schema_file = "datamarts.schema.json"
    schema_version = "v1"


class ExtractorValidator(BaseConfigValidator):
    schema_file = "extractor.schema.json"
    schema_version = "v1"


class WriterValidator(BaseConfigValidator):
    schema_file = "writer.schema.json"
    schema_version = "v1"


class StepValidator(BaseConfigValidator):
    schema_file = "step.schema.json"
    schema_version = "v1"


class SharingValidator(BaseConfigValidator):
    schema_file = "sharing.schema.json"
    schema_version = "v1"
