from Element import Element


class ConfigurationElement(Element):
    elements = []

    def __init__(self, name: str, nodes: list):
        super().__init__(name, nodes)
        ConfigurationElement.elements.append(self)
