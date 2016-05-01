from enum import Enum


class Type(Enum):
    Q_NODE = 1
    P_NODE = 2
    LEAF = 3


class Label(Enum):
    FULL = 1
    EMPTY = 2
    PARTIAL = 3


class Mark(Enum):
    UNMARKED = 1
    QUEUED = 2
    BLOCKED = 3
    UNBLOCKED = 4


# Data class to store info in nodes. Also needed for cross-reference
# with node to speed up computations.
class Data(object):
    def __init__(self, data):
        self.data = data
        self.node_reference = None

    def __str__(self):
        return str(self.data)


class PQnode(object):
    # Counter to get unique id for each node. Useful for debugging.
    id_counter = 0

    # TODO: Perhaps add more field as arguments
    # TODO: add iterator for children of different types
    def __init__(self, node_type=Type.LEAF, data=None):
        # Number of children nodes
        # self.child_count = 0
        self.id = PQnode.id_counter
        PQnode.id_counter += 1

        # Linked list of node's children. Used only by P-node.
        # TODO: perhaps double-linked list should be used instead
        self.circular_link = []

        # Reference to the last node's child. Used only by Q-node.
        self.left_endmost = None
        self.right_endmost = None

        # Set of full node's children
        # TODO: change to linked list later
        self.full_children = []

        # Tuple of immediate sublings.
        # For children of P-node it just a (None, None)
        # For endmost children of Q-node it is (node, None) or (None, node)
        # For interior children of Q-node it is (None, None)
        self.left_subling = None
        self.right_subling = None

        # Node's label: EMPTY, FULL or PARTIAL
        self.label = Label.EMPTY

        # Node's mark: UNMARKED, QUEUED(placed into queue), BLOCKED(hasn't pointer to parent)
        # and UNBLOCKED(when it receives pointer to parent node)
        self.mark = Mark.UNMARKED

        # Pointer to parent node.
        self.parent = None

        # Set of all partial children of the node
        self.partial_children = []

        # Number of pertinent children Full or partial
        self.pertinent_child_count = 0

        # Number of pertinent leafs
        self.pertinent_leaf_count = 0

        # Node type: LEAF, P_NODE or Q_NODE
        self.node_type = node_type

        # Reference to node data(like id of edge)
        self.data = data
        if self.data is not None:
            self.data.node_reference = self

    def get_sublings(self) -> tuple:
        return self.left_subling, self.right_subling

    def get_left_subling(self):
        return self.left_subling

    def get_right_subling(self):
        return self.right_subling

    def get_num_sublings(self):
        count = 0
        if self.left_subling is not None:
            count += 1
        if self.right_subling is not None:
            count += 1
        return count

    def set_pertinent_child_count(self, new_value):
        self.pertinent_child_count = new_value

    def get_pertinent_child_count(self):
        return self.pertinent_child_count

    def inc_pertinent_child_count(self):
        self.pertinent_child_count += 1

    def add_child(self, child_node):
        # self.child_count += 1
        self.circular_link.append(child_node)
        # For now always add new node to the end
        self.endmost_children = child_node

        # Just to make sure that parent reference is correct
        child_node.parent = self

        # TODO: add more

    def copy_node(self, move_data=False):
        new_node = PQnode()
        # new_node.child_count = self.child_count
        new_node.circular_link = self.circular_link[:]
        new_node.left_endmost = self.left_endmost
        new_node.right_endmost = self.right_endmost
        new_node.full_children = self.full_children[:]
        new_node.left_subling = self.left_subling
        new_node.right_subling = self.right_subling
        new_node.label = self.label
        new_node.mark = self.mark
        new_node.parent = self.parent
        new_node.node_type = self.node_type
        if move_data:
            new_node.data = self.data
            new_node.data.node_reference = new_node
            self.data = None
        return new_node

    def move_full_children(self, new_node):
        for full_child in self.full_children:
            self.circular_link.remove(full_child)
            new_node.circular_link.append(full_child)
            full_child.parent = new_node
            new_node.full_children.append(full_child)

        self.full_children = []

    # Replaces child of node depending on current type
    def replace_child(self, old_child, new_child):
        if self.node_type == Type.P_NODE:
            self.circular_link.remove(old_child)
            self.circular_link.append(new_child)
        else:
            if old_child == self.left_endmost:
                self.left_endmost = new_child

            if old_child == self.right_endmost:
                self.right_endmost = new_child

            new_child.left_subling = old_child.left_subling
            new_child.right_subling = old_child.right_subling

    # Replace old_child with new_child which is partial q-node
    def replace_partial_child(self, old_child, new_child):
        new_child.parent = self

        # Add to list of partial children for each type of node
        self.partial_children.append(new_child)
        if old_child in self.partial_children:
            self.partial_children.remove(old_child)

        self.replace_child(old_child, new_child)

    def is_endmost_child(self):
        return self.left_subling is not None or \
               self.right_subling is not None

    def mark_full(self):
        self.label = Label.FULL
        if self.parent is not None and \
           self not in self.parent.full_children:
            self.parent.full_children.append(self)

    def mark_empty(self):
        self.label = Label.EMPTY

    def mark_partial(self):
        self.label = Label.PARTIAL
        if self.parent is not None and \
           self not in self.parent.partial_children:
            self.parent.partial_children.append(self)
            # self.parent.pertinent_child_count += 1
            # self.parent.pertinent_leaf_count += self.pertinent_leaf_count

    def __str__(self):
        return str(self.data)

    def reset(self):
        if self.node_type == Type.P_NODE:
            for child in self.circular_link:
                child.reset()
        elif self.node_type == Type.Q_NODE:
            child = self.left_endmost
            while child is not None:
                child.reset()
                child = child.right_subling

        # Common part for all nodes
        self.full_children = []
        self.partial_children = []
        self.pertinent_child_count = 0
        self.pertinent_leaf_count = 0
        self.mark = Mark.UNMARKED
        self.label = Label.EMPTY


if __name__ == "__main__":
    import doctest

    doctest.testmod()
