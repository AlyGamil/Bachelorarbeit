import pprint
import time

from Combination import Combination
from CombinationNode import CombinationNode
from Configuration import Configuration
from ConfigurationElement import ConfigurationElement
from ConfigurationNode import ConfigurationNode
from Module import Module
from Node import Node
from TopologyElement import TopologyElement
from TopologyNode import TopologyNode
from Types import Types

start_time = time.time()

b6_bridge = "igbt1 1 2 u; diode1 u 1; " \
            "igbt2 1 3 v; diode2 v 1;" \
            "igbt3 1 4 w; diode3 w 1;" \
            "igbt4 u 5 0; diode4 0 u;" \
            "igbt5 v 6 0; diode5 0 v;" \
            "igbt6 w 7 0; diode6 0 w;"

variant1 = 'igbt1 1 2 3;diode1 3 1;' \
           'igbt2 3 4 v;diode2 v 3;' \
           'igbt3 v 5 6;diode4 6 v;' \
           'igbt4 6 7 0;diode4 0 6;' \
           'diode5 u 3;diode6 6 u;'

variant3 = 'igbt1 1 2 v;diode1 v 1;igbt2 v 3 0;diode2 0 v;igbt3 v 4 5;diode3 5 u;igbt4 u 6 5;diode4 5 v;'
variant4 = 'igbt1 1 2 3;diode1 3 1;igbt2 3 4 0;diode2 0 3;diode3 5 3;'

variant6 = "igbt_q1 1 2 3;diode_q1 3 1;igbt_q2 3 4 v;diode_q2 v 3;" \
           "igbt_q3 v 5 6;diode_q3 6 v;igbt_q4 6 7 0;diode_q4 0 6;" \
           "igbt_q5 3 8 u;diode_q5 u 3;igbt_q6 u 9 6;diode_q6 6 u;"

h_bridge = "igbt1 1 2 u; diode1 u 1; " \
           "igbt2 1 3 v; diode2 v 1;" \
           "igbt4 u 5 0; diode4 0 u;" \
           "igbt5 v 6 0; diode5 0 v;"

topology = variant4

configurations = {
    'diode': 'diode n1 n2;',
    'igbt': 'igbt n1 n2 n3;',
    'single_switch': 'diode n3 n1;igbt n1 n2 n3;',
    'half_bridge': 'igbt1 n1 n2 n3; diode1 n3 n1; diode2 n5 n3; igbt2 n3 n4 n5;',
    'chopper1': 'diode1 n0 n2;diode2 n2 n1;igbt n2 n3 n0',
    'chopper2': 'diode1 n3 n1;diode2 n0 n3;igbt n1 n2 n3',
}


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
        n = i
        if n not in TopologyNode.nodes:
            nodes_list.append(TopologyNode(n))

        else:
            nodes_list.append(TopologyNode.get_node(n))
    return nodes_list


def netlist_configuration_to_oop(configurations_dictionary):
    for key in configurations_dictionary.keys():
        confi = Configuration(key)
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
                        new_node = ConfigurationNode(n, confi)
                        sorted_nodes_list.append(new_node)
                    else:
                        sorted_nodes_list.append(Configuration.get_node(n))

                confi.nodes.extend(sorted_nodes_list)
                confi.nodes = list(set(confi.nodes))

                # create a new element with its nodes
                element = ConfigurationElement(element, sorted_nodes_list)

                add_connections_to_nodes(element, sorted_nodes_list)
                sorted_nodes_list = []

        # configurations_objects.append(confi)


def netlist_topology_to_oop(topology_netlist: str):
    parts = topology_netlist.split(';')
    for i in parts:
        i = i.lstrip()

        # element name
        element = i.split(' ')[0]

        if element:
            # string of the nodes
            nodes_as_string = i.split(' ')[1:]

            # list of nodes
            nodes_list = create_topology_nodes(nodes_as_string)

            # create a new element with its nodes
            element = TopologyElement(element, nodes_list)

            add_connections_to_nodes(element, nodes_list)


netlist_topology_to_oop(topology)
netlist_configuration_to_oop(configurations)


def get_next_nodes(node: Node):
    next_nodes = set()
    for c in node.connections:
        connections = c.connections.copy()
        connections.remove(node)
        next_nodes.update(connections)
    return list(next_nodes)


def all_paths(vertex, configuration):
    configuration_nodes = configuration.nodes
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
                # if len(path) == len(configuration_nodes):
                #     yield list(path)
                path.pop()
                seen.remove(connection)
        if dead_end:
            if len(path) == len(configuration_nodes):
                yield list(path)

    if 'diode' in configuration.name or 'igbt' in configuration.name:
        # for diodes and transistors (single element)
        next_nodes = get_next_nodes(vertex)
        for next_node in next_nodes:
            path.append(next_node)
        yield path
    else:

        yield from search()


def get_elements_on_path(topo_nodes):
    elements = []
    common_elements = set()

    for node1 in topo_nodes:
        for node2 in topo_nodes:
            if node1 is not node2:
                x = node2.connections
                y = node1.connections
                common_elements.update(set(node2.connections).intersection(node1.connections))

    if common_elements:
        for element in common_elements:

            # to avoid adding an IGBT or MOSFET with just two nodes
            if set(element.connections).issubset(topo_nodes):
                elements.append(element)

    return set(elements)


def get_corresponding_elements(topo_nodes):
    elements = []

    for element in TopologyElement.elements:
        if set(element.connections) == set(topo_nodes):
            elements.append(element)
    return elements


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
    # print(topo_path)
    # print(confi_path)
    for i in range(len(confi_path) - 1):
        if len(topo_path) >= len(confi_path):

            topo_node = topo_path[i]
            next_topo_node = topo_path[i + 1]
            confi_node = confi_path[i]
            next_confi_node = confi_path[i + 1]
            if set(confi_node.terminals).issubset(set(topo_node.terminals)):

                if element_same_direction([topo_node, next_topo_node], [confi_node, next_confi_node]):
                    path.append((topo_node, confi_node))
            else:
                return

    if set(confi_path[-1].terminals).issubset(set(topo_path[-1].terminals)):
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


def taken_topology_nodes(layouts_tuple):
    return list(set([j[0] for j in layouts_tuple]))


def taken_configuration_nodes(layouts_tuple):
    return list(set([j[1] for j in layouts_tuple]))


def possible_layouts(configuration):
    configurations_nodes = configuration.nodes
    routes = []
    topo_paths = []
    confi_paths = []
    accepted_routes = []

    for topo_node in TopologyNode.nodes:
        topo_paths.extend(all_paths(topo_node, configuration))

    for confi_node in configurations_nodes:
        confi_paths.extend(all_paths(confi_node, configuration))

    for topo_path in topo_paths:
        for confi_path in confi_paths:

            route = compare_paths(topo_path, confi_path)
            # route = list(compare_routes(topo_path, confi_path))
            if route and len(route) == len(confi_path):
                route = set(route)

                if route not in routes:
                    routes.append(route)
                    if 'diode' in configuration.name or 'igbt' in configuration.name:
                        route = list(route)
                        route.sort(key=lambda tup: tup[1])
                        accepted_routes.append(route)
                    elif not route_split_single_switch(route):
                        route = list(route)
                        route.sort(key=lambda tup: tup[1])
                        accepted_routes.append(route)

    return accepted_routes


def all_possible_layouts():
    all_possibilities = []
    for conf in Configuration.configurations_objects:
        results = possible_layouts(conf)
        all_possibilities.extend(results)

    return all_possibilities


# pprint.pprint(all_possible_layouts())
# print(len(all_possible_layouts()))

def combinations(layouts_to_permute, topology_elements, current_permutation=None):
    current_permutation = [] if not current_permutation else current_permutation

    for module in layouts_to_permute:

        if topology_elements:

            # topology nodes in the module
            nodes = taken_topology_nodes(module)

            # topology elements on these nodes
            # todo differentiate between elements and modules
            # corresponding_elements = list(get_elements_on_path(nodes))
            corresponding_elements = list(get_corresponding_elements(nodes))

            # elements of the module are a subset of (exist in) the remaining elements
            if set(corresponding_elements).issubset(set(topology_elements)):

                remaining_elements_length = len(topology_elements)

                # remove used elements from the topology
                topology_elements = [i for i in topology_elements if i not in corresponding_elements]

                # check if the module has been used
                # by checking if elements have been remove
                # from the copied topology elements list
                if remaining_elements_length > len(topology_elements):
                    current_permutation.append(module)
                    next_permutation = current_permutation
                    remaining_elements = layouts_to_permute.copy()
                    remaining_elements.remove(module)

                    yield from combinations(layouts_to_permute=remaining_elements,
                                            topology_elements=topology_elements,
                                            current_permutation=next_permutation)

                    next_permutation.pop()
                    topology_elements.extend(corresponding_elements)

        else:
            yield current_permutation.copy()


permutations = list(combinations(all_possible_layouts(), TopologyElement.elements.copy()))


def sub_graph_matches():
    topology_nodes = TopologyNode.nodes.copy()
    configuration_nodes = Configuration.configurations_objects[2].nodes

    similar_nodes = {}
    for i in configuration_nodes:
        similar_nodes.update({i.name: []})

    for confi_node in configuration_nodes:
        for topo_node in topology_nodes:

            if set(confi_node.terminals) <= set(topo_node.terminals):
                similar_nodes[confi_node.name].append(topo_node)

    return similar_nodes


# pprint.pprint(permutations)
# print(len(permutations))

def remove_duplication(perms):
    final_combinations = []

    for perm in perms:
        modules = set()
        for module in perm:
            modules.add(tuple(module))
        if modules not in final_combinations:
            final_combinations.append(modules)

    return final_combinations


pprint.pprint(remove_duplication(permutations))
print(len(remove_duplication(permutations)))


# pprint.pprint(sub_graph_matches())


########################################################################

def create_combinations_oop():
    for combination in remove_duplication(permutations):
        new_combination = Combination()
        new_combination.nodes = [CombinationNode(i.name) for i in TopologyNode.nodes]
        for module in combination:
            paar = module[0]
            confi_node = paar[1]
            nodes_name = taken_topology_nodes(module)
            module_nodes = []

            for node in new_combination.nodes:
                if node in nodes_name:
                    module_nodes.append(node)

            new_module = Module(confi_node.configuration, module_nodes, new_combination)
            new_combination.modules.append(new_module)

            for node in module_nodes:
                node.connections.append(new_module)


create_combinations_oop()


def get_next_module(module):
    next_modules = set()
    for node in module.nodes:
        connections = node.connections.copy()
        connections.remove(module)
        next_modules.update(connections)
    return list(next_modules)


def recursive(connected_modules):
    if connected_modules:
        if all(element == connected_modules[0] for element in connected_modules) and len(connected_modules) > 1:
            pass


def next_module(module: Module, vertex):
    nodes = module.nodes.copy()
    nodes.remove(vertex)
    seen = set()
    for node in nodes:
        c = node.connections
        c.remove(module)
        seen.update(c)
    return list(seen)


def next_node_in_combinations(node: CombinationNode):
    nodes = []
    for c in node.connections:
        nodes = c.nodes.copy()
        nodes.remove(node)
    return nodes


def common_modules(node1: CombinationNode, node2: CombinationNode):
    return set(node1.connections).intersection(set(node2.connections))


visited = []  # List for visited nodes.
queue = []  # Initialize a queue


def bfs(visited, node):  # function for BFS
    node = f'{topology=}'.split('=')[0] + '_' + node
    center_node = Combination.combinations[0].get_node(node)
    visited.append(center_node)
    queue.append(center_node)

    while queue:  # Creating loop to visit each node
        n = queue.pop(0)
        # print(n, next_node_in_combinations(n))
        for neighbour in next_node_in_combinations(n):
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)


def foo(vertex):
    center_node = f'{topology=}'.split('=')[0] + '_' + vertex

    # for combination in Combination.combinations:
    # connected_modules = list(combination.get_connected_modules_by_node(center_node))
    # for module1 in connected_modules:
    #     next_module(module1, center_node)
    # for module2 in connected_modules:
    #     if module1.configuration == module2.configuration:
    #         if module1 is not module2:
    #             print(connected_modules)
    # print(get_next_module(connected_modules[0]))


print("--- %s seconds ---" % (time.time() - start_time))
