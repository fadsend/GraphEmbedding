from pqnode import Data, Type
from pqtree import PQtree, reduce_tree
import unittest


def convert_array(array):
    return [str(i) for i in array]


def check_consecutive(array, consecutive_elements_list):
    print("Result: " + str(array))

    if consecutive_elements_list == []:
        return False

    for consecutive in consecutive_elements_list:
        consecutive = convert_array(consecutive)
        if not __check_consequtive(array, consecutive):
            return False

    return True


def __check_consequtive(array, conseq_elements):
    if len(array) < len(conseq_elements):
        return False
    for i in range(len(array) - len(conseq_elements) + 1):
        if array[i] in conseq_elements:
            len_conseq = len(conseq_elements)
            for j in range(len_conseq):
                if not array[i + j] in conseq_elements:
                    return False
                conseq_elements.remove(array[i + j])
    return len(conseq_elements) == 0


class TestReduction(unittest.TestCase):

    def test1(self):
        data = [Data(i) for i in range(0, 7)]

        test_universe = data
        test_subset = data[1:3]
        T = PQtree(test_universe)
        T = reduce_tree(T, test_subset)
        tmp = [data[3], data[6], data[5]]
        T = reduce_tree(T, tmp)
        self.assertTrue(check_consecutive(T.get_frontier(), [[1, 2], [3, 6, 5]]))

    def test2(self):
        data = [Data(i) for i in range(0, 10)]
        test_universe = data
        test_subset = [data[i] for i in [1, 3, 5]]
        T = PQtree(test_universe)
        T = reduce_tree(T, test_subset)
        tmp = [data[i] for i in [5, 7]]
        T = reduce_tree(T, tmp)
        self.assertTrue(check_consecutive(T.get_frontier(), [[1, 3, 5], [5, 7]]))

    def test3(self):
        data = [Data(i) for i in range(0, 10)]
        test_universe = data
        test_subset = [data[i] for i in [0, 1, 2, 3, 4, 5]]
        T = PQtree(test_universe)
        T = reduce_tree(T, test_subset)
        tmp = [data[i] for i in [3, 4, 5]]
        T = reduce_tree(T, tmp)
        tmp = [data[i] for i in [2, 4, 5]]
        T = reduce_tree(T, tmp)
        tmp = [data[i] for i in [0, 3, 7]]
        print("------------------")
        T = reduce_tree(T, tmp)
        print(T)
        self.assertTrue(check_consecutive(T.get_frontier(), [[0, 1, 2, 3, 4, 5],
                                                             [3, 4, 5], [2, 4, 5],
                                                             [0, 3, 7]]))

    # Construct tree for checking P6 template
    def test4(self):
        tree = PQtree([])
        root = tree.get_root()
        data = [Data(i) for i in range(0, 10)]
        root.add_child(Type.LEAF, data[9])
        root.add_child(Type.LEAF, data[4])

        q1 = root.add_child(Type.Q_NODE, None)
        q1.add_child(Type.LEAF, data[5])
        q1.add_child(Type.LEAF, data[0])
        q1.add_child(Type.LEAF, data[6])

        root.add_child(Type.LEAF, data[2])
        root.add_child(Type.LEAF, data[7])

        q2 = root.add_child(Type.Q_NODE, None)
        q2.add_child(Type.LEAF, data[1])
        q2.add_child(Type.LEAF, data[8])
        q2.add_child(Type.LEAF, data[3])

        tree = reduce_tree(tree, [data[i] for i in [0, 7, 2, 6, 3, 8]])
        self.assertTrue(check_consecutive(tree.get_frontier(), [[0, 2, 3, 6, 7, 8]]))

    def test_Pnode_iterator(self):
        data = [Data(i) for i in range(0, 10, 2)]
        tree = PQtree(data)
        index = 0
        for child in tree.get_root().iter_children():
            self.assertEqual(child.data, data[index])
            index += 1

    def test_Qnode_iterator(self):
        tree = PQtree([])
        root = tree.get_root()
        qnode = root.add_child(Type.Q_NODE)
        data = [Data(i) for i in range(0, 10, 2)]
        new_data = [data[i] for i in [1, 3, 0, 4, 2]]

        for i in new_data:
            qnode.add_child(Type.LEAF, i)

        index = 0
        for child in qnode.iter_children():
            self.assertEqual(child, new_data[index])
            index += 1


if __name__ == "__main__":
    unittest.main()
