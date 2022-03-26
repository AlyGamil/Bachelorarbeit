from Configuration import Configuration
from Combination import Combination


class Module:
    def __init__(self, configuration: Configuration, nodes: list, combination: Combination):
        self.configuration = configuration
        self.nodes = nodes
        self.combination = combination

    def __repr__(self):
        return str(self.configuration) + str(self.nodes)

    def __eq__(self, other):
        return (other.configuration, self.nodes) == (self.configuration, self.nodes)

    def __hash__(self):
        return hash(self.configuration)
