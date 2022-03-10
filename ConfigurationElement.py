from Element import Element


class ConfigurationElement(Element):
    elements = []

    def __init__(self, name: str, connections: list):
        super().__init__(name, connections)
        ConfigurationElement.elements.append(self)

    @staticmethod
    def get_element(name: str):
        for e in ConfigurationElement.elements:
            if e.name == name:
                return e