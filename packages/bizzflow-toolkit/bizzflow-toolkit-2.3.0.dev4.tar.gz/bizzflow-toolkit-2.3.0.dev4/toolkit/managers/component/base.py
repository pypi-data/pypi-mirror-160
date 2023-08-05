import os


class BaseComponentManager:
    def __init__(self, component_type: str, component_name: str, component_id: str, component_config: dict):
        """

        Args:
            component_type: basic type of component transformation/extractor/writer
            component_name: name of component - ex_google, etc...
            component_id: specific component id
            component_config: specific component config
        """
        self.component_type = component_type
        self.component_name = component_name
        self.component_id = component_id
        self.component_config = component_config
        self.component_relative_path = os.path.join(self.component_type, self.component_id)
