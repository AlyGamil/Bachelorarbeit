
# ignore this function
from Node import Node
from Types import Types


def step22():
    for node in Node.nodes:
        connections = node.connections.copy()
        if len(connections) > 1:  # parallel connection

            # get a list of IGBTs connected to this node
            igbt_list = [c for c in connections if c.type is Types.IGBT]

            # get a list of diodes connected to this node
            diode_list = [c for c in connections if c.type is Types.DIODE]

            for d in diode_list:
                for i in igbt_list:

                    # check if the diode and the igbt parallel to each other
                    if all(n in i.connections for n in d.connections):

                        # check if the IGBT Emitter connected to the diode anode
                        # the IGBT Collector connected to the diode cathode
                        # True? -> this is a co-pack
                        if d.connections[0] == i.connections[-1] and d.connections[-1] == i.connections[0]:
                            print('the diode: ' + d.name +
                                  ' and the IGBT: ' +
                                  i.name + ' build a co-pack')

