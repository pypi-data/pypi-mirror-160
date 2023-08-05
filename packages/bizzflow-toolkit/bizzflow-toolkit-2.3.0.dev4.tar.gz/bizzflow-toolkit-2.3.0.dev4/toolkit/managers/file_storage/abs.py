import csv
import json
import logging
import os
import time
from datetime import datetime, timedelta
from io import BytesIO, TextIOWrapper
from json.decoder import JSONDecodeError
from typing import Any, Dict, Iterable, Optional, Sequence, Tuple
from urllib.parse import urlparse

from toolkit.managers.worker import AzureWorkerManager

logger = logging.getLogger(__name__)

try:
    from azure.storage.blob import (
        AccountSasPermissions,
        BlobClient,
        ContainerClient,
        ResourceTypes,
        generate_account_sas,
    )
except ImportError:
    logger.info("Azure Storage libraries are not installed.")

from toolkit.managers.file_storage.base import BaseFileStorageManager

COPY_POLL_INTERVAL = 5
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)


def _get_csv_stream(fieldnames: Sequence) -> Tuple[BytesIO, TextIOWrapper, "csv.DictWriter"]:
    stream = BytesIO()
    wrapper = TextIOWrapper(stream, encoding="utf-8")
    writer = csv.DictWriter(wrapper, dialect=csv.unix_dialect, fieldnames=fieldnames)
    return stream, wrapper, writer


class ABSFileStorageManager(BaseFileStorageManager):
    PEEK_SIZE = 16 * 1024

    def __init__(
        self,
        account_name,
        live_container,
        archive_container,
        access_key,
        blob_storage_credential,
        prefix: str = "",
    ):
        super().__init__(prefix)
        self.account_name = account_name
        self.container_name = live_container
        self.archive_container = archive_container
        self.access_key = access_key
        self.account_url = f"https://{self.account_name}.blob.core.windows.net"
        self.container_url = f"{self.account_url}/{self.container_name}"
        self.blob_storage_credential = blob_storage_credential

    @property
    def base_path(self):
        return f"az://{self.container_name}/{self.prefix}/"

    def get_base_archive_path(self, timestamp: Optional[datetime] = None):
        timestamp = timestamp or datetime.now()
        return f"az://{self.archive_container}/{self.prefix}/{timestamp.isoformat()}"

    def get_sas_token(self, resource_kwargs: dict, permission_kwargs: dict, ttl=timedelta(hours=1)):
        resource_kwargs = resource_kwargs or {}
        permission_kwargs = permission_kwargs or {}
        token = generate_account_sas(
            account_name=self.account_name,
            account_key=self.access_key,
            resource_types=ResourceTypes(**resource_kwargs),
            permission=AccountSasPermissions(**permission_kwargs),
            expiry=datetime.utcnow() + ttl,
        )
        return token

    def get_blob_name(self, uri: str) -> str:
        return self.__blob_from_uri(uri).blob_name

    def get_fields_names_from_csv(self, path: str):
        path = self.get_absolute_path(path)

        blob = self.__blob_from_uri(path)

        blob_data = blob.download_blob(offset=0, length=self.PEEK_SIZE)

        stream = BytesIO()
        blob_data.readinto(stream)
        blob_data.readinto(stream)
        wrapper = TextIOWrapper(stream, encoding="utf-8")
        wrapper.seek(0)
        reader = csv.reader(wrapper, dialect=csv.unix_dialect)
        header = next(reader)
        logger.info(f"File {path} contains {len(header)} columns: {header}")
        return header

    def __blob_from_uri(self, uri: str, mode: str = "wr") -> "BlobClient":
        permission_kwargs = {}
        if "r" in mode:
            permission_kwargs.update({"read": True})
        if "w" in mode:
            permission_kwargs.update({"write": True})
        if "l" in mode:
            permission_kwargs.update({"list": True})
        if "d" in mode:
            permission_kwargs.update({"delete": True})
        sas_token = self.get_sas_token(resource_kwargs={"object": True}, permission_kwargs=permission_kwargs)
        parse = urlparse(uri)
        container_name = parse.netloc or self.container_name
        path = parse.path.strip("/")
        blob = BlobClient(
            account_url=self.account_url,
            credential=sas_token,
            container_name=container_name,
            blob_name=path,
        )
        return blob

    def __get_container(self, container_name: str) -> "ContainerClient":
        sas_token = self.get_sas_token(
            resource_kwargs={"container": True},
            permission_kwargs={"read": True, "write": True, "list": True},
        )
        client = ContainerClient(
            account_url=self.account_url,
            container_name=container_name,
            credential=sas_token,
        )
        return client

    def write_to_csv_file(self, path: str, values: Iterable[Dict[str, Any]]):
        path = self.get_absolute_path(path)
        max_azure_allowed_length = 4194303
        logger.info(f"Start uploading file {path} to blob storage")

        blob = self.__blob_from_uri(path, "w")
        blob.create_append_blob()
        try:
            first_item = next(values)
        except StopIteration:
            logger.info(f"Cannot write {path} have no data")
        header = list(first_item.keys())
        stream, wrapper, writer = _get_csv_stream(header)
        writer.writeheader()
        writer.writerow(first_item)
        count = 1
        for count, value in enumerate(values, 2):
            if count % 1000 == 0:
                logger.info(f"{count} rows uploaded to file {path}")

            writer.writerow(value)
            length = wrapper.tell()
            while length > max_azure_allowed_length:
                wrapper.seek(0)
                # need to use origin bytes stream not text stream cause python http client  force encode to iso-8859-1
                blob.append_block(data=stream.read(max_azure_allowed_length), length=max_azure_allowed_length)
                residual_data = stream.read()
                logger.debug(
                    f"Uploaded {max_azure_allowed_length} bytes to file {path}, {length - max_azure_allowed_length} bytes left"
                )
                wrapper.close()
                stream.close()
                stream, wrapper, writer = _get_csv_stream(header)
                stream.write(residual_data)
                length = wrapper.tell()
        length = wrapper.tell()
        if length:
            wrapper.seek(0)
            blob.append_block(data=stream, length=length)
            logger.debug(f"Uploaded residual part of stream {length} bytes to file {path}")
        logger.info(f"File {path} successfully uploaded, count of rows: {count}")
        wrapper.close()
        stream.close()

    def upload_local_file(self, source: str, destination: str):
        """Upload single local file {source} to {destination}"""
        destination = self.get_absolute_path(destination)
        blob = self.__blob_from_uri(destination, "w")
        with open(source, "rb") as fid:
            fid.seek(0, 2)
            length = fid.tell()
            fid.seek(0)
            blob.upload_blob(data=fid, length=length, overwrite=True)

    def __copy_blob(self, source: "BlobClient", destination: "BlobClient"):
        """Copy file within Azure BLOB Storage from blob source to blob destination"""
        logger.info("Creating blob copy from %s to %s", source, destination)
        destination.start_copy_from_url(source_url=source.url)
        props = destination.get_blob_properties()
        while props.copy.status == "pending":
            time.sleep(COPY_POLL_INTERVAL)
            props = destination.get_blob_properties()

    def __copy(self, source: str, destination: str):
        """Copy file within Azure BLOB Storage from path source to path destination"""
        blob_source = self.__blob_from_uri(source)
        blob_dest = self.__blob_from_uri(destination)
        return self.__copy_blob(blob_source, blob_dest)

    def list_files(self, relative_path: str, suffix: Optional[str] = None):
        logger.info("Listing files in %s", relative_path)
        parser = urlparse(relative_path)
        container_name = parser.netloc or self.container_name
        prefix = parser.path.lstrip("/") or None
        if self.prefix and prefix and not parser.netloc:
            prefix = os.path.join(self.prefix, prefix)
            logger.info("Using relative prefix with absolute value: %s", prefix)
        container = self.__get_container(container_name)
        logger.info("Listing container / prefix: %s / %s", container.url, prefix)
        lst = container.list_blobs(name_starts_with=prefix)
        for blob in lst:
            if suffix and not blob["name"].endswith(suffix):
                continue
            # If returned blobs come from a subdirectory
            if prefix or self.prefix:
                residual = os.path.dirname(os.path.relpath(blob["name"], prefix or self.prefix))
                if residual:
                    logger.info(
                        "Skipping blob %s -> not in the immediate requested prefix (%s)", blob["name"], residual
                    )
                    continue
            logger.info("Returned blob %s", blob["name"])
            yield blob["name"]

    def __remove_blob(self, uri: str):
        """Remove blob"""
        blob = self.__blob_from_uri(uri, "d")
        blob.delete_blob()

    def clean_folder(self, path: str):
        """Delete all blobs with specified prefix {path}"""
        # ensure we delete folders only
        path = self.get_absolute_path(path)
        path = path.rstrip("/") + "/"
        parse = urlparse(path)
        container_name = parse.netloc or self.container_name
        blob_list = self.list_files(path, suffix=None)
        for child in blob_list:
            full_path = f"az://{container_name}/{child.lstrip('/')}"
            logger.warning("Removing BLOB %s", full_path)
            self.__remove_blob(full_path)

    def __az_blob_proxy(self, worker: AzureWorkerManager, cmd: str, _include_key: bool = True, **kwargs):
        key_part = f"--account-name '{self.account_name}' --account-key '{self.access_key}'"
        cmd = cmd.format(**kwargs) if kwargs else cmd
        fid = worker.run(f"{cmd} {key_part if _include_key else ''}", hide=True)
        if not fid.ok:
            logger.error("Proxy command %s failed.", cmd)
            logger.error(fid.stdout)
            logger.error(fid.stderr)
            raise Exception(f"Proxy command {cmd} failed")
        try:
            return json.loads(fid.stdout)
        except JSONDecodeError:
            logger.info(fid.stdout)
            return fid.stdout

    def download_file_to_worker(self, worker: AzureWorkerManager, source: str, destination: str):
        source = self.get_absolute_path(source)

        destination = destination.rstrip("/")
        if source.endswith("*"):
            dirname = source.rstrip("*")
            blob_list = (
                (blob_name, os.path.join(destination, os.path.basename(blob_name)))
                for blob_name in self.list_files(relative_path=dirname, suffix=None)
            )
        else:
            blob_list = [(source, os.path.join(destination, os.path.basename(source)))]
        for blob_source, destination_path in blob_list:
            logger.info(
                "Downloading file %s => %s on remote machine",
                blob_source,
                destination_path,
            )
            blob = self.__blob_from_uri(blob_source)
            container_name = blob.container_name
            name = blob.blob_name
            self.__az_blob_proxy(
                worker,
                (
                    f"mkdir -p `dirname '{destination_path}'`; az storage blob download --container-name '{container_name}' "
                    f"--name '{name}' --file '{destination_path}'"
                ),
            )

    def upload_files_from_worker(self, worker: AzureWorkerManager, data_volume_path: str):
        archive_storage_path = self.get_base_archive_path()
        logger.info("Uploading csv to live bucket")
        blob = self.__blob_from_uri(self.base_path)
        storage_path = blob.blob_name
        self.__az_blob_proxy(
            worker,
            (
                f'cd "{data_volume_path}" && '
                f'for f in $(compgen -G "*.csv"); '
                f'do echo "Uploading $f to {storage_path}/$f"; '
                f'az storage blob upload --container-name "{self.container_name}" '
                f'--name "{storage_path}/$f" --file "$f" '
                f'--account-name "{self.account_name}" --account-key "{self.access_key}"; '
                f"done"
            ),
            _include_key=False,
        )
        logger.info("Data uploaded to live bucket")
        logger.info("Creating data copy in archive bucket")
        for blob_name in self.list_files(self.base_path, suffix=".csv"):
            base = os.path.basename(blob_name)
            target_name = os.path.join(archive_storage_path, base)
            logger.info("Processing copy for %s => %s", blob_name, target_name)
            self.__copy(blob_name, target_name)
        logger.info("Data successfully copied to archive bucket")
