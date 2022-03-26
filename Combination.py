class Combination:
    combinations = []

    def __init__(self):
        self.modules = []
        self.nodes = []
        Combination.combinations.append(self)

    def get_connected_modules_by_node(self, node):
        for module in self.modules:
            if node in module.nodes:
                yield module

    def get_node(self, name):
        for n in self.nodes:
            if n.name == name:
                return n

    def __repr__(self):
        return str(self.modules)
