from Element import Element


class TopologyElement(Element):
    elements = []

    def __init__(self, name: str, connections: list):
        super().__init__(name, connections)
        TopologyElement.elements.append(self)

    @staticmethod
    def get_element(name: str):
        for e in TopologyElement.elements:
            if e.name == name:
                return e
