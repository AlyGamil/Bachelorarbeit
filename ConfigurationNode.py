from Configuration import Configuration
from Element import Element
from Node import Node
from Types import Types


class ConfigurationNode(Node):

    def __init__(self, name, configuration: Configuration):
        super().__init__(name)
        self.configuration = configuration
        configuration.nodes.append(self)
        # self.nodes.append(self)

    def add_connection(self, element: Element, terminal: Types):
        self.connections.append(element)
        self.terminals.append(terminal)
        self.element_and_terminal[element] = terminal


