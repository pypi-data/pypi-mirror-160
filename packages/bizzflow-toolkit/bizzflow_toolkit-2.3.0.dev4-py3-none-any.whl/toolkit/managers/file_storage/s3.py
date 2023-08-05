"""S3 File Storage Manager

Module for uploading files into AWS S3 and their archivation.
"""
import csv
import os
import subprocess
from datetime import datetime
from io import BytesIO, TextIOWrapper
from logging import getLogger
from typing import Optional
from urllib.parse import urlparse

from toolkit.managers.file_storage.base import BaseFileStorageManager
from toolkit.managers.worker import AwsWorkerManager

logger = getLogger(__name__)
try:
    import boto3
    import botocore.exceptions
except ImportError:
    logger.info("AWS libraries are not installed.")


class S3FileStorageManager(BaseFileStorageManager):
    """Manage uploading files into AWS S3 and their archivation."""

    def __init__(
        self,
        live_bucket,
        archive_bucket,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_iam_role=None,
        prefix: str = "",
    ):
        """Initiate S3 File Storage Manager

        Arguments:
            prefix {str} -- relative path that should be used on file storage as prefix
        """
        super().__init__(prefix)
        self.bucket = live_bucket
        self.archive_bucket = archive_bucket
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_iam_role = aws_iam_role

    @property
    def base_path(self):
        return f"s3://{self.bucket}/{self.prefix}/"

    def get_base_archive_path(self, timestamp: Optional[datetime] = None):
        timestamp = timestamp or datetime.now()
        return f"s3://{self.archive_bucket}/{self.prefix}/{timestamp.isoformat()}/"

    def upload_files_from_worker(self, worker: AwsWorkerManager, data_volume_path: str):
        """Upload file into s3 and archive it

        Arguments:
            worker {AwsWorkerManager} -- AwsWorkerManager

            data_volume_path {str} -- Path to extracted data

        Raises:
            Exception: If failed to upload csv to live or archive bucket
        """
        archive_storage_path = self.get_base_archive_path()
        data_path = "{}/".format(data_volume_path)
        # upload to live bucket
        logger.info(f"Uploading csv from {data_path} to live bucket")
        fid = worker.run(
            f"aws s3 cp '{data_path}' '{self.base_path}' --recursive --include '*.csv'",
            hide=False,
        )
        if not fid.ok:
            logger.error("Failed to upload csv to live bucket")
            raise Exception(fid.stderr)
        logger.info("Data successfully uploaded to live bucket")
        # upload to archive bucket
        logger.info("Uploading csv to archive bucket")
        fid = worker.run(
            f"aws s3 cp '{self.base_path}' '{archive_storage_path}' --recursive --include '*.csv'",
            hide=False,
        )
        if not fid.ok:
            logger.error("Failed to upload csv to archive bucket")
            raise Exception(fid.stderr)
        logger.info("Data successfully uploaded to archive bucket")

    def __remote_file_exists(self, uri: str) -> bool:
        """Returns whether remote file exists, if False, the path may still exist as a prefix"""
        blob = self.__blob_from_uri(uri)
        try:
            blob.load()
            return True
        except botocore.exceptions.ClientError:
            return False

    def download_file_to_worker(self, worker: AwsWorkerManager, source: str, destination: str):
        """Download remote files from S3 to remote worker's {destination} using {ssh} connection.

        Arguments:
            worker {AwsWorkerManager} -- AWS worker
            source {str} -- S3 path (starting with s3://)
            destination {str} -- Worker's local path
        """
        # for downloading folder S3 do not use asterisk just prefix so remove it
        source = self.get_absolute_path(source)

        source = source.rstrip("*")

        # --recursive does not work for files (creates empty directory instead)
        # so we need to "guess" whether the requested path is a file or a directory
        # TODO: Is there any better way to do this?
        recursive = "" if self.__remote_file_exists(source) else "--recursive"

        logger.info(f"Copying {source} to {destination}")
        fid = worker.run(
            f"aws s3 cp '{source}' '{destination}' {recursive} --quiet",
            hide=False,
        )
        if not fid.ok:
            logger.error("Failed to download %s to %s", source, destination)
            raise Exception(f"{fid.stderr}\n{fid.stdout}")
        logger.info("Data successfully downloaded to destination")

    def clean_folder(self, path: str):
        path = self.get_absolute_path(path)
        logger.info(f"Cleaning path: {path}")
        pipe = subprocess.Popen(
            f'aws s3 rm "{path}" --recursive --quiet',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = pipe.communicate()
        out = stdout.decode("utf-8")
        err = stderr.decode("utf-8")
        logger.info(out)
        if pipe.returncode != 0:
            raise Exception(f"Failed to clean s3 folder '{path}'.\n{err}")

    def __blob_from_uri(self, uri: str):
        """Helper function to get blob object from S3 uri (starting s3://)"""
        url = urlparse(uri)
        bucket_name = url.netloc
        blob_path = url.path.lstrip("/")
        s3 = boto3.resource("s3")
        blob = s3.Object(bucket_name, blob_path)
        return blob

    def upload_local_file(self, source: str, destination: str):
        """Upload single local file {source} to {destination}."""
        destination = self.get_absolute_path(destination)
        blob = self.__blob_from_uri(destination)
        logger.info("Uploading %s to %s", source, destination)
        blob.upload_file(source)
        logger.info("Upload complete")

    def list_files(self, relative_path: str, suffix: Optional[str] = None):
        """Lists all files in storage bucket

        Arguments:
            relative_path {str} -- relative path to current prefix


        Returns:
            files_list {list} -- List of files in AWS S3 bucket
        """
        prefix = os.path.join(self.prefix, relative_path)
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.bucket)
        filelist = bucket.objects.filter(Prefix=prefix)
        if suffix:
            return [file_object.key for file_object in filelist if str(file_object.key).endswith(suffix)]
        return [file_object.key for file_object in filelist]

    def get_fields_names_from_csv(self, path: str):
        path = self.get_absolute_path(path)
        parsed_url = urlparse(path)
        logger.debug("Parsed url: %s", parsed_url)
        infile_name = parsed_url.path
        if infile_name.startswith("/"):
            infile_name_fix = infile_name[len("/") :]
        else:
            infile_name_fix = infile_name
        logger.debug("Generated infile name: %s", infile_name_fix)
        s3 = boto3.resource("s3")
        obj = s3.Object(self.bucket, infile_name_fix)
        body = obj.get()["Body"]
        bio = BytesIO(body.read(self.PEEK_SIZE))
        wrapper = TextIOWrapper(bio, encoding="utf-8")
        wrapper.seek(0)
        reader = csv.reader(wrapper, dialect=csv.unix_dialect)
        header = next(reader)
        logger.info(f"File {path} contains {len(header)} columns: {header}")
        return header
