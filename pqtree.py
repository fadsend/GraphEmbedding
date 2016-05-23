from pqnode import PQnode, Type, Mark, Label
import myqueue
from llist import dllist


class ReductionFailed(Exception):
    pass


class PQtree(object):

    def __init__(self, universe, create_root=False):
        # Universe set
        assert universe is not None
        # self.universe = universe
        # Reference to pseudo node
        self.pseudo_node = None
        # References to siblings of pseudo node to restore them later
        self.pseudo_siblings = [None, None]
        # Pertinent root
        # self.pertinent_root = None
        # Root of the tree
        if len(universe) > 0 or create_root:
            if len(universe) != 1:
                self.root = PQnode(node_type=Type.P_NODE, data=None)
                # Form initial tree
                for element in universe:
                    self.root.add_child(Type.LEAF, element)
            else:
                self.root = PQnode(node_type=Type.LEAF, data=universe[0])
        else:
            self.root = None

    def pre_reset(self):
        self.root.reset()

    def post_reset(self):
        self.pseudo_node = None
        self.pseudo_siblings = [None, None]

    # Note: tree must be reduced, and subset must be the same
    # as for reduction
    def get_pertinent_root(self, subset):
        assert subset is not None
        assert len(subset) > 0
        element = subset[0].node_reference
        successor = element.parent
        prev = element
        while successor is not None and (successor.label == Label.FULL):
            prev = successor
            successor = successor.parent

        if successor is None or successor.label == Label.EMPTY:
            return prev
        if successor.label == Label.PARTIAL:
            return successor

    def get_root(self):
        return self.root

    def __str__(self):
        if self.root is None:
            return "None"
        else:
            return self.print_tree(self.root)

    def print_tree(self, node: PQnode):
        result = ""

        # TODO: find a way to print indicator
        if node.prev_indicator:
            prev_node = node.prev_indicator.prev_node
            next_node = node.prev_indicator.next_node
            if prev_node:
                prev_node = prev_node.id
            if next_node:
                next_node = next_node.id
            result += " " + str(node.prev_indicator) + \
                      "!( " + str(prev_node) +\
                      " -> " + str(next_node) + ")!"

        if node.node_type == Type.Q_NODE:
            result += str(node.id) + ": { "
            # while child is not None:
            for child in node.iter_children():
                result += self.print_tree(child) + ", "

            # Remove last comma
            result += " }"

        elif node.node_type == Type.P_NODE:
            result += str(node.id) + ": [ "
            # for child in node.circular_link:
            for child in node.iter_children():
                result += self.print_tree(child) + ", "
            # Remove last comma
            result += " ]"
        else:
            result += str(node.id) + ":(" + str(node.data) + ")"

        return result

    def get_frontier(self):
        if self.root is None:
            return []
        return self.__get_frontier(self.root)

    def __get_frontier(self, node: PQnode):
        frontier = []
        if node.node_type != Type.LEAF:
            for child in node.iter_children():
                frontier += self.__get_frontier(child)
        else:
            frontier += [str(node.data)]
        return frontier

    # Template L1
    # Only applicable for leafs
    # If leaf is in subset then mark it as full
    # otherwise mark it as empty
    @staticmethod
    def template_l1(node: PQnode) -> bool:
        if node.node_type == Type.LEAF and node.data is not None:
            node.mark_full()
            return True

        print("[Template_L1] result = False, node: " + str(node.id))
        return False

    # Template P1
    # Match P-node only
    # If all children of P-node are empty, mark node as empty
    # If all are full then mark node as full
    @staticmethod
    def template_p1(node: PQnode, is_root: bool) -> bool:

        if node.node_type != Type.P_NODE or len(node.full_children) != len(node.circular_link):
            print("[Template_P1] result = " + str(False) + " node: " + str(node.id))
            return False

        node.label = Label.FULL
        # TODO: get rid of "in" operator
        if not is_root and node not in node.parent.full_children:
            node.full_list_node = node.parent.full_children.append(node)
        print("[Template_P1] result = True node: " + str(node.id))
        return True

    @staticmethod
    def template_p2(node: PQnode) -> bool:
        if node.node_type != Type.P_NODE or len(node.partial_children) > 0:
            print("[Template_P2] result = " + str(False) + " node: " + str(node.id))
            return False

        # TODO: update direction indicators here
        if len(node.full_children) >= 2:
            full_node = PQnode()
            full_node.node_type = Type.P_NODE
            full_node.parent = node
            node.move_full_children(full_node)
            full_node.circular_list_node = node.circular_link.append(full_node)
            full_node.mark_full()

        node.mark_partial()

        print("P2 = True node: " + str(node.id))
        return True

    @staticmethod
    def template_p3(node: PQnode) -> bool:
        if node.node_type != Type.P_NODE or len(node.partial_children) > 0:
            print("[Template_P3] result = " + str(False) + " node: " + str(node.id))
            return False

        new_qnode = PQnode()
        new_qnode.node_type = Type.Q_NODE
        new_qnode.label = Label.PARTIAL

        node.parent.replace_partial_child(node, new_qnode)
        node.replace_direction_indicator(new_qnode)

        # Special case when only one full child
        if len(node.full_children) == 1:
            full_child = node.full_children.nodeat(0).value
            node.full_children = dllist()
            node.circular_link.remove(full_child.circular_list_node)
        # Otherwise create new P-node
        else:
            full_child = PQnode()
            full_child.node_type = Type.P_NODE
            node.move_full_children(full_child)

        full_child.parent = new_qnode
        new_qnode.endmost_children[0] = full_child
        full_child.mark_full()

        # If only one empty child
        if len(node.circular_link) - len(node.full_children) == 1:
            empty_child = node.circular_link.nodeat(0).value
            node.circular_link = dllist()
        else:
            empty_child = node

        empty_child.parent = new_qnode
        new_qnode.endmost_children[1] = empty_child
        empty_child.mark_empty()

        empty_child.immediate_sublings[0] = full_child
        full_child.immediate_sublings[0] = empty_child

        new_qnode.mark_partial()
        print("Template 3 exit with True node: " + str(node.id))

        return True

    def template_p4(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE or \
           len(node.partial_children) != 1:
            print("[Template_P4] 1) result = False node: " + str(node.id))
            return False

        # Should be Q-node
        partial_child = node.partial_children.nodeat(0).value
        empty_child = partial_child.get_endmost_child_with_label(Label.EMPTY)
        full_child = partial_child.get_endmost_child_with_label(Label.FULL)

        if not empty_child or not full_child:
            print("[Template_P4] 2) result = False node: " + str(node.id))
            return False

        if len(node.full_children) > 0:
            if len(node.full_children) == 1:
                new_full_node = node.full_children.nodeat(0).value
                node.full_children = dllist()
                node.circular_link.remove(new_full_node.circular_list_node)
            else:
                new_full_node = PQnode()
                new_full_node.node_type = Type.P_NODE
                node.move_full_children(new_full_node)

            new_full_node.parent = partial_child
            new_full_node.mark_full()
            partial_child.replace_endmost_child(full_child, new_full_node)
            full_child.add_sibling(new_full_node)
            new_full_node.add_sibling(full_child)

            if full_child.has_indicator(None):
                indicator = full_child.get_indicator(None)
                indicator.replace_node_for_indicator(None, new_full_node)

        # P4 is applied only for root, so no need to update direction indicator
        # for child q-node
        if len(node.circular_link) == 1:
            if node.parent is None:
                if node == self.root:
                    # old_root = self.root
                    self.root = partial_child
                    self.root.parent = None
                else:
                    # In case of pseudonode??
                    for i in range(2):
                        node.immediate_sublings[i].replace_siblings(node, partial_child)
            else:
                node.parent.replace_partial_child(node, node.circular_link[0])
            node.full_reset_node()

        print("[Template_P4] 3) result True node: " + str(node.id))
        return True

    @staticmethod
    def template_p5(node: PQnode) -> bool:
        if node.node_type != Type.P_NODE:
            print("[Template_P5] 1) result = False node: " + str(node.id))
            return False

        if len(node.partial_children) != 1:
            print("[Template_P5] 2) result = False node: " + str(node.id))
            return False

        node_parent = node.parent
        assert node_parent is not None

        partial_node = node.partial_children.nodeat(0).value
        assert partial_node.node_type == Type.Q_NODE

        empty_child = partial_node.get_endmost_child_with_label(Label.EMPTY)
        full_child = partial_node.get_endmost_child_with_label(Label.FULL)
        if not empty_child or not full_child:
            print("[Template_P5] 3) result = False node: " + str(node.id))
            return False

        # Combine full nodes and move them
        if len(node.full_children) > 0:
            if len(node.full_children) > 1:
                full_node = PQnode()
                full_node.node_type = Type.P_NODE
                node.move_full_children(full_node)
            else:
                # node.full_children has a len == 1 here
                full_node = node.full_children.nodeat(0).value
                node.full_children = dllist()
                node.circular_link.remove(full_node.circular_list_node)

            full_node.parent = partial_node
            full_node.mark_full()

            # Add new full node as an endmost children
            partial_node.replace_endmost_child(full_child, full_node)
            full_child.add_sibling(full_node)
            full_node.add_sibling(full_child)

            if full_child.has_indicator(None):
                indicator = full_child.get_indicator(None)
                indicator.replace_node_for_indicator(None, full_node)

        # Update links
        node.circular_link.remove(partial_node.circular_list_node)
        node.partial_children.remove(partial_node.partial_list_node)

        node_parent.replace_partial_child(node, partial_node)
        node.replace_direction_indicator(partial_node)

        # If there are left empty children, move them to
        # partial node
        if len(node.circular_link) > 0:
            empty_node = node
            # If only one child is left, use it instead of P-node
            if len(node.circular_link) == 1:
                empty_node = node.circular_link.nodeat(0).value
                node.circular_link = dllist()

            # Move empty child to partial node
            partial_node.replace_endmost_child(empty_child, empty_node)
            empty_node.parent = partial_node
            empty_node.clear_siblings()
            empty_child.add_sibling(empty_node)
            empty_node.add_sibling(empty_child)
            # Just in case
            empty_node.mark_empty()

            if empty_child.has_indicator(None):
                indicator = empty_child.get_indicator(None)
                indicator.replace_node_for_indicator(None, empty_node)

        print("[Template_P5] 4) result = True node: " + str(node.id))
        return True

    def template_p6(self, node: PQnode) -> bool:
        if node.node_type != Type.P_NODE:
            print("[Template_P6] 1) result = False node: " + str(node.id))
            return False

        if len(node.partial_children) != 2:
            print("[Template_P6] 2) result = False node: " + str(node.id))
            return False

        partial_qnode1 = node.partial_children.nodeat(0).value
        assert partial_qnode1.node_type == Type.Q_NODE

        empty_child1 = partial_qnode1.get_endmost_child_with_label(Label.EMPTY)
        full_child1 = partial_qnode1.get_endmost_child_with_label(Label.FULL)
        if not empty_child1 or not full_child1:
            print("[Template_P6] 3) result = False node: " + str(node.id))
            return False

        partial_qnode2 = node.partial_children.nodeat(1).value
        assert partial_qnode2.node_type == Type.Q_NODE

        empty_child2 = partial_qnode2.get_endmost_child_with_label(Label.EMPTY)
        full_child2 = partial_qnode2.get_endmost_child_with_label(Label.FULL)
        if not empty_child2 or not full_child2:
            print("[Template_P6] 4) result = False node: " + str(node.id))
            return False

        if len(node.full_children) > 0:
            # Only one full child, no need to create new P-node
            if len(node.full_children) == 1:
                full_node = node.full_children.nodeat(0).value
                node.full_children = dllist
                node.circular_link.remove(full_node.circular_list_node)
            else:
                full_node = PQnode()
                full_node.node_type = Type.P_NODE
                node.move_full_children(full_node)

            full_node.parent = partial_qnode1
            full_node.mark_full()

            # Put full_node as a child of partial_qnode1
            #
            # Note: do not set endmost_child yet, it will be done later
            # after merge of partial nodes
            full_child1.add_sibling(full_node)
            full_node.add_sibling(full_child1)

            # Now merge two partial nodes
            full_node.add_sibling(full_child2)
            full_child2.add_sibling(full_node)

            partial_qnode1.replace_direction_indicator(full_node)
            partial_qnode2.replace_direction_indicator(full_node)

            for child in [full_child1, full_child2]:
                if child.has_indicator(None):
                    indicator = child.get_indicator(None)
                    indicator.replace_node_for_indicator(None, full_node)

        else:
            # In this case just merge partial nodes
            full_child1.add_sibling(full_child2)
            full_child2.add_sibling(full_child1)

            # Update direction indicator for partial_qnode1
            partial_qnode1.replace_direction_indicator(full_child1)
            partial_qnode2.replace_direction_indicator(full_child2)

            if full_child1.has_indicator(None):
                indicator = full_child1.get_indicator(None)
                indicator.replace_node_for_indicator(None, full_child2)

            if full_child2.has_indicator(None):
                indicator = full_child2.get_indicator(None)
                indicator.replace_node_for_indicator(None, full_child1)

        partial_qnode1.replace_endmost_child(full_child1, empty_child2)
        empty_child2.parent = partial_qnode1

        partial_qnode2.move_full_children(partial_qnode1)

        # full_child2.parent = partial_qnode1
        # full_child2.mark_full()

        # Remove partial_qnode2
        node.circular_link.remove(partial_qnode2.circular_list_node)
        partial_qnode2.full_reset_node()

        # Since node could be only root, no need to update direction indicator
        if len(node.circular_link) == 1:
            if node.parent is None:
                if self.root == node:
                    self.root = node.circular_link.nodeat(0).value
                node.circular_link.nodeat(0).value.parent = None
                node.full_reset_node()
            else:
                new_node = node.circular_link.nodeat(0).value
                node.parent.replace_child(node, new_node)
                new_node.parent = node.parent
                new_node.mark_partial()

        print("[Template_P6] 2) result = True node: " + str(node.id))
        return True

    @staticmethod
    def template_q1(node: PQnode) -> bool:
        if node.node_type != Type.Q_NODE:
            print("[Template_Q1] result = " + str(False) + " node: " + str(node.id))
            return False

        for child in node.iter_children():
            if child.label != Label.FULL:
                print("[Template_Q1] result = " + str(False) + " node: " + str(node.id))
                return False

        node.mark_full()
        print("[Template_Q1] result = " + str(True) + " node: " + str(node.id))
        return True

    @staticmethod
    def template_q2(node: PQnode) -> bool:
        # TODO: understand check for pseudo_node
        if node.node_type != Type.Q_NODE or \
           len(node.partial_children) > 1 or \
           node.is_pseudo_node or \
           not node.full_or_partial_children_are_consecutive():
            print("[Template_Q2] 1) result = False node: " + str(node.id))
            return False

        has_partial_child = len(node.partial_children) >= 1
        has_full_child = len(node.full_children) >= 1

        if has_full_child and not node.get_endmost_child_with_label(Label.FULL):
            print("[Template_Q2] 2) result = False node: " + str(node.id))
            return False

        if not has_full_child and not node.get_endmost_child_with_label(Label.PARTIAL):
            print("[Template_Q2] 3) result = False node: " + str(node.id))
            return False

        should_process = True
        # Check special case when partial child is an endmost
        endmost_partial_node = node.get_endmost_child_with_label(Label.PARTIAL)
        if endmost_partial_node:
            should_process = False
            empty_child = endmost_partial_node.get_endmost_child_with_label(Label.EMPTY)
            full_child = endmost_partial_node.get_endmost_child_with_label(Label.FULL)
            # 2 cases: when empty child is endmost or when full child is endmost
            if endmost_partial_node.get_sibling_with_label(Label.EMPTY):
                empty_sibling = endmost_partial_node.get_sibling_with_label(Label.EMPTY)
                empty_sibling.replace_sibling(endmost_partial_node, empty_child)
                node.replace_endmost_child(endmost_partial_node, full_child)

                # Update direction indicator on a node
                endmost_partial_node.replace_direction_indicator(empty_child)

                # Update direction indicator on a endmost_partial_node
                if empty_child.has_indicator(None):
                    indicator = empty_child.get_indicator(None)
                    indicator.replace_node_for_indicator(None, empty_sibling)

            elif endmost_partial_node.get_sibling_with_label(Label.FULL):
                full_sibling = endmost_partial_node.get_sibling_with_label(Label.FULL)
                full_sibling.replace_sibling(endmost_partial_node, full_child)
                node.replace_endmost_child(endmost_partial_node, empty_child)

                # Same updates for full node
                endmost_partial_node.replace_direction_indicator(full_child)

                # Update direction indicator on a endmost_partial_node
                if full_child.has_indicator(None):
                    indicator = full_sibling.get_indicator(None)
                    indicator.replace_node_for_indicator(None, full_sibling)
            else:
                assert False
            # Move all full nodes from endmost_partial_node to node
            node.full_children.extend(endmost_partial_node.full_children)
            node.mark_partial()

            print("[Template_Q2] 4) result = True node: " + str(node.id))
            return True

        # If partial Q-node exists, move all children from it
        if has_partial_child and should_process:
            partial_node = node.partial_children.nodeat(0).value

            # Merge both corners
            for i in range(2):
                child = node.endmost_children[i]
                assert child is not None

                # Get endmost child of a partial node with the same label
                partial_child = partial_node.get_endmost_child_with_label(child.label)

                # I guess it cannot be eq to None
                # if partial_child is not None:
                sibling_of_partial = partial_node.get_sibling_with_label(child.label)
                if sibling_of_partial is not None:
                    # Note: add_sibling for partial_child is not needed since it
                    # will be added in replace_sibling
                    sibling_of_partial.replace_sibling(partial_node, partial_child)
                else:
                    node.replace_endmost_child(sibling_of_partial, partial_child)

                partial_node.replace_direction_indicator(partial_child, child.label)

                # Override parent node just in case
                assert partial_child is not None

                partial_child.parent = node
                if partial_child.label == Label.FULL:
                    partial_child.mark_full()

                # Update direction indicators
                partial_node.replace_direction_indicator(partial_child, child.label)

                if partial_child.has_indicator(None):
                    indicator = partial_child.get_indicator(None)
                    indicator.replace_node_for_indicator(None, sibling_of_partial)

            node.partial_children.remove(partial_node.partial_list_node)
            partial_node.parent = None

        node.mark_partial()

        print("[Template_Q2] 5) result = True node: " + str(node.id))
        return True

    @staticmethod
    def template_q3(node: PQnode) -> bool:
        if node.node_type != Type.Q_NODE or \
           len(node.partial_children) > 2 or \
           not node.full_or_partial_children_are_consecutive():
            print("[Template_Q3] 1) result = False node: " + str(node.id))
            return False

        # Updating direction indicator, i guess it could be re-written
        for tmp_node in node.partial_children:
            # Check if the node is endmost, in this case skip update for direction
            # indicator on empty side

            # Updating indicator for empty part of partial node
            empty_child = tmp_node.get_endmost_child_with_label(Label.EMPTY)
            empty_sibling = tmp_node.get_sibling_with_label(Label.EMPTY)
            tmp_node.replace_direction_indicator(empty_child, Label.EMPTY)
            if empty_child.has_indicator(None):
                indicator = empty_child.get_indicator(None)
                indicator.replace_node_for_indicator(None, empty_sibling)

            # Updating direction indicators for full part
            # tmp_node is an endmost child, so skip empty part
            full_child = tmp_node.get_endmost_child_with_label(Label.FULL)
            full_sibling = tmp_node.get_sibling_with_label(Label.FULL)
            # At first replace direction indicator-sibling if tmp_node
            tmp_node.replace_direction_indicator(full_child, Label.FULL)
            if len(node.full_children) == 0:
                tmp_node.replace_direction_indicator(full_child, Label.PARTIAL)
            # Then update indicator which is sibling of tmp_node's child
            if full_child.has_indicator(None):
                indicator = full_child.get_indicator(None)
                indicator.replace_node_for_indicator(None, full_sibling)

        for partial_node in node.partial_children:
            for partial_node_sibling in partial_node.immediate_sublings:
                if partial_node_sibling is None:
                    # No need for update direction indicator if partial_node is the endmost child
                    partial_node_empty_child = partial_node.get_endmost_child_with_label(Label.EMPTY)
                    partial_node_empty_child.parent = node
                    node.replace_endmost_child(partial_node, partial_node_empty_child)
                else:
                    partial_node_child = partial_node.get_endmost_child_with_label(partial_node_sibling.label)
                    if partial_node_child is None:
                        partial_node_child = partial_node.get_endmost_child_with_label(Label.FULL)
                    partial_node_child.parent = node
                    partial_node_sibling.replace_sibling(partial_node, partial_node_child)

            node.full_children.extend(partial_node.full_children)
            partial_node.full_reset_node()

        node.partial_children = dllist()

        node.mark_partial()

        print("[Template_Q3] 2) result = True node: " + str(node.id))
        return True

    def unblock_sublings(self, node):
        assert node.mark == Mark.UNBLOCKED

        count = 0
        for subling in node.immediate_sublings:
            if subling is not None and subling.mark == Mark.BLOCKED:
                subling.parent = node.parent
                subling.mark = Mark.UNBLOCKED
                count += 1
                count += self.unblock_sublings(subling)
        return count

    @staticmethod
    def filter_sublings(node: PQnode, mark: Mark) -> list:
        sublings_to_return = []
        for sub in node.immediate_sublings:
            if sub and sub.mark == mark:
                sublings_to_return.append(sub)
        return sublings_to_return

    def reset_pseudo_node(self):
        if self.pseudo_node is None:
            return

        for i in range(2):
            self.pseudo_node.endmost_children[i].add_sibling(self.pseudo_siblings[i])
            self.pseudo_siblings[i].add_sibling(self.pseudo_node.endmost_children[i])
            # Just in case
            self.pseudo_node.endmost_children[i].parent = self.pseudo_siblings[i].parent

        self.root.full_children = self.pseudo_node.full_children
        for full_child in self.pseudo_node.full_children:
            full_child.parent = self.root

        # TODO: not sure about this
        self.root.mark_partial()

        self.pseudo_node.clear_endmost()
        self.pseudo_node = None

    def is_empty(self):
        return self.root is None

    def replace_full_children(self, node: PQnode, new_node: PQnode, iteration):
        return node.replace_full_children(new_node, iteration)

    def replace_node(self, node: PQnode, new_node: PQnode):
        if node == self.root:
            old_root = self.root
            self.root = new_node
            return old_root.collect_full_leaves()
        else:
            return node.replace(new_node)


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

    if tree.is_empty():
        return tree

    # Keep track of blocked nodes
    blocked_nodes = []

    # Initialize global variables
    QUEUE = myqueue.MyQueue()
    BLOCK_COUNT = 0
    BLOCKED_NODES = 0
    OFF_THE_TOP = 0

    for element in subset:
        # Ignore elements from the subset which is not in the tree
        if element.node_reference is None:
            continue
        QUEUE.push(element.node_reference)

    while QUEUE.size() + BLOCK_COUNT + OFF_THE_TOP > 1:
        if QUEUE.size() == 0:
            return PQtree([])

        # Get new node from queue and set BLOCKED mark by default
        node = QUEUE.pop()
        node.mark = Mark.BLOCKED

        # Get list of blocked/unblocked sublings
        blocked_sublings = PQtree.filter_sublings(node, Mark.BLOCKED)
        unblocked_sublings = PQtree.filter_sublings(node, Mark.UNBLOCKED)

        # If some subling is unblocked, then set parent pointer and mark node as unblocked
        if len(unblocked_sublings) > 0:
            node.parent = unblocked_sublings[0].parent
            node.mark = Mark.UNBLOCKED
        # If not an interior child of Qnode, than mark as unblocked
        elif node.get_num_siblings() < 2:
            node.mark = Mark.UNBLOCKED

        if node.mark == Mark.UNBLOCKED:
            node_parent = node.parent
            unblocked_sublings_count = 0

            # Now, if node has been unblocked, then we should make all adjacent previously blocked
            # sublings unblocked and set parent pointer to them
            if len(blocked_sublings) > 0:
                unblocked_sublings_count = tree.unblock_sublings(node)
                node_parent.pertinent_child_count += unblocked_sublings_count

            if node_parent is None:
                # Inform that root node has been reached
                # tree.pertinent_root = node
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
            blocked_nodes.append(node)

    if BLOCK_COUNT > 1 or (OFF_THE_TOP == 1 and BLOCK_COUNT != 0):
        return PQtree([])

    # Create a pseudo node
    if BLOCK_COUNT == 1 and BLOCKED_NODES > 1:
        pseudo_node = PQnode()
        pseudo_node.node_type = Type.Q_NODE
        pseudo_node.pertinent_child_count = 0
        pseudo_node.is_pseudo_node = True

        count = 0

        for blocked_node in blocked_nodes:
            # Some node could be unblocked by sibling, so just ignore them
            if blocked_node.mark == Mark.BLOCKED:
                pseudo_node.pertinent_child_count += 1
                pseudo_node.pertinent_leaf_count += blocked_node.pertinent_leaf_count
                blocked_node.parent = pseudo_node
                for i in range(2):
                    sibling = blocked_node.immediate_sublings[i]
                    # Check if sibling is from "outer" tree, then update references
                    if sibling.mark == Mark.UNMARKED:
                        blocked_node.remove_sibling(sibling)
                        sibling.remove_sibling(blocked_node)
                        # Remember sibling to restore it later
                        tree.pseudo_siblings[count] = sibling
                        count += 1
                        pseudo_node.add_endmost_child(blocked_node)
                        break

        tree.pseudo_node = pseudo_node

    return tree


def __reduce(tree, subset):
    global QUEUE, BLOCK_COUNT, BLOCKED_NODES, OFF_THE_TOP

    QUEUE = myqueue.MyQueue()
    subset_len = 0

    for leaf in subset:
        # Ignore elements from subset which is not in the tree
        if leaf.node_reference is None:
            continue
        subset_len += 1
        QUEUE.push(leaf.node_reference)
        leaf.node_reference.pertinent_leaf_count = 1

    while QUEUE.size() > 0:
        node = QUEUE.pop()
        if node.pertinent_leaf_count < subset_len:
            node_parent = node.parent

            node_parent.pertinent_leaf_count += node.pertinent_leaf_count
            node_parent.pertinent_child_count -= 1

            if node_parent.pertinent_child_count == 0:
                QUEUE.push(node_parent)

            if not PQtree.template_l1(node) and \
               not PQtree.template_p1(node, False) and \
               not PQtree.template_p3(node) and \
               not PQtree.template_p5(node) and \
               not PQtree.template_q1(node) and \
               not PQtree.template_q2(node):
                tree.reset_pseudo_node()
                return PQtree([])

        else:
            if not PQtree.template_l1(node) and \
               not PQtree.template_p1(node, True) and \
               not PQtree.template_p2(node) and \
               not tree.template_p4(node) and \
               not tree.template_p6(node) and \
               not PQtree.template_q1(node) and \
               not PQtree.template_q2(node) and \
               not PQtree.template_q3(node):
                tree.reset_pseudo_node()
                return PQtree([])

    tree.reset_pseudo_node()
    return tree


def reduce_tree(tree, subset):
    tree.pre_reset()
    tree = __bubble(tree, subset)
    if tree.is_empty():
        raise ReductionFailed()
    tree = __reduce(tree, subset)
    if tree.is_empty():
        raise ReductionFailed()

    tree.post_reset()
    return tree

