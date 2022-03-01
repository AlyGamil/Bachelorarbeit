from Element import Element


class TopologyElement(Element):
    elements = []

    def __init__(self, name: str, connections: list):
        super().__init__(name, connections)
        TopologyElement.elements.append(self)
