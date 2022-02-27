from Element import Element
from Node import Node
from Types import Types


class Connection:
    configurations_connections = []
    topology_connections = []

    def __init__(self, element1: Element, element_terminal1: Types, node: Node,
                 element2: Element, element_terminal2: Types):

        self.element1 = element1
        self.element_terminal1 = element_terminal1
        self.element2 = element2
        self.element_terminal2 = element_terminal2
        self.node = node

    def __repr__(self):
        return self.element1.name + ' ' + str(self.element_terminal1) + ' and ' + self.element2.name + ' ' + \
               str(self.element_terminal2) + ' in the node: ' + str(self.node)

    def __eq__(self, other):
        return self.element1.typ == other.element1.typ and self.element2.typ == other.element2.typ
