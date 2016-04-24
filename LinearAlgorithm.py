from pqtree import PQtree
from pqtree import bubble_tree, reduce_tree
from pqnode import Data
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



def test():
    data = [Data(0),
            Data(1),
            Data(2),
            Data(3),
            Data(4),
            Data(5),
            Data(6)]

    test_universe = data
    test_subset = data[1:3]
    T = PQtree(test_universe, test_subset)
    print(T)
    tmp = [data[3], data[6], data[5]]
    T = bubble_tree(T, tmp)
    T = reduce_tree(T, tmp)
    print("3, 6" in str(T))
    print(T)


def linear_algorithm(graph):
    pass
