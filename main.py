import itertools
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
# test = 'diode1 1 2; diode2 2 3; diode3 2 3;'
test = 'igbt1 n1 n2 n3; diode1 n3 n1; diode2 n5 n3; igbt2 n3 n4 n5;'
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
        # n = i
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

                # add element to his configuration
                confi.elements.append(element)

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


def all_paths(node, configuration):
    configuration_nodes = configuration.nodes
    path = [node]  # path traversed so far
    seen = {node}  # set of vertices in path

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

    if 'diode' in configuration.name:
        # for diodes and transistors (single element)
        next_nodes = get_next_nodes(node)
        for next_node in next_nodes:
            yield [node, next_node]
    else:
        yield from search()
    # yield from search()


def get_elements_on_path(nodes):
    elements = []
    common_elements = set()

    for node1 in nodes:
        for node2 in nodes:
            if node1 is not node2:
                common_elements.update(set(node2.connections).intersection(node1.connections))

    if common_elements:
        for element in common_elements:

            # to avoid adding an IGBT or MOSFET with just two nodes
            if set(element.connections).issubset(nodes):
                elements.append(element)

    return set(elements)


def get_corresponding_elements(nodes):
    elements = []

    if isinstance(nodes[0], TopologyNode):
        for element in TopologyElement.elements:
            if set(element.connections) == set(nodes):
                elements.append(element)

    if isinstance(nodes[0], ConfigurationNode):
        for element in ConfigurationElement.elements:
            if set(element.connections) == set(nodes):
                elements.append(element)
    return elements


def compare_elements_layouts(topo_nodes, confi_nodes):
    path = []
    topo_elements = get_corresponding_elements(topo_nodes)
    confi_elements = get_corresponding_elements(confi_nodes)

    if topo_elements and confi_elements:

        topo_element = topo_elements[0]
        confi_element = confi_elements[0]

        # determine the number of the terminals
        length = 2 if topo_element.typ is Types.DIODE and confi_element.typ is Types.DIODE else 3
        for j in range(length):  # collector -> gate -> emitter OR anode -> cathode

            topo_terminal = topo_nodes[j].element_and_terminal[topo_element]
            confi_terminal = confi_nodes[j].element_and_terminal[confi_element]
            path.append((topo_nodes[j], confi_nodes[j]))

            # do they have the same type of terminals
            if not topo_terminal == confi_terminal:
                return False

        return path

    return False


def elements_have_same_direction(topo_nodes: list, confi_nodes: list):
    if compare_elements_layouts(topo_nodes, confi_nodes):
        return True

    else:
        topo_element = confi_element = None

        for element in TopologyElement.elements:
            if element.typ is not Types.DIODE:
                connections = element.connections
                intersections = set(topo_nodes).intersection(set(connections))
                if len(intersections) >= 2:
                    topo_element = element
                    break

        for element in ConfigurationElement.elements:
            if element.typ is not Types.DIODE:
                connections = element.connections
                intersections = set(confi_nodes).intersection(set(connections))
                if len(intersections) >= 2:
                    confi_element = element
                    break

        if topo_element and confi_element:
            topo_terminal1 = topo_nodes[0].element_and_terminal[topo_element]
            topo_terminal2 = topo_nodes[1].element_and_terminal[topo_element]
            confi_terminal1 = confi_nodes[0].element_and_terminal[confi_element]
            confi_terminal2 = confi_nodes[1].element_and_terminal[confi_element]

            return topo_terminal1 == confi_terminal1 and topo_terminal2 == confi_terminal2

        return False


def compare_routes(topo_path: list, confi_path: list):
    t_path = topo_path.copy()
    c_path = confi_path.copy()

    def search_tree():
        topo_node = t_path.pop(0)
        confi_node = c_path.pop(0)
        if set(confi_node.terminals).issubset(set(topo_node.terminals)):
            if len(c_path) > 0:
                if elements_have_same_direction([topo_node, t_path[0]], [confi_node, c_path[0]]):
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

                    if elements_have_same_direction([topo_node, next_topo_node], [confi_node, next_confi_node]):
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


def taken_topology_nodes(layouts_tuple):
    return list(set([j[0] for j in layouts_tuple]))


def taken_configuration_nodes(layouts_tuple):
    return list(set([j[1] for j in layouts_tuple]))


def possible_layouts(configuration):
    one_element_configuration = 'diode' in configuration.name \
                                or 'igbt' in configuration.name \
                                or 'mosfet' in configuration.name
    routes = []
    topo_paths = []
    confi_paths = []
    accepted_routes = []

    for topo_node in TopologyNode.nodes:
        topo_paths.extend(all_paths(topo_node, configuration))

    for confi_node in configuration.nodes:
        confi_paths.extend(all_paths(confi_node, configuration))

    for topo_path in topo_paths:
        for confi_path in confi_paths:
            if one_element_configuration:
                route = compare_elements_layouts(topo_path, confi_path)
            else:
                route = compare_paths(topo_path, confi_path)
                # route = list(compare_routes(topo_path, confi_path))
            if route and len(route) == len(confi_path):
                route = set(route)

                if route not in routes:
                    routes.append(route)
                    if one_element_configuration:
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


layouts = all_possible_layouts()
# pprint.pprint(all_possible_layouts())
print(len(layouts))


def module_contain_one_element(layout):
    node_couple = layout[0]
    element_node = node_couple[1]
    return 'diode' in element_node.name or 'igbt' in element_node.name or 'mosfet' in element_node.name


# if len(topology_elements) == 0:
#     yield current_permutation.copy()
def modules_combinations(layouts_to_permute, topology_elements, current_permutation=None):
    current_permutation = [] if not current_permutation else current_permutation
    for module in layouts_to_permute:

        # if topology_elements:

        # topology nodes in the module
        nodes = taken_topology_nodes(module)

        # topology elements on these nodes
        if module_contain_one_element(module):
            corresponding_elements = list(get_corresponding_elements(nodes))
            # continue
        else:
            corresponding_elements = list(get_elements_on_path(nodes))

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

                if len(topology_elements) == 0:
                    yield current_permutation.copy()

                yield from modules_combinations(layouts_to_permute=remaining_elements,
                                                topology_elements=topology_elements,
                                                current_permutation=next_permutation)

                next_permutation.pop()
                topology_elements.extend(corresponding_elements)

    # else:
    #     yield current_permutation.copy()


def get_combinations(layouts):
    results = []
    for i in range(1, len(layouts) + 1):
        results.extend(list(itertools.combinations(layouts, i)))
    return results


def accepted_permutations(perms, left_component=0):
    combinations = []

    for perm in perms:

        modules = set()
        topology_elements = TopologyElement.elements.copy()

        for module in perm:
            if topology_elements:

                # topology nodes in the module
                nodes = taken_topology_nodes(module)

                # topology elements on these nodes
                elements = list(get_elements_on_path(nodes))

                # elements of the module are a subset of (exist in) the remaining elements
                if set(elements).issubset(set(topology_elements)):

                    remaining_elements_length = len(topology_elements)

                    # remove used elements from the topology
                    topology_elements = [i for i in topology_elements if i not in elements]

                    # check if the module has been used
                    # by checking if elements have been remove
                    # from the copied topology elements list
                    if remaining_elements_length > len(topology_elements):
                        modules.add(tuple(module))
        if modules:
            # how many elements allowed not be in modules combination
            if len(topology_elements) <= left_component:
                if modules not in combinations:
                    combinations.append(modules)

    return combinations


# pprint.pprint(all_possible_layouts())

# start_time = time.time()
permutations = list(modules_combinations(layouts, TopologyElement.elements.copy()))


# print(len(permutations))


# print(" combinations --- %s seconds ---" % (time.time() - start_time))


def remove_duplicated_modules_combinations(perms):
    final_combinations = []

    for perm in perms:
        modules = set()
        for module in perm:
            modules.add(tuple(module))
        if modules not in final_combinations:
            final_combinations.append(modules)

    return final_combinations


# start_time = time.time()
final_permutation = remove_duplicated_modules_combinations(permutations)
pprint.pprint(final_permutation)
print(len(final_permutation))
print(" remove_duplication --- %s seconds ---" % (time.time() - start_time))
