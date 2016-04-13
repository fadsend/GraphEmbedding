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


# Global variables
# TODO: Move into separate file later
BLOCK_COUNT = 0
BLOCKED_NODES = 0
OFF_THE_TOP = False
QUEUE = None


class PQnode(object):
    # TODO: Perhaps add more field as arguments
    def __init__(self, parent, node_type, data=None):
        self.childCount = 0

        # List of children
        self.circularLink = []

        self.endmostChildren = None
        self.fullChildren = None
        self.immediate_sublings = (None, None)
        self.label = Label.EMPTY
        self.mark = Mark.UNMARKED
        self.parent = parent
        self.partial_children = set([])
        self.pertinentChildCount = 0
        self.pertinentLeafCount = 0
        self.nodeType = node_type
        self.data = data

    def add_child(self, child_node):
        self.childCount += 1
        self.circularLink.append(child_node)
        # For now always add new node to the end
        self.endmostChildren = child_node

        # Just to make sure that parent reference is correct
        child_node.parent = self

        # TODO: add more 


if __name__ == "__main__":
    import doctest
    doctest.testmod()
