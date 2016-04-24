from pqnode import Data
from pqtree import PQtree, bubble_tree, reduce_tree


def run_tests():
    test1()
    test2()


def test1():
    """
    Simple test in which P1 and P2 templates are used
    """
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
    tmp = [data[3], data[6], data[5]]
    T = bubble_tree(T, tmp)
    T = reduce_tree(T, tmp)
    frontier = T.get_frontier()
    assert("3, 6, 5" in ", ".join(frontier))


def test2():
    data = [Data(i) for i in range(0, 10)]
    test_universe = data
    test_subset = [data[i] for i in [1, 3, 5]]
    T = PQtree(test_universe, test_subset)
    print(T.get_frontier())
    tmp = [data[i] for i in [5, 7]]
    T = bubble_tree(T, tmp)
    T = reduce_tree(T, tmp)
    assert("7, 5, 1, 3" in ", ".join(T.get_frontier()))


if __name__ == "__main__":
    run_tests()
