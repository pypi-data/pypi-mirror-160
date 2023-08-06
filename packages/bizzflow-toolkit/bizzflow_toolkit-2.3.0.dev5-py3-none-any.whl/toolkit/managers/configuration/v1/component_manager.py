import os

from toolkit.managers.configuration.component_manager import BaseComponentManagerLoader

class ComponentManagerLoader(BaseComponentManagerLoader):
    def _get_component_source(self, config, component_type=None) -> dict:
        component_source = config.get("component_source")
        if component_source is None:
            component_source = {}
            if component_type == "transformation":
                component_source["type"] = "local"
                component_source["path"] = os.path.join(
                    self.project_loader.project_path, f"{component_type}s", config["source"]
                )
            else:
                component_source["type"] = "bizztreat-gitlab"
        return component_source

    def _get_component_name(self, config, component_type=None) -> str:
        if component_type == "transformation":
            return config["source"]
        else:
            return config["type"]
