from enum import Enum


class Types(Enum):
    DIODE = 1
    IGBT = 2
    DIODE_ANODE = 3
    DIODE_CATHODE = 4
    IGBT_COLLECTOR = 5
    IGBT_GATE = 6
    IGBT_EMITTER = 7

    def __repr__(self):
        return self.name
