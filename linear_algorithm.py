from pqtree import PQtree
from pqtree import reduce_tree
from pqnode import Data
from pqnode import Type
import copy


def planar_testing(graph):
    # graph = copy.deepcopy(working_graph)
    # graph.compute_st_numbering()

    universe = graph.get_edges_lower(1)
    n = graph.get_num_of_vertices()
    tree = PQtree(universe)
    # TODO: not sure if needed
    # tree = reduce_tree(tree, universe)
    for i in range(2, n):
        subset = graph.get_edges_higher(i)
        tree = reduce_tree(tree, subset)
        if tree.is_empty():
            return False
        subset1 = graph.get_edges_lower(i)
        # Save pertinent root before its re-written on the next iteration
        pertinent_root = tree.get_pertinent_root()
        assert pertinent_root is not None
        assert pertinent_root.node_type != Type.LEAF

        if pertinent_root.nodeType == Type.Q_NODE:
            tree.replace_full_children(pertinent_root, PQtree(subset1).get_root())
        else:
            tree.replace_node(pertinent_root, PQtree(subset1).get_root())

        # TODO: why need to subtract universe???
        # universe = universe.subtract(subset.union(subset1))
    return True

def linear_algorithm(graph):
    pass
