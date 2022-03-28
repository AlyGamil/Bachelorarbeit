from Types import Types


class Element:

    def __init__(self, name: str, connections: list):
        self.typ = None
        self.name = name
        self.connections = connections
        self.get_element_type()

    def get_element_type(self):
        if 'DIODE' in self.name.upper():
            self.typ = Types.DIODE
        if 'IGBT' in self.name.upper():
            self.typ = Types.IGBT
        if 'MOSFET' in self.name.upper():
            self.typ = Types.MOSFET

    def __repr__(self):
        return self.name

    # def __repr__(self):
    #     return self.name + ' ' + str(self.typ) + ' ' + str(self.nodes)

