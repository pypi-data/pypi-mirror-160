from toolkit.managers.configuration.datamarts import BaseDatamartLoader
from toolkit.managers.configuration.v1.validators import DatamartsValidator



class DatamartLoader(BaseDatamartLoader):
    validatorClass = DatamartsValidator
