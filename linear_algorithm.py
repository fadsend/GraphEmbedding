from pqtree import PQtree
from pqtree import reduce_tree, ReductionFailed
from pqnode import Type


def upward_embed(graph):
    universe = graph.get_edges_lower(1)
    n = graph.get_num_of_vertices()
    tree = PQtree(universe)
    for i in range(2, n + 1):
        subset = graph.get_edges_higher(i)
        # if len(subset) == 0:
        #    continue
        tree = reduce_tree(tree, subset)
        # try:
        #    tree = reduce_tree(tree, subset)
        # except ReductionFailed:
        #    return False

        subset1 = graph.get_edges_lower(i)

        # Save pertinent root before its re-written on the next iteration
        pertinent_root = tree.get_pertinent_root(subset)
        assert pertinent_root is not None

        if pertinent_root.node_type == Type.Q_NODE:
            adj_list = tree.replace_full_children(pertinent_root, PQtree(subset1, True).get_root())
        else:
            adj_list = tree.replace_node(pertinent_root, PQtree(subset1, True).get_root())

        print(tree)
        tmp123 = [tmp.data.data.vertices[0] for tmp in adj_list]
        for vertex in tmp123:
            graph.new_adj_list[i].append(vertex)

    print(graph.new_adj_list)
    return True

# Assumed that upward_embed has been called for graph
def embed(graph):
    pass
