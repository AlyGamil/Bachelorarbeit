import itertools
import pprint

from ConfigurationElement import ConfigurationElement
from ConfigurationNode import ConfigurationNode
from Element import Element
from Node import Node
from TopologyElement import TopologyElement
from TopologyNode import TopologyNode
from Types import Types

b6 = "igbt1 1 2 u; diode1 u 1; " \
     "igbt2 1 3 v; diode2 v 1;" \
     "igbt3 1 4 w; diode3 w 1;" \
     "igbt4 u 5 0; diode4 0 u;" \
     "igbt5 v 6 0; diode5 0 v; " \
     "igbt6 w 7 0; diode6 0 w;"

variant1 = 'igbt1 1 2 3;diode1 3 1;' \
           'igbt2 3 4 v;diode2 v 3;' \
           'igbt3 v 5 6;diode4 6 v;' \
           'igbt4 6 7 0;diode4 0 6;' \
           'diode5 u 3;diode6 6 u;'

variant3 = 'igbt1 1 2 v;diode1 v 1;igbt2 v 3 0;diode2 0 v;igbt3 v 4 5;diode3 5 u;igbt4 u 6 5;diode4 6 v;'
variant4 = 'igbt1 1 2 3;diode1 3 1;igbt2 3 4 0;diode2 0 3;diode3 5 3;'
test_topo = 'diode1 1 2; diode2 2 4; igbt1 2 3 4;'
single_switch = 'diode n3 n1;igbt n1 n2 n3;'  # IGBT co-pack
chopper2 = 'diode1 n3 n1;diode2 n0 n3;igbt n1 n2 n3'  # chopper 2
chopper1 = 'diode1 n0 n2;diode2 n2 n1;igbt n2 n3 n0'  # chopper 1
test_configuration = 'diode1 n1 n2;igbt1 n2 n3 n4;'

topo = variant4
configuration = chopper2


def netlist_to_oop(t: str, topology_type: bool):
    if topology_type:
        node_type = TopologyNode
        element_type = TopologyElement
    else:
        node_type = ConfigurationNode
        element_type = ConfigurationElement
        ConfigurationNode.nodes = []

    parts = t.split(';')
    for i in parts:
        i = i.lstrip()

        # element name
        element = i.split(' ')[0]

        # string of the nodes
        nodes = i.split(' ')[1:]

        # list of nodes
        nodes_list = []

        for n in nodes:
            # skip if node exists
            if n not in node_type.nodes:
                nodes_list.append(node_type(n))

            else:

                # create a new node
                nodes_list.append(node_type.get_node(n))

        # create a new element with its nodes
        element = element_type(element, nodes_list)

        # append the element of the list of connections of each node
        if element.typ is Types.DIODE:
            nodes_list[0].add_connection(element, Types.DIODE_ANODE)
            nodes_list[1].add_connection(element, Types.DIODE_CATHODE)

        if element.typ is Types.IGBT:
            nodes_list[0].add_connection(element, Types.IGBT_COLLECTOR)
            nodes_list[1].add_connection(element, Types.IGBT_GATE)
            nodes_list[2].add_connection(element, Types.IGBT_EMITTER)


# {'n0': [3, v, 6, 0, u], 'n1': [1, 3, v, 6], 'n2': [2, 4, 5, 7], 'n3': [3, v, 6]}
def sub_graph_matches():
    topology_nodes = TopologyNode.nodes.copy()
    configuration_nodes = ConfigurationNode.nodes.copy()

    similar_nodes = {}
    for i in configuration_nodes:
        similar_nodes.update({i.name: []})

    for topo_node in topology_nodes:
        for confi_node in configuration_nodes:
            if set(confi_node.terminals) <= set(topo_node.terminals):
                similar_nodes[confi_node.name].append(topo_node)

    return similar_nodes


# todo create sub-topology and check it can be built from the same configuration
# todo sub-topology could be created from the extracted matches


netlist_to_oop(topo, True)
netlist_to_oop(configuration, False)


def dfs(node, visited):  # depth First Search

    if node not in visited:
        visited.append(node)
        for connection in node.connections:
            dfs(connection, visited)
    return visited


def get_next_nodes(node: Node):
    next_nodes = set()
    for c in node.connections:
        connections = c.connections.copy()
        connections.remove(node)
        next_nodes.update(connections)
    return list(next_nodes)


def paths(vertex):
    path = [vertex]  # path traversed so far
    seen = {vertex}  # set of vertices in path

    def search():
        dead_end = True
        connections = get_next_nodes(path[-1])
        for neighbour in connections:  # last element in path. connections
            if neighbour not in seen:
                dead_end = False
                seen.add(neighbour)
                path.append(neighbour)
                yield from search()
                path.pop()
                seen.remove(neighbour)
        if dead_end:
            yield list(path)

    yield from search()


def old_match():
    for confi_node in ConfigurationNode.nodes:
        for topo_node in TopologyNode.nodes:
            path = [topo_node]
            seen = {topo_node}

            def dfs_match():
                dead_end = True
                if set(confi_node.terminals) <= set(path[-1].terminals):
                    connections = get_next_nodes(path[-1])
                    for connection in connections:
                        if connection not in seen:
                            if set(confi_node.terminals) <= set(connection.terminals):
                                dead_end = False

                if dead_end:
                    if len(path) > 1:
                        yield list(path)

            yield from dfs_match()


# print(list(old_match()))
combinations = []


def compare_paths(topo_path, confi_path):
    path = []
    confi_length = len(confi_path)
    topo_length = len(topo_path)

    for i in range(confi_length):
        if confi_length <= topo_length:
            t_node = topo_path[i]
            c_node = confi_path[i]
            if set(c_node.terminals) <= set(t_node.terminals):
                path.append((t_node, c_node))
            else:
                return
    if path:
        combinations.append(path)


def possible_paths():
    for topo_node in TopologyNode.nodes:
        for confi_node in ConfigurationNode.nodes:

            topo_paths = list(paths(topo_node))
            confi_paths = list(paths(confi_node))

            for topo_path in topo_paths:
                for confi_path in confi_paths:

                    if len(confi_path) <= len(topo_path):
                        compare_paths(topo_path, confi_path)


def refine_combinations():
    length = len(max(combinations, key=len))
    possible_combination = [i for i in combinations if len(i) == length]

    return possible_combination


possible_paths()
# combinations_set = set(tuple(x) for x in refine_combinations())
# c = [list(x) for x in combinations_set]
# pprint.pprint(refine_combinations())
# pprint.pprint(c)
