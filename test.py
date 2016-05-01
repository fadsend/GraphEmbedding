from pqnode import Data
from pqtree import PQtree, bubble_tree, reduce_tree


def check_consequtive(array, conseq_elements):
    for i in range(len(array) - len(conseq_elements)):
        if array[i] in conseq_elements:
            len_conseq = len(conseq_elements)
            for j in range(len_conseq):
                if not array[i + j] in conseq_elements:
                    return False
                conseq_elements.remove(array[i + j])
    return True


def run_tests():
    test1()
    test2()
    test3()


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
    check_consequtive(T.get_frontier(), ['3', '6', '5'])


def test2():
    data = [Data(i) for i in range(0, 10)]
    test_universe = data
    test_subset = [data[i] for i in [1, 3, 5]]
    T = PQtree(test_universe, test_subset)
    print(T.get_frontier())
    tmp = [data[i] for i in [5, 7]]
    T = bubble_tree(T, tmp)
    T = reduce_tree(T, tmp)
    assert(check_consequtive(T.get_frontier(), ['7', '5', '1', '3']))

def test3():
    data = [Data(i) for i in range(0, 10)]
    test_universe = data
    test_subset = [data[i] for i in [0, 1, 2, 3, 4, 5]]
    T = PQtree(test_universe, test_subset)
    print(T.get_frontier())
    tmp = [data[i] for i in [3, 4, 5]]
    T = bubble_tree(T, tmp)
    T = reduce_tree(T, tmp)
    tmp = [data[i] for i in [2, 4, 5]]
    T = bubble_tree(T, tmp)
    T = reduce_tree(T, tmp)
    tmp = [data[i] for i in [0, 3, 6]]
    T = bubble_tree(T, tmp)
    T = reduce_tree(T, tmp)
    print(T.get_frontier())
    assert(check_consequtive(T.get_frontier(), ['0', '1', '2', '3', '4', '5', '6']))


if __name__ == "__main__":
    run_tests()
