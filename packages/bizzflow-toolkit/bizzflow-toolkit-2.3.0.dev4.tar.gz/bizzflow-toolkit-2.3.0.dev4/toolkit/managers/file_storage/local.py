import csv
import logging
import os
import shutil
from datetime import datetime
from glob import glob
from typing import Any, Dict, Iterable, Optional

logger = logging.getLogger(__name__)

from toolkit.managers.file_storage.base import BaseFileStorageManager


class LocalFileStorageManager(BaseFileStorageManager):
    def __init__(
        self,
        live_folder,
        archive_folder,
        prefix: str = "",
    ):
        super().__init__(prefix)
        self.live_folder = live_folder
        self.archive_folder = archive_folder
        if not os.path.exists(self.live_folder):
            os.makedirs(self.live_folder)
        if not os.path.exists(self.archive_folder):
            os.makedirs(self.archive_folder)

    @property
    def base_path(self):
        return os.path.join(self.live_folder, self.prefix)

    def get_base_archive_path(self, timestamp: Optional[datetime] = None):
        timestamp = timestamp or datetime.now()
        return os.path.join(self.archive_folder, f"{self.prefix}/{timestamp.isoformat()}")

    def get_fields_names_from_csv(self, path: str):
        path = self.get_absolute_path(path)
        with open(path) as file:
            header = csv.DictReader(file, dialect=csv.unix_dialect).fieldnames
        if header is None:
            raise ValueError(f"File {path} has either zero size or an invalid header")
        logger.info(f"File {path} contains {len(header)} columns: {header}")
        return header

    def write_to_csv_file(self, path: str, values: Iterable[Dict[str, Any]]):
        path = self.get_absolute_path(path)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        logger.info(f"Start storing file {path}")
        try:
            first_item = next(values)
        except StopIteration:
            logger.info(f"Cannot write {path} have no data")
            return
        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=first_item.keys(), dialect=csv.unix_dialect)
            writer.writeheader()
            writer.writerow(first_item)
            writer.writerows(values)

    def upload_local_file(self, source: str, destination: str):
        """Upload single local file {source} to {destination}"""
        destination = self.get_absolute_path(destination)
        logger.info("Creating local copy %s => %s", source, destination)
        dname = os.path.dirname(destination)
        if not os.path.exists(dname):
            os.makedirs(dname)
        shutil.copyfile(source, destination)

    def list_files(self, relative_path: str, suffix: Optional[str] = None):
        path = os.path.join(self.base_path, relative_path)
        logger.info("Listing files in %s", path)
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    if suffix and not entry.name.endswith(suffix):
                        continue
                    yield entry.name

    def clean_folder(self, path: str):
        path = self.get_absolute_path(path)
        logger.info(f"Cleaning path: {path}")
        try:
            shutil.rmtree(path)
        except OSError:
            logger.warning("Failed to clean directory %s", path, exc_info=True)

    def download_file_to_worker(self, worker, source: str, destination: str):
        absource = self.get_absolute_path(source)
        if source[-1] == "*":
            logger.info("Copying files from glob pattern %s", source)
            for srcpatt in glob(absource):
                logger.info("Found %s in the source", srcpatt)
                bname = os.path.basename(srcpatt)
                self.download_file_to_worker(worker, os.path.relpath(srcpatt, self.base_path), destination)
            return
        if not os.path.exists(destination):
            os.makedirs(destination)
        bname = os.path.basename(source)
        destination = os.path.join(destination, bname)
        logger.info("Copying file %s from local storage to %s", absource, destination)
        shutil.copyfile(absource, destination)

    def upload_files_from_worker(self, worker, data_volume_path: str):
        logger.info("Creating live and archive copy of worker data from %s", data_volume_path)
        archive_path = self.get_base_archive_path()
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)
        for fname in glob(os.path.join(data_volume_path, "*.csv")):
            outname = os.path.join(self.base_path, os.path.basename(fname))
            archivename = os.path.join(archive_path, os.path.basename(fname))
            logger.info("Copying %s into %s", fname, outname)
            shutil.copyfile(fname, outname)
            logger.info("Copying %s into %s", fname, archivename)
            shutil.copyfile(fname, archivename)
