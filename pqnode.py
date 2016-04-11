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
    def __init__(self, parent, nodeType):
        self.childCount = 0
        self.circularLink = None
        self.endmostChildren = None
        self.fullChildren = None
        self.immediateSublings = (None, None)
        self.label = Label.EMPTY
        self.mark = Mark.UNMARKED
        self.parent = parent
        self.partialChilren = set([])
        self.pertinentChildCount = 0
        self.pertinentLeafCount = 0
        self.nodeType = nodeType


def buble(tree, subset):
    return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
