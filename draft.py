import main


def compare_paths(topo_path, confi_path):
    path = []

    for i in range(len(confi_path)):
        if len(topo_path) >= len(confi_path):

            topo_node = topo_path[i]
            confi_node = confi_path[i]

            # if set(c_node.terminals) <= set(t_node.terminals):
            if set(confi_node.terminals).issubset(set(topo_node.terminals)):
                path.append((topo_node, confi_node))
            else:
                return
    return path


def element_same_direction(topo_nodes: list, confi_nodes: list):
    # common element
    topo_element = list(main.get_elements_on_path(topo_nodes))
    confi_element = list(main.get_elements_on_path(confi_nodes))

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


# u = TopologyNode.get_node('u')
# v = TopologyNode.get_node('v')
# drei = TopologyNode.get_node('3')
# vier = TopologyNode.get_node('4')
# zero = TopologyNode.get_node('0')
# sieben = TopologyNode.get_node('7')
# n1 = ConfigurationNode.get_node('n1')
# n2 = ConfigurationNode.get_node('n2')
# n3 = ConfigurationNode.get_node('n3')
# n0 = ConfigurationNode.get_node('n0')
# test = [u, drei, v, vier]
# print(element_same_direction([zero, sieben], [n0, n3]))