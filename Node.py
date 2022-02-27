from Element import Element


class Node:
    h = 0

    def __init__(self, name):
        self.name = name
        Node.h += 1

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return other == self.name

