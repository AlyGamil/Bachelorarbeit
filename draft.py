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

