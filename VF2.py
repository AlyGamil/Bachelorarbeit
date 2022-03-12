import main
from ConfigurationElement import ConfigurationElement
from ConfigurationNode import ConfigurationNode
from TopologyElement import TopologyElement
from TopologyNode import TopologyNode
from Types import Types


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


netlist_to_oop(main.topology, True)
netlist_to_oop(main.configuration, False)


def successors_of(n):
    path = [n]  # path traversed so far
    seen = {n}  # set of vertices in path

    def search():
        dead_end = True
        connections = main.get_next_nodes(path[-1])
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


def predecessors_of(n):
    successors = successors_of(n)
    for i in successors:
        if i[0] == n:
            i.reverse()
            yield i


one = TopologyNode.get_node('1')
two = TopologyNode.get_node('2')
three = TopologyNode.get_node('3')
four = TopologyNode.get_node('4')
five = TopologyNode.get_node('5')
six = TopologyNode.get_node('6')
seven = TopologyNode.get_node('7')
u = TopologyNode.get_node('u')
v = TopologyNode.get_node('v')
w = TopologyNode.get_node('w')
n1 = ConfigurationNode.get_node('n1')
n2 = ConfigurationNode.get_node('n2')
n3 = ConfigurationNode.get_node('n3')
print(list(successors_of(main.u)))
print(list(predecessors_of(main.u)))
