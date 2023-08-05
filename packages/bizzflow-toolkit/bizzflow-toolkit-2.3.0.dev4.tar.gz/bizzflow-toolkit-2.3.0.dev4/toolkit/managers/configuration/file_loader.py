import logging
import os
from io import BytesIO
from typing import List, Optional, Tuple
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class BaseFileLoader:

    def get_file(self, path):
        raise NotImplementedError()

    def file_exists(self, path) -> bool:
        raise NotImplementedError()

    def list_directory(self, path: str) -> List[str]:
        raise NotImplementedError()


class LocalFileLoader(BaseFileLoader):

    def get_file(self, path):
        return open(path, "r")

    def file_exists(self, path) -> bool:
        raise NotImplementedError()

    def list_directory(self, path: str) -> List[str]:
        return os.listdir(path)


class S3FileLoader(BaseFileLoader):

    def __init__(self, profile: Optional[str] = None):
        self.profile = profile
        if profile:
            session = boto3.Session(profile_name=profile)
            self.resource = session.resource("s3")
        else:
            self.resource = boto3.resource("s3")

    def parse_path(self, path: str) -> Tuple[str, str]:
        """Parse path to bucket and key"""
        o = urlparse(path, allow_fragments=False)
        return o.netloc, o.path

    def file_exists(self, path: str) -> bool:
        """Check whether specified key exists"""
        bucket, key = self.parse_path(path)
        blob = self.resource.Object(bucket, key)
        try:
            blob.content_length
            return True
        except ClientError as error:
            if str(error.response.get("Error", {}).get("Code")) == "404":
                return False
            raise

    def get_file(self, path: str) -> BytesIO:
        """Get file by its key"""
        bucket, key = self.parse_path(path)
        obj = self.resource.Object(bucket, key)
        fid = BytesIO()
        obj.download_fileobj(fid)
        fid.seek(0)
        return fid

    def list_directory(self, path: str) -> List[str]:
        """List directory contents"""
        bucket, key = self.parse_path(path)
        bucket = self.resource.Bucket(bucket)
        path = key.rstrip("/") + "/"
        return [os.path.basename(obj.key) for obj in bucket.objects.filter(Prefix=path).all()]
