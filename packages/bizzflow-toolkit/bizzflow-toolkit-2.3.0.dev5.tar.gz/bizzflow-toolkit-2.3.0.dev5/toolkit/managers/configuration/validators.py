import json
import logging
import pathlib
from typing import List

from jsonschema import ValidationError, validate

from toolkit.managers.configuration.exceptions import ConfigurationNotValid
from toolkit.managers.configuration.file_loader import BaseFileLoader

logger = logging.getLogger(__name__)


class BaseConfigValidator:
    schema_file = NotImplemented
    schema_version = NotImplemented
    ref_files = ["_definitions.schema.json"]

    def __init__(self, file_loader: BaseFileLoader):
        self._schema = None
        self._file_loader = file_loader
        self.schemas_folder = pathlib.Path(__file__).parent / "schemas" / self.schema_version

    def _path_exists(self, path) -> bool:
        """Returns whether specified path exists in the context of the project"""
        return self._file_loader.file_exists(path)

    def _list_path(self, path: str) -> List[str]:
        """Returns list of paths within specified path"""
        return self._file_loader.list_directory(path)

    @property
    def schema(self):
        if self._schema is None:
            self._schema = self.load_schema()
        return self._schema

    def load_schema(self):
        full_path = self.schemas_folder / self.schema_file
        with open(full_path) as json_file:
            schema_text = json_file.read()
        for ref in self.ref_files:
            schema_text = schema_text.replace(ref, f"file://{self.schemas_folder}/{ref}")
        return json.loads(schema_text)

    def validate(self, config, *args, **kwargs):
        try:
            validate(config, self.schema)
        except ValidationError as e:
            logger.error("Configuration is not valid: %s", e)
            raise ConfigurationNotValid("Configuration is not valid: {}".format(e))
