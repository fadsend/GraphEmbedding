from pqnode import PQnode, Type, Mark, Label
import myqueue


class PQtree(object):

    def __init__(self, universe, subset):
        self.universe = universe
        self.root = None
        self.construct_tree_with_subset(subset)

    # def __init__(self, universe, subset):
    #     self.universe = universe
    #    # self.subset = subset
    #     self.root = None
    #     self.construct_tree_with_subset(subset)

    # TODO:Check how tree should be constructed
    def construct_tree_with_subset(self, subset):
        self.root = PQnode(node_type=Type.P_NODE, data=None)
        if len(subset) > 0:
            sub_root = PQnode(node_type=Type.P_NODE, data=None)
            self.root.add_child(sub_root)

        for element in self.universe:
            new_node = PQnode(node_type=Type.LEAF, data=element)
            if element in subset:
                sub_root.add_child(new_node)
            else:
                self.root.add_child(new_node)

    def construct_from_graph(self, graph):
        edges = graph.getEdgeNumbers()

        # TODO: change to logger
        print("[PQtree::constructFromGraph] Edges: " + str(edges))

        self.root = PQnode(None)

        for edge in edges:
            self.add_node(self.root, Type.LEAF, edge)

    # def add_node(self, parent, node_type, data):
    #     # FIXME: deal with new constructor for PQnode
    #     new_node = PQnode(parent)
    #     parent.add_child(new_node)

    def __str__(self):
        return self.print_tree(self.root)

    def print_tree(self, node):
        if node is None:
            return ""

        result = ""
        if node.node_type == Type.Q_NODE:
            result += str(node.id) + ": { "
            child = node.left_endmost
            while child is not None:
                result += self.print_tree(child) + ", "
                child = child.right_subling

            # Remove last comma
            # TODO: Do it in a better way
            # result = result[:-2]
            result += " }"

        elif node.node_type == Type.P_NODE:
            result += str(node.id) + ": [ "
            for child in node.circular_link:
                result += self.print_tree(child) + ", "
            # Remove last comma
            # TODO: Do it in a better way
            # result = result[:-2]
            result += " ]"
        else:
            result = str(node.data)

        return result

    def get_frontier(self):
        return self.__get_frontier(self.root)

    def __get_frontier(self, node):
        frontier = []
        if node.node_type == Type.P_NODE:
            for child in node.circular_link:
                frontier += self.__get_frontier(child)
        elif node.node_type == Type.Q_NODE:
            child = node.left_endmost
            while child is not None:
                frontier += self.__get_frontier(child)
                child = child.right_subling
        else:
            frontier += [str(node.data)]
        return frontier




    @staticmethod
    def exchange_nodes(old_node: PQnode, new_node: PQnode):

        # TODO: check reference parent

        if old_node.is_endmost_child():
            if old_node.parent.left_endmost == old_node:
                old_node.parent.left_endmost = new_node
            elif old_node.parent.right_endmost == old_node:
                old_node.parent.right_endmost = new_node

        new_node.parent = old_node.parent

    # Template L1
    # Only applicable for leafs
    # If leaf is in subset then mark it as full
    # otherwise mark it as empty
    def template_l1(self, node: PQnode) -> bool:
        if node.node_type == Type.LEAF and node.data is not None:
            node.mark_full()
            return True

        print("[Template_L1] result = False")
        return False


    # Template P1
    # Match P-node only
    # If all children of P-node are empty, mark node as empty
    # If all are full then mark node as full
    def template_p1(self, node: PQnode, is_root: bool) -> bool:

        if node.node_type != Type.P_NODE or len(node.full_children) != len(node.circular_link):
            print("[Template_P1] result = " + str(False))
            return False

        #node.mark_full()
        node.label = Label.FULL
        if not is_root and not node in node.parent.full_children:
            node.parent.full_children.append(node)

        return True

    def template_p2(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE or len(node.partial_children) > 0:
            print("[Template_P2] result = " + str(False))
            return False

        if len(node.full_children) >= 2:
            full_node = PQnode()
            full_node.node_type = Type.P_NODE
            full_node.parent = node
            node.move_full_children(full_node)
            node.circular_link.append(full_node)
            full_node.mark_full()

        node.mark_partial()

        print("P2 = True")
        return True

    def template_p3(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE or len(node.partial_children) > 0:
            print("[Template_P3] result = " + str(False))
            return False

        new_qnode = PQnode()
        new_qnode.node_type = Type.Q_NODE
        new_qnode.label = Label.PARTIAL

        node.parent.replace_partial_child(node, new_qnode)

        # Special case when only one full child
        if len(node.full_children) == 1:
            full_child = node.full_children[0]
            node.full_children = []
            node.circular_link.remove(full_child)
        # Otherwise create new P-node
        else:
            full_child = PQnode()
            full_child.node_type = Type.P_NODE
            node.move_full_children(full_child)

        full_child.parent = new_qnode
        new_qnode.right_endmost = full_child
        full_child.mark_full()

        # If only one empty child
        if len(node.circular_link) - len(node.full_children) == 1:
            empty_child = node.circular_link[0]
            node.circular_link = []
        else:
            empty_child = node

        empty_child.parent = new_qnode
        new_qnode.left_endmost = empty_child
        empty_child.mark_empty()

        empty_child.right_subling = full_child
        full_child.left_subling = empty_child

        print("Template 3 exit with True")

        return True


    def template_p4(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE or \
           len(node.partial_children) != 1:
            return False

        print("Template_P4 entered")

        # Should be Q-node
        partial_child = node.partial_children[0]
        if partial_child.left_endmost == Label.FULL:
            partial_full = partial_child.left_endmost
            partial_empty = partial_child.right_endmost
        else:
            partial_full = partial_child.right_endmost
            partial_empty = partial_child.left_endmost

        if partial_full is None or partial_empty is None:
            return False

        if len(node.full_children) == 1:
            full_child = node.full_children[0]
            node.full_children = []
            node.circular_link.remove(full_child)
        else:
            full_child = PQnode()
            full_child.node_type = Type.P_NODE
            node.move_full_children(full_child)

        # TODO: refactor a little bit
        if partial_child.right_endmost.label == Label.FULL:
            endmost_full = partial_child.right_endmost
            full_child.parent = partial_child
            partial_child.right_endmost = full_child
            full_child.mark_full()
            full_child.left_subling = endmost_full
            endmost_full.right_subling = full_child
        else:
            endmost_full = partial_child.left_endmost
            full_child.parent = partial_child
            partial_child.left_endmost = full_child
            full_child.mark_full()
            full_child.right_subling = endmost_full
            endmost_full.left_subling = full_child

        # TODO: if node has only one child, delete it

        return True


    def template_p5(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE:
            print("[Template_P5] result = False")
            return False

        if len(node.partial_children) != 1:
            print("[Template_P5] result = False")
            return False

        partial_node = node.partial_children[0]
        # TODO: complete implementation

        print("[Template_P5] result = False")
        return False


    def template_p6(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE:
            return False
        pass


    def template_q1(self, node: PQnode) -> bool:
        if node.node_type != Type.Q_NODE:
            print("[Template_Q1] result = " + str(False))
            return False

        child = node.left_endmost
        while child is not None:
            if child.label != Label.FULL:
                print("[Template_Q1] result = " + str(False))
                return False

        node.mark_full()
        print("[Template_Q1] result = " + str(True))
        return True


    def template_q2(self, node: PQnode) -> bool:
        if node.node_type != Type.Q_NODE:
            return False
        pass


    def template_q3(self, node: PQnode) -> bool:
        if node.node_type != Type.Q_NODE:
            return False
        return False



# Global variables
# Number of block of blocked nodes
BLOCK_COUNT = 0
# Total number of blocked nodes
BLOCKED_NODES = 0
# True if virtual root node is used(1 is used, 0 is not)
OFF_THE_TOP = 0
# Queue of processed nodes
QUEUE = None


def filter_sublings(sublings: tuple, mark: Mark) -> list:
    sublings_to_return = []
    for sub in sublings:
        if sub and sub.mark == mark:
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


def bubble_tree(tree, subset):
    global QUEUE, BLOCK_COUNT, BLOCKED_NODES, OFF_THE_TOP

    # Initialize global variables
    QUEUE = myqueue.MyQueue()
    BLOCK_COUNT = 0
    BLOCKED_NODES = 0
    OFF_THE_TOP = 0

    for element in subset:
        QUEUE.push(element.node_reference)

    while QUEUE.size() + BLOCK_COUNT + OFF_THE_TOP > 1:
        if QUEUE.size() == 0:
            return PQtree([], [])

        # Get new node from queue and set BLOCKED mark by default
        node = QUEUE.pop()
        node.mark = Mark.BLOCKED

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
            node.mark = Mark.UNBLOCKED

        if node.mark == Mark.UNBLOCKED:
            node_parent = node.parent
            max_consecutive_blocked_sublings_list = []

            # Now, if node has been unblocked, then we should make all adjacent previously blocked
            # sublings unblocked and set parent pointer to them
            if len(blocked_sublings) > 0:
                max_consecutive_blocked_sublings_list = get_max_consecutive_blocked_sublings_list(node)

                # TODO: is node_parent not None here????
                for blocked_node in max_consecutive_blocked_sublings_list:
                    blocked_node.set_mark(Mark.UNBLOCKED)
                    blocked_node.set_parent(node_parent)
                    node_parent.pertinent_child_count += 1

            # TODO: not sure why this check is needed
            if node_parent is None:
                OFF_THE_TOP = 1
            else:
                node_parent.inc_pertinent_child_count()
                if node_parent.mark == Mark.UNMARKED:
                    QUEUE.push(node_parent)
                    node_parent.mark = Mark.QUEUED

            BLOCK_COUNT -= len(blocked_sublings)
            BLOCKED_NODES -= len(max_consecutive_blocked_sublings_list)

        else:
            BLOCK_COUNT += (1 - len(blocked_sublings))
            BLOCKED_NODES += 1

    # TODO: i guess pseudonode should be added here
    return tree


def reduce_tree(tree, subset):
    global QUEUE, BLOCK_COUNT, BLOCKED_NODES, OFF_THE_TOP

    QUEUE = myqueue.MyQueue()

    for leaf in subset:
        QUEUE.push(leaf.node_reference)
        leaf.node_reference.pertinent_leaf_count = 1

    while QUEUE.size() > 0:
        node = QUEUE.pop()
        if node.pertinent_leaf_count < len(subset):
            node_parent = node.parent

            # TODO: check if ok to do so
            node_parent.pertinent_leaf_count += node.pertinent_leaf_count
            node_parent.pertinent_child_count -= 1

            if node_parent.pertinent_child_count == 0:
                QUEUE.push(node_parent)

            if not tree.template_l1(node) and \
               not tree.template_p1(node, False) and \
               not tree.template_p3(node) and \
               not tree.template_q1(node) and \
               not tree.template_q2(node):
                return PQtree([], [])

        else:
            if not tree.template_l1(node) and \
               not tree.template_p1(node, True) and \
               not tree.template_p2(node) and \
               not tree.template_p4(node) and \
               not tree.template_p6(node) and \
               not tree.template_q1(node) and \
               not tree.template_q2(node) and \
               not tree.template_q3(node):
                return PQtree([], [])

    return tree

