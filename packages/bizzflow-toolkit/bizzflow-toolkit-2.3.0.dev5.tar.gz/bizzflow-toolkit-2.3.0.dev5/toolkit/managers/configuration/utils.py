import re
from collections import defaultdict
from typing import Union

from toolkit.managers.vault.base import BaseVaultManager


class Graph:
    def __init__(self, nodes: list):
        self.graph = defaultdict(list)
        self.nodes = nodes
        self.visited = {node: False for node in self.nodes}
        self.in_path = {node: False for node in self.nodes}

    def add_edge(self, start, end):
        assert start in self.nodes
        assert end in self.nodes
        self.graph[start].append(end)

    def _detect_sub_graph_cycle(self, node):
        self.visited[node] = True
        self.in_path[node] = True
        for neighbour in self.graph[node]:
            if not self.visited[neighbour]:
                if self._detect_sub_graph_cycle(neighbour):
                    return True
            elif self.in_path[neighbour]:
                return True
        self.in_path[node] = False
        return False

    def detect_cycle(self):
        for node in self.nodes:
            if not self.visited[node]:
                if self._detect_sub_graph_cycle(node):
                    return True
        return False


CREDENTIALS_RE = re.compile(r"^#!#:(?P<credentials_key>[a-zA-Z\d\-_]+)$")


def reveal_credentials(data: Union[str, dict, list], vault_manager: BaseVaultManager):
    """Replace credential substitution by real credential recursively using VaultManager instance.

    Args:
        data (str, dict | list): config part: dict, array of str
        vault_manager (BaseVaultManager): VaultManager to look for credentials in
    """
    if isinstance(data, str):
        match = CREDENTIALS_RE.match(data)
        if match:
            return vault_manager.get_credentials(match.group("credentials_key"))
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = reveal_credentials(value, vault_manager)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = reveal_credentials(item, vault_manager)
    return data
