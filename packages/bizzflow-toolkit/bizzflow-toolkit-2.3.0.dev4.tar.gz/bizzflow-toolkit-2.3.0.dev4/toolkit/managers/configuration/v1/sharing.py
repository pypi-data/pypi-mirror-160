from toolkit.managers.configuration.sharing import BaseSharingLoader
from toolkit.managers.configuration.v1.validators import SharingValidator


class SharingLoader(BaseSharingLoader):
    validatorClass = SharingValidator
