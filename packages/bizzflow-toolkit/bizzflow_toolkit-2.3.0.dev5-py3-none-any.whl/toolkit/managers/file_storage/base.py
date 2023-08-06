"""File Storage Manager

Module for managing all file storage managers on different platforms.
"""
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from toolkit.managers.worker.base import BaseWorkerManager


class BaseFileStorageManager:
    """Abstract class for all file storage managers on different platforms, e.g. GcsFileStorageMAnager.

    Raises:
        NotImplementedError: If any of methods is not imlemented in the child class.
    """

    PEEK_SIZE = 9192

    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    @property
    def base_path(self):
        raise NotImplementedError("This method must be overridden")

    def get_base_archive_path(self, timestamp: Optional[datetime] = None):
        raise NotImplementedError("This method must be overridden")

    def get_absolute_path(self, path: str) -> str:
        """Return absolute path to storage"""
        path = path.lstrip("/")
        return os.path.join(self.base_path, path)

    def get_tmp_dir(self):
        return f"tmp_{uuid.uuid4().hex}"

    def upload_files_from_worker(self, worker: BaseWorkerManager, data_volume_path: str):
        # TODO: This is rubbish and should not be used as it is right now
        # Create separate methods, this class and all subclasses do not feel like File Storage Managers at all
        """Upload file into storage and archive it."""
        raise NotImplementedError("This method must be overriden")

    def clean_up_live_storage(self):
        self.clean_folder("")

    def clean_folder(self, path: str):
        """Delete all files in remote file storage folder recursively

        Arguments:
            path {str} -- Path to remote
        """
        raise NotImplementedError("This method must be overriden")

    def upload_local_file(self, source: str, destination: str):
        """Upload local file {source} into remote {destination}

        Arguments:
            source {str} -- Local source file
            destination {str} -- Remote destination path
        """
        raise NotImplementedError("This method must be overriden")

    def download_file_to_worker(self, worker: BaseWorkerManager, source: str, destination: str):
        """Download remote file from file storage path {source} to worker local storage {destination}

        Arguments:
            worker {BaseWorkerManager} -- Worker Manager
            source {str} -- File storage source
            destination {str} -- worker local destination folder
        """
        raise NotImplementedError("This method must be overriden")

    def list_files(self, relative_path: str, suffix: Optional[str] = None):
        """Lists all files in  bucket."""
        raise NotImplementedError("This method must be overridden")

    def get_fields_names_from_csv(self, path: str) -> List[str]:
        """

        Arguments:
            path {str} -- path to table in uri format

        Returns:
            List -- list of fields namesr
        """
        raise NotImplementedError("This method must be overridden")

    def write_to_csv_file(self, path: str, values: Iterable[Dict[str, Any]]):
        """Create and upload csv file to file storage from given data"""
        raise NotImplementedError("This method must be overridden")
