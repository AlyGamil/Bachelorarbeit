from Element import Element
from Node import Node
from Types import Types


class ConfigurationNode(Node):
    nodes = []

    def __init__(self, name):
        super().__init__(name)
        ConfigurationNode.nodes.append(self)

    def add_connection(self, element: Element, terminal: Types):
        self.connections.append(element)
        self.terminals.append(terminal)
        self.element_and_terminal[element] = terminal

    @staticmethod
    def get_node(name: str):
        for n in ConfigurationNode.nodes:
            if n == name:
                return n
