import pprint

from ConfigurationElement import ConfigurationElement
from ConfigurationNode import ConfigurationNode
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
test_topo = 'igbt1 1 2 3;diode1 3 1;' \
            'igbt2 3 4 v;diode2 v 3;' \
            'igbt3 v 5 6;diode4 6 v;' \
            'diode5 u 3;diode6 6 u;'
single_switch = 'diode n3 n1;igbt n1 n2 n3;'
chopper2 = 'diode1 n3 n1;diode2 n0 n3;igbt n1 n2 n3'
chopper1 = 'diode1 n0 n2;diode2 n2 n1;igbt n2 n3 n0'
test_configuration = 'diode1 n1 n2;igbt1 n2 n3 n4;'

topology = test_topo
configuration = chopper1


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
        nodes_str = i.split(' ')[1:]

        # list of nodes
        nodes_list = []

        for n in nodes_str:

            if n not in node_type.nodes:
                nodes_list.append(node_type(n))

            else:

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


netlist_to_oop(topology, True)
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


def all_paths(vertex):
    path = [vertex]  # path traversed so far
    seen = {vertex}  # set of vertices in path

    def search():
        dead_end = True
        connections = get_next_nodes(path[-1])
        for connection in connections:
            if connection not in seen:
                dead_end = False
                seen.add(connection)
                path.append(connection)
                yield from search()
                path.pop()
                seen.remove(connection)
        if dead_end:
            if len(path) == len(ConfigurationNode.nodes):
                yield list(path)

    yield from search()


def compare_paths(topo_path, confi_path):
    path = []
    u = TopologyNode.get_node('u')
    v = TopologyNode.get_node('v')
    drei = TopologyNode.get_node('3')
    vier = TopologyNode.get_node('4')
    test = [u, drei, v, vier]
    x = [True if j in test else False for j in topo_path]
    for i in range(len(confi_path)):
        if len(topo_path) >= len(confi_path):

            t_node = topo_path[i]
            c_node = confi_path[i]
            # [(v, n0), (u, n1), (6, n2), (5, n3)]
            # [(v, n0), (u, n1), (3, n2), (4, n3)]

            if set(c_node.terminals) <= set(t_node.terminals):
                if all(x):
                    print(c_node)
                    print(c_node.terminals)
                    print(t_node)
                    print(t_node.terminals)
                    print()
                path.append((t_node, c_node))
            else:
                return
    if path:
        return path


def detect_single_switches():
    for diode in TopologyElement.elements:
        for igbt in TopologyElement.elements:
            if diode.typ is Types.DIODE:
                if igbt.typ is Types.IGBT:
                    if igbt.connections[0] == diode.connections[1]:
                        if igbt.connections[2] == diode.connections[0]:
                            yield [diode, igbt]


def get_elements_on_path(route):
    elements = []
    common_elements = set()
    topo_nodes = [i[0] for i in route]

    for node1 in topo_nodes:
        for node2 in topo_nodes:
            if node1 is not node2:
                common_elements.update(set(node2.connections).intersection(node1.connections))

    if common_elements:
        for element in common_elements:

            # to avoid adding an IGBT or MOSFET with just two nodes
            if set(element.connections).issubset(topo_nodes):
                elements.append(element)

    return set(elements)


def route_split_single_switch(route):
    single_switches = detect_single_switches()

    if route:
        elements_on_route = get_elements_on_path(route)
        for unit in single_switches:
            intersection = set(unit).intersection(elements_on_route)

            if len(intersection) == 1:
                return True

    return False


def possible_layouts(configurations_nodes):
    routes = []
    topo_paths = []
    confi_paths = []
    accepted_routes = []

    for topo_node in TopologyNode.nodes:
        topo_paths.extend(list(all_paths(topo_node)))

    for confi_node in configurations_nodes:
        confi_paths.extend(list(all_paths(confi_node)))

    for topo_path in topo_paths:
        for confi_path in confi_paths:
            route = compare_paths(topo_path, confi_path)

            if route:
                route = set(route)
                if route not in routes:
                    routes.append(route)
                    if not route_split_single_switch(route):
                        route = list(route)
                        route.sort(key=lambda tup: tup[1])
                        accepted_routes.append(route)

    return accepted_routes


results = possible_layouts(ConfigurationNode.nodes)
pprint.pprint(results)
