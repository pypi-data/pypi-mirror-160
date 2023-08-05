# std
from fnmatch import fnmatch
from typing import List

# external
from braceexpand import braceexpand

# internal
from laz.model.path import Path
from laz.model.target import Target
from laz.model.tree import Node
from laz.utils.node import get_node_configuration, get_target_configuration


class Resolver:

    def __init__(self, node: Node, path: Path):
        self.node = node
        self.path = path

    def resolve(self) -> List[Target]:
        nodes = self.resolve_nodes()
        return self.resolve_targets(nodes)

    def resolve_nodes(self) -> List[Node]:
        patterns = list(braceexpand(self.path.base_pattern))
        nodes: List[Node] = []
        for node in self.node.nodes():
            name_path = self.get_name_path(node)
            if any(fnmatch(name_path, p) for p in patterns):
                nodes.append(node)
        return nodes

    def resolve_targets(self, nodes: List[Node]) -> List[Target]:
        configurations = []
        for node in nodes:
            node_configuration = get_node_configuration(node)
            for target_name in node_configuration.data.get('targets', {}).keys():
                if fnmatch(target_name, self.path.target):
                    target_configuration = get_target_configuration(node, target_name)
                    configurations.append(target_configuration)
        return configurations

    @staticmethod
    def get_name_path(node: Node) -> str:
        nodes = node.root_path()
        names = [node.configuration.name for node in nodes]
        return '/'.join(names + [''])
