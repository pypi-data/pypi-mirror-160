from toolkit.managers.configuration.base import ConfigurationManager


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CurrentConfigurationManager(ConfigurationManager, metaclass=Singleton):
    pass


# It just init class but all load are lazy
current_config = CurrentConfigurationManager()
