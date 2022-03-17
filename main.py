import pprint

from ConfigurationElement import ConfigurationElement
from ConfigurationNode import ConfigurationNode
from Node import Node
from TopologyElement import TopologyElement
from TopologyNode import TopologyNode
from Types import Types

b6_bridge = "igbt1 1 2 u; diode1 u 1; " \
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

variant3 = 'igbt1 1 2 v;diode1 v 1;igbt2 v 3 0;diode2 0 v;igbt3 v 4 5;diode3 5 u;igbt4 u 6 5;diode4 5 v;'
variant4 = 'igbt1 1 2 3;diode1 3 1;igbt2 3 4 0;diode2 0 3;diode3 5 3;'
test_topo = 'igbt1 1 2 3;diode1 3 1;' \
            'igbt2 3 4 v;diode2 v 3;' \
            'igbt3 v 5 6;diode4 6 v;' \
            'diode5 u 3;diode6 6 u;'
single_switch = 'diode n3 n1;igbt n1 n2 n3;'
chopper2 = 'diode1 n3 n1;diode2 n0 n3;igbt n1 n2 n3'
chopper1 = 'diode1 n0 n2;diode2 n2 n1;igbt n2 n3 n0'
test_configuration = 'diode1 n1 n2;igbt1 n2 n3 n4;'

topology = variant1
configuration = single_switch

configurations = {
    # 'single_switch': 'diode n3 n1;igbt n1 n2 n3;',
    'half_bridge': 'igbt1 n1 n2 n3; diode1 n3 n1; diode2 n5 n3; igbt2 n3 n4 n5;',
    'chopper1': 'diode1 n0 n2;diode2 n2 n1;igbt n2 n3 n0',
    'chopper2': 'diode1 n3 n1;diode2 n0 n3;igbt n1 n2 n3',
}
configurations_objects = []


def add_connections_to_nodes(element, nodes: list):
    # append the element of the list of connections of each node
    if element.typ is Types.DIODE:
        nodes[0].add_connection(element, Types.DIODE_ANODE)
        nodes[1].add_connection(element, Types.DIODE_CATHODE)

    if element.typ is Types.IGBT:
        nodes[0].add_connection(element, Types.IGBT_COLLECTOR)
        nodes[1].add_connection(element, Types.IGBT_GATE)
        nodes[2].add_connection(element, Types.IGBT_EMITTER)


def create_topology_nodes(nodes_as_string):
    nodes_list = []
    for i in nodes_as_string:
        n = f'{topology=}'.split('=')[0] + '_' + i

        if n not in TopologyNode.nodes:
            nodes_list.append(TopologyNode(n))

        else:
            nodes_list.append(TopologyNode.get_node(n))
    return nodes_list


def netlist_configuration_to_oop(configurations_dictionary):
    for key in configurations_dictionary.keys():
        confi = ConfigurationNode(key)
        value = configurations_dictionary[key]
        items = value.split(';')

        for i in items:
            if i:
                i = i.lstrip()

                # element name
                element = i.split(' ')[0]

                # string of the nodes
                nodes_as_string = i.split(' ')[1:]

                sorted_nodes_list = []

                for j in nodes_as_string:
                    n = str(key) + '_' + j

                    if n not in confi.nodes:
                        new_node = ConfigurationNode(n)
                        sorted_nodes_list.append(new_node)
                    else:
                        sorted_nodes_list.append(confi.get_node(n))

                # confi.nodes.extend(sorted_nodes_list.copy())

                confi.nodes.extend(sorted_nodes_list)
                confi.nodes = list(set(confi.nodes))

                # create a new element with its nodes
                element = ConfigurationElement(element, sorted_nodes_list)

                add_connections_to_nodes(element, sorted_nodes_list)
                sorted_nodes_list = []

        configurations_objects.append(confi)


def netlist_topology_to_oop(topology_netlist: str):
    parts = topology_netlist.split(';')
    for i in parts:
        i = i.lstrip()

        # element name
        element = i.split(' ')[0]

        # string of the nodes
        nodes_as_string = i.split(' ')[1:]

        # list of nodes
        nodes_list = create_topology_nodes(nodes_as_string)

        # create a new element with its nodes
        element = TopologyElement(element, nodes_list)

        add_connections_to_nodes(element, nodes_list)


netlist_topology_to_oop(topology)
netlist_configuration_to_oop(configurations)


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


# netlist_to_oop(topology, True)
# netlist_to_oop(configuration, False)


# {'n0': [3, v, 6, 0, u], 'n1': [1, 3, v, 6], 'n2': [2, 4, 5, 7], 'n3': [3, v, 6]}
def sub_graph_matches(confi):
    topology_nodes = TopologyNode.nodes.copy()
    configuration_nodes = confi.nodes.copy()

    similar_nodes = {}
    for i in configuration_nodes:
        similar_nodes.update({i.name: []})

    for topo_node in topology_nodes:
        for confi_node in configuration_nodes:
            if set(confi_node.terminals) <= set(topo_node.terminals):
                similar_nodes[confi_node.name].append(topo_node)

    return similar_nodes


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


def all_paths(vertex, configuration_nodes):
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
            if len(path) == len(configuration_nodes):
                yield list(path)

    yield from search()


def get_elements_on_path(topo_nodes):
    elements = []
    common_elements = set()

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


def element_same_direction(topo_nodes: list, confi_nodes: list):
    # common element
    topo_element = list(get_elements_on_path(topo_nodes))
    confi_element = list(get_elements_on_path(confi_nodes))

    # if common element exists check direction
    if topo_element and confi_element:

        # check if both the topology element terminal and the configuration element terminal are the same
        topo_terminal = topo_nodes[0].element_and_terminal[topo_element[0]]
        confi_terminal = confi_nodes[0].element_and_terminal[confi_element[0]]

        if topo_terminal == confi_terminal:
            return True

    # if there is no connection between the nodes return true
    elif len(topo_element) == 0 and len(confi_element) == 0:
        return True

    else:
        return False


def compare_routes(topo_path: list, confi_path: list):
    t_path = topo_path.copy()
    c_path = confi_path.copy()

    def search_tree():
        topo_node = t_path.pop(0)
        confi_node = c_path.pop(0)
        if set(confi_node.terminals).issubset(set(topo_node.terminals)):
            if len(c_path) > 0:
                if element_same_direction([topo_node, t_path[0]], [confi_node, c_path[0]]):
                    yield topo_node, confi_node
                    yield from search_tree()
            elif set(confi_node.terminals).issubset(set(topo_node.terminals)):
                yield topo_node, confi_node

    yield from search_tree()


def compare_paths(topo_path, confi_path):
    path = []

    for i in range(len(confi_path) - 1):
        if len(topo_path) >= len(confi_path):

            topo_node = topo_path[i]
            next_topo_node = topo_path[i + 1]
            confi_node = confi_path[i]
            next_confi_node = confi_path[i + 1]
            if set(confi_node.terminals).issubset(set(topo_node.terminals)):
                if set(next_confi_node.terminals).issubset(set(next_topo_node.terminals)):

                    if element_same_direction([topo_node, next_topo_node], [confi_node, next_confi_node]):
                        path.append((topo_node, confi_node))
            else:
                return

    path.append((topo_path[-1], confi_path[-1]))

    if len(path) == len(confi_path):
        return path
    else:
        return False


def detect_single_switches():
    for diode in TopologyElement.elements:
        for igbt in TopologyElement.elements:
            if diode.typ is Types.DIODE:
                if igbt.typ is Types.IGBT:
                    if igbt.connections[0] == diode.connections[1]:
                        if igbt.connections[2] == diode.connections[0]:
                            yield [diode, igbt]


def route_split_single_switch(route):
    single_switches = detect_single_switches()

    if route:
        topo_nodes = [i[0] for i in route]
        elements_on_route = get_elements_on_path(topo_nodes)
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
        topo_paths.extend(all_paths(topo_node, configurations_nodes))

    for confi_node in configurations_nodes:
        confi_paths.extend(all_paths(confi_node, configurations_nodes))

    for topo_path in topo_paths:

        for confi_path in confi_paths:

            route = compare_paths(topo_path, confi_path)
            # route = list(compare_routes(topo_path, confi_path))

            if route and len(route) == len(confi_path):
                route = set(route)

                if route not in routes:
                    routes.append(route)
                    if not route_split_single_switch(route):
                        route = list(route)
                        route.sort(key=lambda tup: tup[1])
                        accepted_routes.append(route)

    return accepted_routes
    # return accepted_routes, 'Number of used modules: ' + str(len(accepted_routes))


def taken_nodes(layouts_tuple):
    # return list(set([j[0] for layouts in layouts_tuple for j in layouts]))
    return list(set([j[0] for j in layouts_tuple]))


all_possibilities = []
for conf in configurations_objects:
    results = possible_layouts(conf.nodes)
    # pprint.pprint(results)
    all_possibilities.extend(results)

pprint.pprint(all_possibilities)

generated_permutations = []

# x1 = [(topology_1, half_bridge_n1),
#   (topology_2, half_bridge_n2),
#   (topology_3, half_bridge_n3),
#   (topology_4, half_bridge_n4),
#   (topology_v, half_bridge_n5)]
