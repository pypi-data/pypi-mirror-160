import logging
import os
import tempfile
import zipfile

import invoke

from toolkit.managers.component.docker_build import BaseDockerBuildComponentManager
from toolkit.managers.file_storage.base import BaseFileStorageManager
from toolkit.managers.worker.base import BaseWorkerManager

logger = logging.getLogger(__name__)


class LocalStorageDockerComponentManager(BaseDockerBuildComponentManager):
    def __init__(
        self,
        component_type: str,
        component_name: str,
        component_id: str,
        component_config: dict,
        worker_manager: BaseWorkerManager,
        file_storage_manager: BaseFileStorageManager,
        component_source_path: str,
    ):
        super().__init__(component_type, component_name, component_id, component_config, worker_manager)
        self.component_source_path = component_source_path
        self.file_storage_manager = file_storage_manager
        tmp_zip_file_name = "{}.zip".format(next(tempfile._get_candidate_names()))
        self.local_tmp_zip_file = os.path.join("/tmp", tmp_zip_file_name)
        self.worker_machine_tmp_zip_file = os.path.join(self.worker_component_path, "source.zip")
        self.file_storage_tmp_zip_folder = self.file_storage_manager.get_tmp_dir()
        self.file_storage_tmp_zip_file = os.path.join(self.file_storage_tmp_zip_folder, "source.zip")

    def _docker_download(self):
        self._validate()
        self._zip_component()
        logger.info("Downloading component source to worker machine")
        self.file_storage_manager.upload_local_file(self.local_tmp_zip_file, self.file_storage_tmp_zip_file)
        os.remove(self.local_tmp_zip_file)

        self.file_storage_manager.download_file_to_worker(
            self.worker_manager, self.file_storage_tmp_zip_file, self.worker_component_path
        )
        self.file_storage_manager.clean_folder(self.file_storage_tmp_zip_folder)
        self._unzip_component_on_worker_machine()

    def _validate(self):
        if not os.path.exists(os.path.join(self.component_source_path, "Dockerfile")):
            raise FileNotFoundError(f"No Dockerfile was found in transformation source '{self.component_source_path}'")

    def _zip_component(self):
        logger.info("Packing local component source...")
        with zipfile.ZipFile(self.local_tmp_zip_file, mode="w") as zip:
            for root, dirs, fils in os.walk(self.component_source_path):
                for fname in fils:
                    fullpath = os.path.join(root, fname)
                    relpath = os.path.relpath(fullpath, self.component_source_path)
                    zip.write(fullpath, relpath)

    def _unzip_component_on_worker_machine(self):
        logger.info("Will make sure 'unzip' dependency exists")
        try:
            self.worker_manager.run("which unzip")
        except invoke.UnexpectedExit as error:
            logger.error(error, exc_info=True)
            logger.error(
                "'unzip' binary was not found in worker's path. Please make sure the dependency exists on the worker"
            )
            raise
        self.worker_manager.run(
            f"unzip -o {self.worker_machine_tmp_zip_file} -d '{self.worker_component_path}' && rm {self.worker_machine_tmp_zip_file}"
        )
