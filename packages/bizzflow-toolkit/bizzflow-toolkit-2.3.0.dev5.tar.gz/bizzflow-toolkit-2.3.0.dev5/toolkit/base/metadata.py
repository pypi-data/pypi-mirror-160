"""Object metadata
"""

import binascii
import json
import logging
import zlib
from base64 import b64decode, b64encode
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Optional

import dateutil.parser

from toolkit.utils.helpers import json_default

logger = logging.getLogger(__name__)


@dataclass
class ObjectMetadata:
    """Kex / Table metadata"""

    name: str
    description: Optional[str] = None
    component: Optional[str] = None
    user: Optional[str] = None
    created: datetime = field(default_factory=datetime.now)

    @property
    def payload(self) -> str:
        """Return base64 encoded, zlib-compressed JSON representation of metadata"""
        data = json.dumps(asdict(self), separators=(",", ":"), default=json_default).encode("utf-8")
        compressed = zlib.compress(data, level=9)
        return b64encode(compressed).decode("ascii")

    @staticmethod
    def from_payload(payload: str) -> "ObjectMetadata":
        """Return new ObjectMetadata instance from payload previously stored in database

        Raises:
            ValueError - Invalid payload
        """
        try:
            compressed = b64decode(payload)
        except binascii.Error as error:
            raise ValueError("Provided payload is invalid (failed to b64decode payload)") from error
        try:
            data = json.loads(zlib.decompress(compressed))
        except zlib.error as error:
            raise ValueError("Provided payload is invalid (failed to decompress zlib payload)") from error
        except json.decoder.JSONDecodeError as error:
            raise ValueError("Provided payload is invalid (failed to deserialize JSON)") from error
        created = data.pop("created", "1970-01-01T00:00:00")
        try:
            created_dt = dateutil.parser.isoparse(created)
        except ValueError:
            logger.error("Failed to parse date from metadata ('%s' is invalid datetime)", created, exc_info=True)
            created_dt = datetime.now()
        return ObjectMetadata(**data, created=created_dt)
