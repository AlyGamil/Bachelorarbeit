from Element import Element
from Node import Node
from Types import Types


class TopologyNode(Node):
    nodes = []

    def __init__(self, name):
        super().__init__(name)
        TopologyNode.nodes.append(self)

    def add_connection(self, element: Element, terminal: Types):
        self.connections.append(element)
        self.terminals.append(terminal)
        self.element_and_terminal[element] = terminal

    @staticmethod
    def get_node(name: str):
        for n in TopologyNode.nodes:
            if n == name:
                return n



