"""Google Cloud Storage File Storage Manager

Module for uploading files into Google Cloud Storage and their archivation.
"""
import csv
import os
from datetime import datetime
from io import BytesIO, TextIOWrapper
from logging import getLogger
from typing import Optional
from urllib.parse import urlparse

from toolkit.managers.file_storage.base import BaseFileStorageManager
from toolkit.managers.worker import GcpWorkerManager

logger = getLogger(__name__)
try:
    from google.cloud import storage
except ImportError:
    logger.info("Google Cloud Platform libraries are not installed.")


class GcsFileStorageManager(BaseFileStorageManager):
    """Manage uploading files into Google Cloud Storage and their archivation."""

    def __init__(self, live_bucket, archive_bucket, prefix: str = "", gcs_client: Optional["storage.Client"] = None):
        """Initiate Gcs File Storage Manager

        Arguments:
            prefix {str} -- relative path that should be used on file storage as prefix
            gcs_client {google.cloud.storage.Client} -- Google cloud storage client (default: default for current account)
        """
        super().__init__(prefix)
        self.gcs_client = gcs_client or storage.Client()
        self.bucket = live_bucket
        self.archive_bucket = archive_bucket

    @property
    def base_path(self):
        return f"gs://{self.bucket}/{self.prefix}/"

    def get_base_archive_path(self, timestamp: Optional[datetime] = None):
        timestamp = timestamp or datetime.now()
        return f"gs://{self.archive_bucket}/{self.prefix}/{timestamp.isoformat()}/"

    def upload_local_file(self, source: str, destination: str):
        """Upload single local file {source} to {destination}.

        Arguments:
            source {str} -- Local file path
            destination {str} -- Destination path (starting gs://)
        """
        destination = self.get_absolute_path(destination)
        blob = self.__blob_from_uri(destination)
        logger.info("Uploading %s to %s", source, destination)
        blob.upload_from_filename(source)
        logger.info("Upload complete")

    def clean_folder(self, path: str):
        """Delete all blobs with specified prefix {path}

        Arguments:
            path {str} -- Prefix containing bucket name and procotl gs://
        """
        path = self.get_absolute_path(path)
        # Ensure actual prefix
        if not path.endswith("/"):
            path = f"{path}/"
        blob = self.__blob_from_uri(path)
        children = blob.bucket.list_blobs(prefix=blob.name)
        for child in children:
            logger.warning("Removing GCS blob %s", child.name)
            child.delete()

    def __blob_from_uri(self, uri: str) -> "storage.Blob":
        """Helper function to get blob object from GCS uri (starting gs://)

        Arguments:
            uri {str} -- GCS uri to blob (e.g. gs://bucket-name/path/to/file.ext)

        Returns:
            storage.Blob
        """
        # So I guess this is a thing now... (\\)
        url = urlparse(uri.replace("\\", "/"))
        bucket_name = url.netloc
        blob_path = url.path[1:] if url.path.startswith("/") else url.path
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        return blob

    def download_file_to_worker(self, worker: GcpWorkerManager, source: str, destination: str):
        """Download remote blob from GCS {source} to remote worker's {destination} using {ssh} connection.

        Arguments:
            ssh {paramiko.SSHClient} -- Active connection
            source {str} -- GCS blob path (starting with gs://)
            destination {str} -- Worker's local path
        """
        source = self.get_absolute_path(source)
        source = source.strip("'")
        destination = destination.strip("'")

        command = (
            f"if gsutil ls '{source}'; then gsutil -m cp '{source}' '{destination}'; else echo 'No files to copy.'; fi"
        )
        fid = worker.run(command, hide=False)
        if not fid.ok:
            logger.error("Failed to download %s to %s", source, destination)
            raise Exception(f"{fid.stderr}\n{fid.stdout}")
        logger.info("Data successfully downloaded to destination")

    def upload_files_from_worker(self, worker: GcpWorkerManager, data_volume_path: str):
        # TODO: refactor this to be more generic, this is rubbish TBH, failed review!
        # see `base.py`
        # create method for remote upload, this does not feel like a "FileStorageManager" at all
        """Upload file into gcs storage and archive it

        Arguments:
            worker {GcpWorkerManager} -- GcpWorkerManager

            data_volume_path {str} -- Path to extracted data

        Raises:
            Exception: If failed to upload csv to live or archive bucket
        """

        archive_storage_path = self.get_base_archive_path()
        data_path = os.path.join("{}/".format(data_volume_path), "*.csv")
        # upload to live bucket
        logger.info("Uploading csv to live bucket")
        fid = worker.run(f"gsutil -m cp '{data_path}' '{self.base_path}'", hide=False)
        if not fid.ok:
            logger.error("Failed to upload csv to live bucket")
            raise Exception(fid.stderr)
        logger.info("Data successfully uploaded to live bucket")
        # upload to archive bucket
        logger.info("Uploading csv to archive bucket")
        fid = worker.run(
            f"gsutil -m cp -r '{self.base_path}' '{archive_storage_path}'",
            hide=False,
        )
        if not fid.ok:
            logger.error("Failed to upload csv to archive bucket")
            raise Exception(fid.stderr)
        logger.info("Data successfully uploaded to archive bucket")

    def list_files(self, relative_path: str, suffix: Optional[str] = None):
        """Lists all files in storage bucket

        Arguments:
            relative_path {str} -- relative path to current prefix

        Returns:
            blobs_list {list} -- List of blobs in GCS bucket
        """
        prefix = os.path.join(self.prefix, relative_path)
        bucket = self.gcs_client.get_bucket(self.bucket)
        blobs = bucket.list_blobs(prefix=prefix)
        blobs_list = []
        for blob in blobs:
            if suffix and not blob.name.endswith(suffix):
                continue
            # Skip files nested in subdirectories
            # Checks whether there is any directory between prefix and blob's location
            if os.path.dirname(os.path.relpath(blob.name, prefix)):
                continue
            blobs_list.append(blob.name)
        return blobs_list

    def get_fields_names_from_csv(self, path: str):
        path = self.get_absolute_path(path)

        bucket = self.gcs_client.get_bucket(self.bucket)
        # Get columns (Get first "PEEK_SIZE" bytes to get header)
        parsed_url = urlparse(path)
        logger.debug("Parsed url: %s", parsed_url)
        blob_name = parsed_url.path
        if blob_name.startswith("/"):
            blob_name_fix = blob_name[len("/") :]
        else:
            blob_name_fix = blob_name
        logger.debug("Generated blob name: %s", blob_name_fix)
        blob = bucket.get_blob(blob_name_fix)
        with BytesIO() as bfid:
            blob.download_to_file(bfid, start=0, end=self.PEEK_SIZE)
            bfid.seek(0)
            wrapper = TextIOWrapper(bfid, encoding="utf-8")
            reader = csv.reader(wrapper)
            header = next(reader)
            logger.info("blob: %s, %d columns", blob.name, len(header))
        logger.info(f"File {path} contains {len(header)} columns: {header}")
        return header
