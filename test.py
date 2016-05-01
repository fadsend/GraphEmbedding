from pqnode import Data
from pqtree import PQtree, reduce_tree
import unittest


def check_consequtive(array, conseq_elements):
    print("Result: " + str(array))
    if len(array) < len(conseq_elements):
        return False
    for i in range(len(array) - len(conseq_elements)):
        if array[i] in conseq_elements:
            len_conseq = len(conseq_elements)
            for j in range(len_conseq):
                if not array[i + j] in conseq_elements:
                    return False
                conseq_elements.remove(array[i + j])
    return True


# TODO: Implement PQtree construction from string to allow
# more easy testing.
# TODO: Probably should be implemented as PQtree method
def construct_PQtree(str):
    return PQtree([], [])


class TestReduction(unittest.TestCase):

    def test1(self):
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
        T = reduce_tree(T, tmp)
        self.assertTrue(check_consequtive(T.get_frontier(), ['3', '6', '5']))

    def test2(self):
        data = [Data(i) for i in range(0, 10)]
        test_universe = data
        test_subset = [data[i] for i in [1, 3, 5]]
        T = PQtree(test_universe, test_subset)
        tmp = [data[i] for i in [5, 7]]
        T = reduce_tree(T, tmp)
        self.assertTrue(check_consequtive(T.get_frontier(), ['7', '5', '1', '3']))

    def test3(self):
        data = [Data(i) for i in range(0, 10)]
        test_universe = data
        test_subset = [data[i] for i in [0, 1, 2, 3, 4, 5]]
        T = PQtree(test_universe, test_subset)
        tmp = [data[i] for i in [3, 4, 5]]
        T = reduce_tree(T, tmp)
        tmp = [data[i] for i in [2, 4, 5]]
        T = reduce_tree(T, tmp)
        tmp = [data[i] for i in [0, 3, 7]]
        print("------------------")
        T = reduce_tree(T, tmp)
        print(T)
        self.assertTrue(check_consequtive(T.get_frontier(), ['0', '1', '2', '3', '4', '5', '7']))

if __name__ == "__main__":
    unittest.main()
