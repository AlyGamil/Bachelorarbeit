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
