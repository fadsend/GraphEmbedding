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


class Queue(object):

    def __init__(self, data=None):
        """Initiate a queue

        Initiate an empty queue
        >>> Queue().size()
        0

        The same for empty list
        >>> Queue([]).size()
        0

        Assert on incorrect input
        >>> Queue(23)
        Traceback (most recent call last):
        ...
        AssertionError

        Initiate queue from tuple
        >>> Queue((10, 12, 13)).size()
        3

        Check get first element
        >>> Queue([1, 2, 3]).pop()
        1

        Add new element
        >>> s = Queue([1, 2, 3])
        >>> s.push(4)
        >>> s.size()
        4
        >>> s.pop()
        1
        >>> s.size()
        3
        """

        assert \
            data is None or \
            type(data) == list or \
            type(data) == tuple

        if data is None:
            self.data = []
        else:
            self.data = list(data)

    def push(self, dataToAdd):
        self.data.append(dataToAdd)

    def pop(self):
        return self.data.pop(0)

    def size(self):
        return len(self.data)


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
