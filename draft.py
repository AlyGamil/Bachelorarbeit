import pprint

from ConfigurationElement import ConfigurationElement
from ConfigurationNode import ConfigurationNode
from Node import Node
from TopologyElement import TopologyElement
from TopologyNode import TopologyNode
from Types import Types

variant4 = 'igbt1 1 2 3;diode1 3 1;igbt2 3 4 0;diode2 0 3;diode3 5 3;'
topo = variant4
chopper2 = 'diode1 n3 n1;diode2 n0 n3;igbt n1 n2 n3'  # chopper 2


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


# todo sub-topology could be created from the extracted matches


netlist_to_oop(topo, True)
netlist_to_oop(chopper2, False)


def get_next_node(node: Node):
    next_nodes = set()
    for c in node.connections:
        connections = c.connections.copy()
        connections.remove(node)
        next_nodes.update(connections)
    return next_nodes


approved = []
temporary_approved = []
visited_nodes = []


def save_temporary_nodes(node1, node2):
    # x = set()
    # x.add(node1)
    # x.add(node2)
    # if x not in temporary_approved:
    #     temporary_approved.append(x)

    temporary_approved.append((node1, node2))


def dfs_match(confi_node, topo_node, visited):  # depth first Search
    global approved
    global temporary_approved
    tested = set()
    tested.add(confi_node)
    tested.add(topo_node)
    confi_connections = get_next_node(confi_node)
    topo_connections = get_next_node(topo_node)
    if tested not in visited:
        visited.append(tested)

        for confi_connection in confi_connections:
            for topo_connection in topo_connections:
                if set(confi_connection.terminals) <= set(topo_connection.terminals):
                    # print(str(confi_connection) + 'is a subset of ' + str(topo_connection))
                    save_temporary_nodes(confi_connection, topo_connection)
                    dfs_match(confi_connection, topo_connection, visited)
            print(temporary_approved)
            temporary_approved = []

        approved = temporary_approved
        temporary_approved = []


def matches():
    global temporary_approved
    for confi_node in ConfigurationNode.nodes:
        for topo_node in TopologyNode.nodes:

            if set(confi_node.terminals) <= set(topo_node.terminals):
                save_temporary_nodes(confi_node, topo_node)
                dfs_match(confi_node, topo_node, visited_nodes)


matches()
print(temporary_approved)
