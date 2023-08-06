from logging import getLogger

from toolkit.managers.configuration.orchestration import BaseOrchestrationLoader
from toolkit.managers.configuration.v2.validators import OrchestrationValidator

logger = getLogger(__name__)


class OrchestrationLoader(BaseOrchestrationLoader):
    validatorClass = OrchestrationValidator
