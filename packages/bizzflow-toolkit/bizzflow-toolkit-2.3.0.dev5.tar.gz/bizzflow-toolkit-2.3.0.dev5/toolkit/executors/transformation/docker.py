import uuid
from logging import getLogger

from toolkit.base import Step
from toolkit.executors.base.docker import DockerExecutor, DockerInputOutputMixin
from toolkit.managers.component.docker import BaseDockerComponentManager
from toolkit.managers.file_storage.base import BaseFileStorageManager
from toolkit.managers.storage.base import BaseStorageManager
from toolkit.managers.worker.base import BaseWorkerManager

logger = getLogger(__name__)


class DockerTransformationExecutor(DockerInputOutputMixin, DockerExecutor):
    def __init__(
        self,
        worker_manager: BaseWorkerManager,
        storage_manager: BaseStorageManager,
        file_storage_manager: BaseFileStorageManager,
        component_manager: BaseDockerComponentManager,
        step: Step,
        inputs: list,
        output: str,
    ):
        super().__init__(worker_manager, storage_manager, file_storage_manager, component_manager, step)
        self.output = output
        self._inputs = inputs

    def _create_working_kex_name(self):
        return f"tr_{uuid.uuid4().hex}"

    def _create_output_kex_name(self):
        return self.output
