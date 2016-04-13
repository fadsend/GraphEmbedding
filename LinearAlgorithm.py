from pqtree import PQtree
from pqtree import bubble, reduce
from pqnode import Type
import copy


def planar_testing(working_graph):
    graph = copy.deepcopy(working_graph)
    graph.compute_st_numbering()

    U = graph.get_edges_lower(1)
    n = graph.get_num_of_vertices()
    T = PQtree(U, U)
    for i in range(2, n):
        S = graph.get_edges_higher(i)
        T = bubble(T, S)
        T = reduce(T, S)
        if T is None:
            return False
        S1 = graph.get_edges_lower(i)
        if T.getRoot(S).nodeType == Type.Q_NODE:
            # FIXME: implement
            pass
        else:
            # FIXME: implement
            pass
        U = U.subtract(S.union(S1))
    return True


def linear_algorithm(graph):
    pass
