from Element import Element


class TopologyElement(Element):
    elements = []

    def __init__(self, name: str, nodes: list):
        super().__init__(name, nodes)
        TopologyElement.elements.append(self)
