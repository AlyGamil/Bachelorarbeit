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
test_topo = 'igbt1 1 2 u; diode1 u 1; igbt5 v 6 0; diode5 0 v; diode6 0 w'
topo = variant4
igbt_co_pack = 'diode n3 n1;igbt n1 n2 n3;'  # IGBT co-pack
chopper2 = 'diode1 n3 n1;diode2 n0 n3;igbt n1 n2 n3'  # chopper 2
chopper1 = 'diode1 n0 n2;diode2 n2 n1;igbt n2 n3 n0'  # chopper 1
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


#  variant 1
# [1, igbt1, 2, 3, diode1, igbt2, 4, v, diode2, igbt3, 5, 6, diode4, igbt4, 7, 0, diode4, diode6, u, diode5]
# [n3, diode1, n1, igbt, n2, diode2, n0]
# variant 4
# [1, igbt1, 2, 3, diode1, igbt2, 4, 0, diode2, diode3, 5]
# [n3, diode1, n1, igbt, n2, diode2, n0]
def dfs(node, visited):  # depth First Search
    if node not in visited:
        visited.append(node)
        for connection in node.connections:
            dfs(connection, visited)
    return visited


def get_next_node(node: Node):
    next_nodes = set()
    for c in node.connections:
        connections = c.connections.copy()
        connections.remove(node)
        next_nodes.update(connections)
    return list(next_nodes)


x = []
v = []


def dfs_preparer(start, destination):  # depth First Search
    global v
    global x
    if start == destination:
        x = v
        v = []
        return x
    else:
        connections = get_next_node(start)
        v.append(start)
        for connection in connections:
            dfs_preparer(connection, destination)


temporary_approved = []
approved = []
visited_nodes = []


def save_temporary_nodes(node1, node2):
    x = set()
    x.add(node1)
    x.add(node2)
    if x not in temporary_approved:
        temporary_approved.append(x)


def dfs_match(confi_node, topo_node, visited):  # depth first Search
    global temporary_approved
    tested = set()
    tested.add(confi_node)
    tested.add(topo_node)
    confi_connections = get_next_node(confi_node)
    topo_connections = get_next_node(topo_node)
    if tested not in visited:
        visited.append(tested)

        for confi_connection in confi_connections:
            for i in range(len(topo_connections)):
                topo_connection = topo_connections[i]
                if set(confi_connection.terminals) <= set(topo_connection.terminals):
                    save_temporary_nodes(confi_connection, topo_connection)
                    dfs_match(confi_connection, topo_connection, visited)
                    if i == len(topo_connections) - 1:
                        if temporary_approved:
                            approved.append(temporary_approved)
                            temporary_approved = []


def matches():
    for confi_node in ConfigurationNode.nodes:
        for topo_node in TopologyNode.nodes:

            if set(confi_node.terminals) <= set(topo_node.terminals):
                save_temporary_nodes(confi_node, topo_node)
                dfs_match(confi_node, topo_node, visited_nodes)


def prepare_configuration_nodes():
    possibilities = []
    for start in ConfigurationNode.nodes:
        for end in ConfigurationNode.nodes:
            if start is not end:
                flatten_nodes = dfs_preparer(start, end)
                possibilities.append(flatten_nodes)
    return possibilities


def paths(vertex):
    path = [vertex]  # path traversed so far
    seen = {vertex}  # set of vertices in path

    def search():
        dead_end = True
        connections = get_next_node(path[-1])
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


# print(prepare_configuration_nodes())
node1 = ConfigurationNode.nodes[0]
y = paths(node1)
y = list(y)
print(y)
