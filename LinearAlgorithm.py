from pqtree import PQtree
from pqtree import bubble_tree, reduce_tree
from pqnode import Type
import copy


# def planar_testing(working_graph):
#     graph = copy.deepcopy(working_graph)
#     graph.compute_st_numbering()
#
#     U = graph.get_edges_lower(1)
#     n = graph.get_num_of_vertices()
#     T = PQtree(U, U)
#     for i in range(2, n):
#         S = graph.get_edges_higher(i)
#         T = bubble_tree(T, S)
#         T = reduce_tree(T, S)
#         if T is None:
#             return False
#         S1 = graph.get_edges_lower(i)
#         if T.getRoot(S).nodeType == Type.Q_NODE:
#             # FIXME: implement
#             pass
#         else:
#             # FIXME: implement
#             pass
#         U = U.subtract(S.union(S1))
#     return True



def planar_testing(working_graph):
    test_universe = {1, 2, 3, 4}
    test_subset = {2, 3}
    T = PQtree(test_universe, test_subset)
    print(T)


def linear_algorithm(graph):
    pass
