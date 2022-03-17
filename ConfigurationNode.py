from Element import Element
from Node import Node
from Types import Types


class ConfigurationNode(Node):
    configurations_objects = []

    def __init__(self, name):
        super().__init__(name)
        self.nodes = []
        ConfigurationNode.configurations_objects.append(self)
        # self.nodes.append(self)

    def add_connection(self, element: Element, terminal: Types):
        self.connections.append(element)
        self.terminals.append(terminal)
        self.element_and_terminal[element] = terminal

    def get_node(self, name: str):
        for n in self.nodes:
            if n == name:
                return n
