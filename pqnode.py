from enum import Enum


class Type(Enum):
    Q_NODE = 1
    P_NODE = 2
    LEAF = 3


class Label(Enum):
    FULL = 1
    EMPTY = 2
    PERTINENT = 3


class Mark(Enum):
    UNMARKED = 1
    QUEUED = 2
    BLOCKED = 3
    UNBLOCKED = 4


class PQnode(object):
    # TODO: Perhaps add more field as arguments
    def __init__(self, data=None):
        # Number of children nodes
        self.child_count = 0

        # Linked list of node's children. Used only by P-node.
        # TODO: perhaps double-linked list should be used instead
        self.circular_link = []

        # Reference to the last node's child. Used only by Q-node.
        self.endmost_children = None

        # Set of full node's children
        self.full_children = set()

        # Tuple of immediate sublings.
        # For children of P-node it just a (None, None)
        # For endmost children of Q-node it is (node, None) or (None, node)
        # For interior children of Q-node it is (None, None)
        self.left_subling = None
        self.right_subling = None
        self.immediate_sublings = (self.left_subling, self.right_subling)

        # Node's label: EMPTY, FULL or PARTIAL
        self.label = Label.EMPTY

        # Node's mark: UNMARKED, QUEUED(placed into queue), BLOCKED(hasn't pointer to parent)
        # and UNBLOCKED(when it receives pointer to parent node)
        self.mark = Mark.UNMARKED

        # Pointer to parent node.
        self.parent = None

        # Set of all partial children of the node
        self.partial_children = set()

        # Number of pertinent children
        self.pertinent_child_count = 0

        # Number of pertinent leafs
        self.pertinent_leaf_count = 0

        # Node type: LEAF, P_NODE or Q_NODE
        self.node_type = Type.LEAF

        # Reference to node data(like id of edge)
        self.data = data

    def set_type(self, node_type: Type):
        self.node_type = node_type

    def set_parent(self, parent) -> None:
        assert \
            type(parent) == PQnode

        self.parent = parent

    def get_parent(self):
        return self.parent

    def set_data(self, data):
        self.data = data

    def set_mark(self, mark: Mark) -> None:
        self.mark = mark

    def get_mark(self) -> Mark:
        return self.mark

    def get_sublings(self) -> tuple:
        return self.immediate_sublings

    def get_left_subling(self):
        return self.left_subling

    def get_right_subling(self):
        return self.right_subling

    def get_num_sublings(self):
        count = 0
        if self.immediate_sublings[0] is None:
            count += 1
        if self.immediate_sublings[1] is None:
            count += 1
        return count

    def set_pertinent_child_count(self, new_value):
        self.pertinent_child_count = new_value

    def get_pertinent_child_count(self):
        return self.pertinent_child_count

    def inc_pertinent_child_count(self):
        self.pertinent_child_count += 1

    def add_child(self, child_node):
        self.child_count += 1
        self.circular_link.append(child_node)
        # For now always add new node to the end
        self.endmost_children = child_node

        # Just to make sure that parent reference is correct
        child_node.parent = self

        # TODO: add more 


if __name__ == "__main__":
    import doctest
    doctest.testmod()
