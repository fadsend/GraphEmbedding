from pqnode import PQnode, Type, Mark
from queue import Queue


class PQtree(object):

    def __init__(self, universe: set, subset: set):
        self.universe = universe
        self.subset = subset
        self.root = None

    def construct_from_graph(self, graph):
        edges = graph.getEdgeNumbers()

        # TODO: change to logger
        print("[PQtree::constructFromGraph] Edges: " + str(edges))

        self.root = PQnode(None, Type.P_NODE)

        for edge in edges:
            self.add_node(self.root, Type.LEAF, edge)

    def add_node(self, parent, node_type, data):
        # FIXME: deal with new constructor for PQnode
        new_node = PQnode(parent)
        parent.add_child(new_node)


# Global variables
# Number of block of blocked nodes
BLOCK_COUNT = 0
# Total number of blocked nodes
BLOCKED_NODES = 0
# True if virtual root node is used(1 is used, 0 is not)
OFF_THE_TOP = 0
# Queue of processed nodes
QUEUE = None


def reduce(tree : PQtree, subset: set) -> PQtree:
    global QUEUE, BLOCK_COUNT, BLOCKED_NODES, OFF_THE_TOP
    return None


def filter_sublings(sublings: tuple, mark: Mark) -> list:
    sublings_to_return = []
    for sub in sublings:
        if sub.get_mark() == mark:
            sublings_to_return.append(sub)
    return sublings_to_return


def get_max_consecutive_blocked_sublings_list(node):
    result_list = []

    # At first, got to the left direction and add blocked nodes
    left_subling = node.get_left_subling()
    while left_subling is not None and left_subling.get_mark() == Mark.BLOCKED:
        result_list.append(left_subling)
        left_subling = left_subling.get_left_subling()

    # Now to the right. We should not include node to the list, since it's already unblocked.
    right_subling = node.get_right_subling()
    while right_subling is not None and right_subling.get_mark() == Mark.BLOCKED:
        result_list.append(right_subling)
        right_subling = right_subling.get_right_subling()

    return result_list


def bubble(tree, subset):
    global QUEUE, BLOCK_COUNT, BLOCKED_NODES, OFF_THE_TOP

    # Initialize global variables
    QUEUE = Queue()
    BLOCK_COUNT = 0
    BLOCKED_NODES = 0
    OFF_THE_TOP = 0

    for element in subset:
        QUEUE.push(element)

    while QUEUE.size() + BLOCK_COUNT + OFF_THE_TOP > 1:
        if QUEUE.size() == 0:
            return PQtree(set(), set())

        # Get new node from queue and set BLOCKED mark by default
        node = QUEUE.pop()
        node.set_mark(Mark.BLOCKED)

        # Get list of blocked/unblocked sublings
        blocked_sublings = filter_sublings(node.get_sublings(), Mark.BLOCKED)
        unblocked_sublings = filter_sublings(node.get_sublings(), Mark.UNBLOCKED)

        # If some subling is unblocked, then set parent pointer and mark node as unblocked
        if len(unblocked_sublings) > 0:
            node.set_parent(unblocked_sublings[0].get_parent())
            node.set_mark(Mark.UNBLOCKED)
            # TODO: should pertinent child count be updated for parent node?

        # If not an interior child of Qnode, than mark as unblocked
        elif node.get_num_sublings() < 2:
            node.set_mark(Mark.UNBLOCKED)

        if node.get_mark() == Mark.UNBLOCKED:
            node_parent = node.get_parent()
            max_consecutive_blocked_sublings_list = []

            # Now, if node has been unblocked, then we should make all adjacent previously blocked
            # sublings unblocked and set parent pointer to them
            if len(blocked_sublings) > 0:
                max_consecutive_blocked_sublings_list = get_max_consecutive_blocked_sublings_list(node)

                # TODO: is node_parent not None here????
                for blocked_node in max_consecutive_blocked_sublings_list:
                    blocked_node.set_mark(Mark.UNBLOCKED)
                    blocked_node.set_parent(node_parent)
                    node_parent.inc_pertinent_child_count()

            # TODO: not sure why this check is needed
            if node_parent is None:
                OFF_THE_TOP = 1
            else:
                node_parent.inc_pertinent_child_count()
                if node_parent.get_mark() == Mark.UNMARKED:
                    QUEUE.push(node_parent)
                    node_parent.set_mark(Mark.QUEUED)

            BLOCK_COUNT -= len(blocked_sublings)
            BLOCKED_NODES -= len(max_consecutive_blocked_sublings_list)

        else:
            BLOCK_COUNT += (1 - len(blocked_sublings))
            BLOCKED_NODES += 1

    return tree
