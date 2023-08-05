from logging import getLogger
from typing import TYPE_CHECKING

from toolkit.managers.configuration.datamarts import BaseDatamartLoader
from toolkit.managers.configuration.v2.validators import DatamartsValidator

if TYPE_CHECKING:
    from toolkit.managers.configuration.v2.loader import V2ConfigurationLoader

logger = getLogger(__name__)


class DatamartLoader(BaseDatamartLoader):
    validatorClass = DatamartsValidator

    def __init__(self, project_loader: "V2ConfigurationLoader"):
        super().__init__(project_loader)
