class Configuration:
    configurations_objects = []

    def __init__(self, name):
        self.name = name
        Configuration.configurations_objects.append(self)
        self.nodes = []
        self.elements = []

    def __repr__(self):
        return self.name

    @staticmethod
    def get_node(name: str):
        for c in Configuration.configurations_objects:
            for n in c.nodes:
                if n == name:
                    return n
