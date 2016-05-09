from pqtree import PQtree
from pqtree import reduce_tree, ReductionFailed
from pqnode import Type


def planar_testing(graph):
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
            tree.replace_full_children(pertinent_root, PQtree(subset1).get_root())
        else:
            tree.replace_node(pertinent_root, PQtree(subset1).get_root())
    return True

def linear_algorithm(graph):
    pass
