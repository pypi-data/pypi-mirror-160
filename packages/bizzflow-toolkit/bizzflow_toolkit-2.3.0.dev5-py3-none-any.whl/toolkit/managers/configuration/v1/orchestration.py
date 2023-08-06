
from toolkit.managers.configuration.orchestration import BaseOrchestrationLoader
from toolkit.managers.configuration.v1.validators import OrchestrationValidator



class OrchestrationLoader(BaseOrchestrationLoader):
    validatorClass = OrchestrationValidator
