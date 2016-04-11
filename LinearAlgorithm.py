from pqtree import PQtree
from pqtree import Bubble, Reduce
from pqnode import Type


def planarTesting(workingGraph):
    graph = workingGraph.copy()
    graph.computeStNumbering()

    U = graph.getEdgesLower(1)
    n = graph.getNumOfVertices()
    T = PQtree(U, U)
    for i in range(2, n):
        S = graph.getEdgesHigher(i)
        T = Bubble(T, S)
        T = Reduce(T, S)
        if T is None:
            return False
        S1 = graph.getEdgesLower(i)
        if T.getRoot(S).nodeType == Type.Q_NODE:
            # FIXME: implement
            pass
        else:
            # FIXME: implement
            pass
        U = U.subtract(S.union(S1))
    return True


def linearAlgorithm(graph):
    pass
