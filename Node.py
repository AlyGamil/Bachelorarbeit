from Element import Element


class Node:

    def __init__(self, name):
        self.name = name
        self.connections = []
        self.terminals = []

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return other == self.name

    def __hash__(self):
        return hash(self.name)
