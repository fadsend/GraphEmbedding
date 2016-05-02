from pqnode import PQnode, Type, Mark, Label
import myqueue


class PQtree(object):

    def __init__(self, universe):
        self.universe = universe
        self.root = None
        self.construct_tree()

    def reset(self):
        self.root.reset()

    def get_root(self):
        return self.root

    def construct_tree(self):
        self.root = PQnode(node_type=Type.P_NODE, data=None)
        for element in self.universe:
            self.root.add_child(Type.LEAF, element)

    def construct_from_graph(self, graph):
        edges = graph.getEdgeNumbers()

        # TODO: change to logger
        print("[PQtree::constructFromGraph] Edges: " + str(edges))

        self.root = PQnode(None)

        for edge in edges:
            self.add_node(self.root, Type.LEAF, edge)

    def __str__(self):
        if self.root is None:
            return "None"
        else:
            return self.print_tree(self.root)

    def print_tree(self, node):
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
            print("[Template_P4] 1) result = False")
            return False

        # Should be Q-node
        partial_child = node.partial_children[0]
        if partial_child.left_endmost == Label.FULL:
            partial_full = partial_child.left_endmost
            partial_empty = partial_child.right_endmost
        else:
            partial_full = partial_child.right_endmost
            partial_empty = partial_child.left_endmost

        if partial_full is None or partial_empty is None:
            print("[Template_P4] 2) result = False")
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

        print("[Template_P4] 3) result True")
        return True

    def template_p5(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE:
            print("[Template_P5] 1) result = False")
            return False

        if len(node.partial_children) != 1:
            print("[Template_P5] 2) result = False")
            return False

        node_parent = node.parent
        assert node_parent is not None

        partial_node = node.partial_children[0]
        assert partial_node.node_type == Type.Q_NODE

        empty_child = partial_node.get_endmost_child_with_label(Label.EMPTY)
        full_child = partial_node.get_endmost_child_with_label(Label.FULL)
        if not empty_child or not full_child:
            print("[Template_P5] 3) result = False")
            return False

        # Combine full nodes and move them
        if len(node.full_children) > 1:
            full_node = PQnode()
            full_node.node_type = Type.P_NODE
            node.move_full_children(full_node)
        else:
            # node.full_children has a len == 1 here
            full_node = node.full_children[0]
            node.full_children = []
            node.circular_link.remove(full_node)

        full_node.parent = partial_node

        # Append full not as a child of partial node
        # Must choose correct corner to add
        if partial_node.left_endmost.label == Label.FULL:
            endmost_full_node = partial_node.left_endmost
            endmost_full_node.left_subling = full_node
            full_node.right_subling = endmost_full_node
            partial_node.left_endmost = full_node
        else:
            endmost_full_node = partial_node.right_endmost
            endmost_full_node.right_subling = full_node
            full_node.left_subling = endmost_full_node
            partial_node.right_endmost = full_node

        full_node.mark_full()

        node.circular_link.remove(partial_node)
        node.partial_children.remove(partial_node)
        # Remove all reference to node from node_parent
        node_parent.circular_link.remove(node)

        # TODO: Not sure if could be 0
        if len(node.circular_link) == 1:
            node = node.circular_link[0]

        # Make empty P-node child of partial node
        if full_node == partial_node.left_endmost:
            endmost_empty_node = partial_node.right_endmost
            endmost_empty_node.right_subling = node
            node.left_subling = endmost_empty_node
            partial_node.right_endmost = node
        else:
            endmost_empty_node = partial_node.left_endmost
            endmost_empty_node.left_subling = node
            node.right_subling = endmost_empty_node
            partial_node.left_endmost = node

        node.mark_empty()
        partial_node.circular_link.append(node)

        partial_node.parent = node_parent
        partial_node.mark_partial()
        node_parent.circular_link.append(partial_node)

        print("[Template_P5] 4) result = True")
        return True

    def template_p6(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE:
            print("[Template_P6] 1) result = False")
            return False

        if len(node.partial_children) != 2:
            print("[Template_P6] 2) result = False")
            return False

        partial_qnode1 = node.partial_children[0]
        assert partial_qnode1.node_type == Type.Q_NODE

        empty_child1 = partial_qnode1.get_endmost_child_with_label(Label.EMPTY)
        full_child1 = partial_qnode1.get_endmost_child_with_label(Label.FULL)
        if not empty_child1 or not full_child1:
            print("[Template_P6] 3) result = False")
            return False

        partial_qnode2 = node.partial_children[1]
        assert partial_qnode2.node_type == Type.Q_NODE

        empty_child2 = partial_qnode2.get_endmost_child_with_label(Label.EMPTY)
        full_child2 = partial_qnode2.get_endmost_child_with_label(Label.FULL)
        if not empty_child2 or not full_child2:
            print("[Template_P6] 4) result = False")
            return False

        # At first, create P-node for full children of node
        if len(node.full_children) > 1:
            full_node = PQnode()
            full_node.node_type = Type.P_NODE
            node.move_full_children(full_node)
        # TODO: add special case for 0 full_children
        else:
            full_node = node.full_children[0]
            node.full_children = []
            node.circular_link.remove(full_node)

        # Add full node to the partial Q-node
        if len(node.full_children) >= 1:
            partial_qnode1.append_full_node(full_node)


        print("[Template_P6] 2) result = True")
        return True


    def template_q1(self, node: PQnode) -> bool:
        if node.node_type != Type.Q_NODE:
            print("[Template_Q1] result = " + str(False))
            return False

        child = node.left_endmost
        while child is not None:
            if child.label != Label.FULL:
                print("[Template_Q1] result = " + str(False))
                return False
            child = child.right_subling

        node.mark_full()
        print("[Template_Q1] result = " + str(True))
        return True


    def template_q2(self, node: PQnode) -> bool:
        if node.node_type != Type.Q_NODE or \
           len(node.partial_children) > 0:
            print("[Template_Q2] result = False")
            return False

        has_partial_child = len(node.partial_children) >= 1
        has_full_child = len(node.full_children) >= 1

        if has_full_child and not node.is_endmost_child_has_label(Label.FULL):
            print("[Template_Q2] result = False")
            return False

        if not has_full_child and not node.is_endmost_child_has_label(Label.PARTIAL):
            print("[Template_Q2] result = False")
            return False

        if has_partial_child:
            pass

        node.mark_partial()

        print("[Template_Q2] result = True")
        return True

    def template_q3(self, node: PQnode) -> bool:
        if node.node_type != Type.Q_NODE:
            print("[Template_Q3] result = False")
            return False

        print("[Template_Q3] result = False")
        return False

    def unblock_sublings(self, node):
        assert node.mark == Mark.UNBLOCKED

        count = 0
        for subling in node.immediate_sublings:
            if subling.mark == Mark.BLOCKED:
                subling.parent = node.parent
                subling.mark = Mark.UNBLOCKED
                count += 1
                count += self.unblock_sublings(subling)
        return count

    def filter_sublings(self, node: PQnode, mark: Mark) -> list:
        sublings_to_return = []
        for sub in node.immediate_sublings:
            if sub and sub.mark == mark:
                sublings_to_return.append(sub)
        return sublings_to_return


# Global variables
# Number of block of blocked nodes
BLOCK_COUNT = 0
# Total number of blocked nodes
BLOCKED_NODES = 0
# True if virtual root node is used(1 is used, 0 is not)
OFF_THE_TOP = 0
# Queue of processed nodes
QUEUE = None


def __bubble(tree, subset):
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
            return PQtree([])

        # Get new node from queue and set BLOCKED mark by default
        node = QUEUE.pop()
        node.mark = Mark.BLOCKED

        # Get list of blocked/unblocked sublings
        blocked_sublings = tree.filter_sublings(node, Mark.BLOCKED)
        unblocked_sublings = tree.filter_sublings(node, Mark.UNBLOCKED)

        # If some subling is unblocked, then set parent pointer and mark node as unblocked
        if len(unblocked_sublings) > 0:
            node.parent = unblocked_sublings[0].parent
            node.mark = Mark.UNBLOCKED
        # If not an interior child of Qnode, than mark as unblocked
        elif node.get_num_sublings() < 2:
            node.mark = Mark.UNBLOCKED

        if node.mark == Mark.UNBLOCKED:
            node_parent = node.parent
            unblocked_sublings_count = 0

            # Now, if node has been unblocked, then we should make all adjacent previously blocked
            # sublings unblocked and set parent pointer to them
            if len(blocked_sublings) > 0:
                unblocked_sublings_count = tree.unblock_sublings(node)
                node_parent.pertinent_child_count += unblocked_sublings_count

            # TODO: not sure why this check is needed
            if node_parent is None:
                OFF_THE_TOP = 1
            else:
                node_parent.pertinent_child_count += 1
                if node_parent.mark == Mark.UNMARKED:
                    QUEUE.push(node_parent)
                    node_parent.mark = Mark.QUEUED

            BLOCK_COUNT -= len(blocked_sublings)
            BLOCKED_NODES -= unblocked_sublings_count

        else:
            BLOCK_COUNT += (1 - len(blocked_sublings))
            BLOCKED_NODES += 1

    # TODO: i guess pseudonode should be added here
    return tree


def __reduce(tree, subset):
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
               not tree.template_p5(node) and \
               not tree.template_q1(node) and \
               not tree.template_q2(node):
                return PQtree([])

        else:
            if not tree.template_l1(node) and \
               not tree.template_p1(node, True) and \
               not tree.template_p2(node) and \
               not tree.template_p4(node) and \
               not tree.template_p6(node) and \
               not tree.template_q1(node) and \
               not tree.template_q2(node) and \
               not tree.template_q3(node):
                return PQtree([])

    return tree


# TODO: Introduce error checks
def reduce_tree(tree, subset):
    tree = __bubble(tree, subset)
    tree = __reduce(tree, subset)
    tree.reset()
    return tree

