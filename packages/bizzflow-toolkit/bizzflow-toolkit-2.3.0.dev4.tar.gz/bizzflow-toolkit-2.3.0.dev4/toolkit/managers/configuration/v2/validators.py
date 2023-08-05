import logging

from toolkit.managers.configuration.v1 import validators

logger = logging.getLogger(__name__)


class ProjectValidator(validators.ProjectValidator):
    schema_version = "v2"


class OrchestrationValidator(validators.OrchestrationValidator):
    schema_version = "v2"


class TransformationsValidator(validators.TransformationsValidator):
    schema_version = "v2"


class DatamartsValidator(validators.DatamartsValidator):
    schema_version = "v2"


class ExtractorValidator(validators.ExtractorValidator):
    schema_version = "v2"


class WriterValidator(validators.WriterValidator):
    schema_version = "v2"
