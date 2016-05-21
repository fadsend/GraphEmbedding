from enum import Enum
from llist import dllist


class Type(Enum):
    Q_NODE = 1
    P_NODE = 2
    LEAF = 3
    DIRECTION_INDICATOR = 4


class Label(Enum):
    FULL = 1
    EMPTY = 2
    PARTIAL = 3


class Mark(Enum):
    UNMARKED = 1
    QUEUED = 2
    BLOCKED = 3
    UNBLOCKED = 4


class PnodeIterator:
    def __init__(self, node):
        assert node is not None
        self.node = node

    def __iter__(self):
        return iter(self.node.circular_link)


class QnodeIterator:
    def __init__(self, node):
        self.current = node.endmost_children[0]
        self.prev = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration

        child_to_return = self.current

        tmp_node = self.current.immediate_sublings[0]
        if tmp_node == self.prev:
            tmp_node = self.current.immediate_sublings[1]
        self.prev = self.current
        self.current = tmp_node
        return child_to_return


class DirectionIndicator(object):
    id_counter = 0
    list_of_instances = []

    def __init__(self, data):
        self.data = data
        self.id = DirectionIndicator.id_counter
        DirectionIndicator.id_counter += 1
        print("INDICATOR CREATED WITH ID = " + str(self.id))
        DirectionIndicator.list_of_instances.append(self)
        # print("Direction indicator #" + str(self.id) + " is created")
        self.prev_node = None
        self.next_node = None

    def set_next_for_indicator(self, node):
        self.next_node = node
        if node:
            node.prev_indicator = self

    def set_prev_for_indicator(self, node):
        self.prev_node = node
        if node:
            node.next_indicator = self

    def replace_node_for_indicator(self, old_node, new_node, label=None):
        assert self.next_node or self.prev_node
        result = False

        # TODO: not sure what to do with prev_node == None or next_node == None
        if self.next_node == old_node:
            if label:
                if self.prev_node and self.prev_node.label == label:
                    self.set_next_for_indicator(new_node)
                    result = True
            else:
                self.set_next_for_indicator(new_node)
                result = True

        if self.prev_node == old_node:
            if label:
                if self.next_node and self.next_node.label == label:
                    self.set_prev_for_indicator(new_node)
                    result = True
            else:
                self.set_prev_for_indicator(new_node)
                result = True
        return result

    def add_node_for_indicator(self, new_node):
        assert self.next_node or self.prev_node
        assert not self.next_node and not self.prev_node
        assert not new_node.next_indicator and not new_node.prev_indicator

        if self.prev_node:
            self.set_next_for_indicator(new_node)
            return
        if self.next_node:
            self.set_prev_for_indicator(new_node)
            return

    def has_nodes(self, node1, node2):
        if self.next_node == node1 and self.prev_node == node2:
            return True
        if self.next_node == node2 and self.prev_node == node1:
            return True
        return False

    def clear_nodes(self):
        if self.next_node:
            self.next_node.prev_indicator = None
            self.next_node = None
        if self.prev_node:
            self.prev_node.next_indicator = None
            self.prev_node = None

    def __str__(self):
        return str(self.data)


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

    def __init__(self, node_type=Type.LEAF, data=None):
        # Number of children nodes
        # self.child_count = 0
        self.id = PQnode.id_counter
        PQnode.id_counter += 1

        # Linked list of node's children. Used only by P-node.
        self.circular_link = dllist()

        # Reference to the last node's child. Used only by Q-node.
        self.endmost_children = [None, None]

        # Set of full node's children
        self.full_children = dllist()

        # Tuple of immediate sublings.
        # For children of P-node it just a (None, None)
        # For endmost children of Q-node it is (node, None) or (None, node)
        # For interior children of Q-node it is (None, None)
        self.immediate_sublings = [None, None]

        # Node's label: EMPTY, FULL or PARTIAL
        self.label = Label.EMPTY

        # Node's mark: UNMARKED, QUEUED(placed into queue), BLOCKED(hasn't pointer to parent)
        # and UNBLOCKED(when it receives pointer to parent node)
        self.mark = Mark.UNMARKED

        # Pointer to parent node.
        self.parent = None

        # Flag if the current node is pseudo node
        self.is_pseudo_node = False

        # Set of all partial children of the node
        self.partial_children = dllist()

        # Number of pertinent children Full or partial
        self.pertinent_child_count = 0

        # Number of pertinent leafs
        self.pertinent_leaf_count = 0

        # Node type: LEAF, P_NODE, Q_NODE or DIRECTION_INDICATOR
        self.node_type = node_type

        # Additional field to handle direction of indicator
        self.prev_indicator = None
        self.next_indicator = None

        # Reference to node data(like id of edge)
        self.data = data
        if self.data is not None:
            self.data.node_reference = self
        else:
            print("New node is created: id = " + str(self.id))

        # Aux references for lists of its parent
        self.full_list_node = None
        self.circular_list_node = None
        self.queue_list_node = None
        self.partial_list_node = None

    def get_num_siblings(self):
        count = 0
        for subling in self.immediate_sublings:
            if subling is not None:
                count += 1
        return count

    def set_pertinent_child_count(self, new_value):
        self.pertinent_child_count = new_value

    def get_pertinent_child_count(self):
        return self.pertinent_child_count

    def inc_pertinent_child_count(self):
        self.pertinent_child_count += 1

    def move_full_children(self, new_node):
        for full_child in self.full_children:
            self.circular_link.remove(full_child.circular_list_node)
            full_child.circular_list_node = new_node.circular_link.append(full_child)
            full_child.parent = new_node
            full_child.full_list_node = new_node.full_children.append(full_child)

        self.full_children = dllist()

    # Useful to move empty children after full were already moved
    def move_children(self, new_node):
        for child in self.circular_link:
            child.circular_list_node = new_node.circular_link.append(child)
            child.parent = new_node

        self.circular_link = dllist()

    # Replaces child of node depending on current type
    def replace_child(self, old_child, new_child):
        assert self.node_type != Type.LEAF

        if self.node_type == Type.P_NODE:
            self.circular_link.remove(old_child.circular_list_node)
            new_child.circular_list_node = self.circular_link.append(new_child)
        else:
            old_child.replace_qnode_child(new_child)

    def clear_siblings(self):
        for i in range(2):
            self.immediate_sublings[i] = None

    def clear_endmost(self):
        for i in range(2):
            self.endmost_children[i] = None

    def replace_qnode_child(self, new_node):
        new_node.clear_siblings()

        for i in range(2):
            if self.parent.endmost_children[i] == self:
                self.parent.endmost_children[i] = new_node
            if self.immediate_sublings[i] is not None:
                self.immediate_sublings[i].replace_sibling(self, new_node)

        self.clear_siblings()
        self.parent = None

    # TODO: not sure about lists here
    def replace(self, new_node):
        # assert self.node_type == Type.P_NODE
        assert self.parent is not None

        adjacency_list = []
        if self.node_type != Type.LEAF:
            for full_child in self.full_children:
                adjacency_list.extend(full_child.collect_full_leaves())
        else:
            adjacency_list = [self]

        parent_node = self.parent
        parent_node.replace_child(self, new_node)
        parent_node.full_children = dllist()
        new_node.full_list_node = parent_node.full_children.append(new_node)
        new_node.parent = parent_node
        return adjacency_list

    def replace_full_children(self, new_node, iteration):
        assert new_node.node_type == Type.P_NODE or new_node.node_type == Type.LEAF
        assert self.node_type == Type.Q_NODE

        endmost_full_children = []

        # Special case for single full children
        if len(self.full_children) == 1:
            full_child = self.full_children.nodeat(0).value
            adjacency_list = []
            for i in range(2):
                if full_child.immediate_sublings[i]:
                    full_child.immediate_sublings[i].replace_sibling(full_child, new_node)
                if self.endmost_children[i] == full_child:
                    self.replace_endmost_child(full_child, new_node)
            self.full_children = dllist()
            adjacency_list.append(full_child)
            next_indicator_found = False
            if full_child.next_indicator:
                next_indicator_found = True
                indicator = full_child.next_indicator
                if int(indicator.data) == full_child.data.data.get_lower():
                    adjacency_list.append("|" + str(full_child.next_indicator) + ">")
                    full_child.next_indicator.clear_nodes()
                else:
                    print("!!!Will be proceeded later")

            if full_child.prev_indicator:
                indicator = full_child.prev_indicator
                if int(indicator.data) == full_child.data.data.get_lower():
                    if next_indicator_found:
                        adjacency_list.append("<" + str(full_child.prev_indicator) + "|")
                    else:
                        adjacency_list.append("|" + str(full_child.prev_indicator) + ">")
                    full_child.prev_indicator.clear_nodes()
            return adjacency_list

        # Only need to update pointers for first and last full children
        for full_child in self.full_children:
            for i in range(2):
                if full_child.immediate_sublings[i] is None:
                    # Full child is the endmost also should update
                    endmost_full_children.append(full_child)
                elif full_child.immediate_sublings[i].label != Label.FULL:
                    # Found endmost full children save it
                    endmost_full_children.append(full_child)

            if len(endmost_full_children) == 2:
                # Both endmost full children are found, so no
                # need to proceed
                break

        assert len(endmost_full_children) == 2

        found_direction_indicators = []
        adjacency_list = []
        count = 0
        # Iterate from one endmost full child to another since order of self.full_children
        # could differ from actual one. It's a bit re-written version of QnodeIterator
        prev_child = endmost_full_children[0].get_sibling_with_label(Label.EMPTY)
        full_child = endmost_full_children[0]
        while True:
            if full_child is None or full_child.label != Label.FULL:
                break
            actual_child = full_child
            next_child = full_child.immediate_sublings[0]
            if next_child == prev_child:
                next_child = full_child.immediate_sublings[1]
            prev_child = full_child
            full_child = next_child
            # # Check if direction indicator is present and add it to a list if it is
            # if actual_child.prev_indicator:
            #     # Prev indicator will be added only at first or last iteration
            #     # Check iteration
            #     indicator = actual_child.prev_indicator
            #     if int(indicator.data) == actual_child.data.data.get_lower():
            #         if count == 0:
            #             # We at the first iteration, so prev in a right direction
            #             # Check just in case
            #             if actual_child.prev_indicator not in found_direction_indicators:
            #                 found_direction_indicators.append(actual_child.prev_indicator)
            #                 adjacency_list.append("|" + str(actual_child.prev_indicator) + ">")
            #             else:
            #                 print("Indicator again 1")
            #         else:
            #             # Last iteration
            #             if actual_child.prev_indicator not in found_direction_indicators:
            #                 found_direction_indicators.append(actual_child.prev_indicator)
            #                 adjacency_list.append("<" + str(actual_child.prev_indicator) + "|")
            #             else:
            #                 print("Indicator again 2")
            #     else:
            #         print("Indicator differs from lower edge value, will be processes later")
            # if actual_child.next_indicator:
            #     # In case of next indicator should check only last one
            #     indicator = actual_child.next_indicator
            #     if indicator.next_node is None or indicator.next_node.label != Label.FULL:
            #         if int(indicator.data) == actual_child.data.data.get_lower():
            #             if actual_child.next_indicator not in found_direction_indicators:
            #                 found_direction_indicators.append(actual_child.next_indicator)
            #                 if count != 0:
            #                     adjacency_list.append("|" + str(actual_child.next_indicator) + ">")
            #                 else:
            #                     adjacency_list.append("<" + str(actual_child.next_indicator) + "|")
            #             else:
            #                 print("Repeated indicator 1")
            #         else:
            #             print("Indicator will be proceeded later.")
            #     else:
            #         if actual_child.next_indicator not in found_direction_indicators:
            #             found_direction_indicators.append(actual_child.next_indicator)
            #             adjacency_list.append("|" + str(actual_child.next_indicator) + ">")
            #         else:
            #             print("Repeated indicator 2")
            if actual_child.next_indicator:
                if actual_child.next_indicator not in found_direction_indicators:
                    found_direction_indicators.append(actual_child.next_indicator)
                    adjacency_list.append(actual_child.next_indicator)
            if actual_child.prev_indicator:
                if actual_child.prev_indicator not in found_direction_indicators:
                    found_direction_indicators.append(actual_child.prev_indicator)
                    adjacency_list.append(actual_child.prev_indicator)
            adjacency_list.extend(actual_child.collect_full_leaves())

        # Process direction indicators along with the nodes
        # At first, check corner indicators for value
        # Find nearest node
        has_some_nodes = True
        top_index = 0
        bottom_index = len(adjacency_list) - 1
        while type(adjacency_list[top_index]) != PQnode:
            top_index += 1
            if top_index == len(adjacency_list):
                has_some_nodes = False

        while type(adjacency_list[bottom_index]) != PQnode:
            bottom_index -= 1
            if bottom_index == 0:
                has_some_nodes = False

        assert has_some_nodes

        count = 0
        while count < top_index:
            if type(adjacency_list[0]) == DirectionIndicator:
                if adjacency_list[0].data != adjacency_list[top_index].data.data.get_lower():
                    adjacency_list.pop(0)
            count += 1

        count = 0
        while count > bottom_index:
            if type(adjacency_list[-1]) == DirectionIndicator:
                if adjacency_list[-1].data != adjacency_list[top_index].data.data.get_lower():
                    adjacency_list.pop(-1)
            count -= 1

        # TODO: check if one more iteration is needed
        for idx in range(bottom_index, top_index):
            if type(adjacency_list[idx]) == DirectionIndicator:
                if adjacency_list[idx].next_node == adjacency_list[idx + 1]:
                    adjacency_list[idx] = "|" + str(adjacency_list[idx]) + ">"
                elif adjacency_list[idx].prev_node == adjacency_list[idx + 1]:
                    adjacency_list[idx] = "<" + str(adjacency_list[idx]) + "|"

        # found_direction_indicators = []

        # for indicator in found_direction_indicators:
        #     indicator.clear_nodes()

        direction_indicator = DirectionIndicator(str(iteration))

        sibling1 = endmost_full_children[0].get_sibling_with_label(Label.EMPTY)
        sibling2 = endmost_full_children[1].get_sibling_with_label(Label.EMPTY)

        if sibling1 is None and sibling2 is None:
            # Q-node consist only of full children
            self.replace_endmost_child(endmost_full_children[0], new_node)
            self.replace_endmost_child(endmost_full_children[1], new_node)
        elif sibling1 is not None and sibling2 is None:
            sibling1.replace_sibling(endmost_full_children[0], new_node)
            self.replace_endmost_child(endmost_full_children[1], new_node)
        elif sibling2 is not None and sibling1 is None:
            sibling2.replace_sibling(endmost_full_children[1], new_node)
            self.replace_endmost_child(endmost_full_children[0], new_node)
        else:
            # Replace siblings with new node
            # new_node's siblings are updated there
            sibling1.replace_sibling(endmost_full_children[0], new_node)
            sibling2.replace_sibling(endmost_full_children[1], new_node)

        direction_indicator.set_next_for_indicator(new_node)
        direction_indicator.set_prev_for_indicator(sibling1)

        self.full_children = dllist()
        # Add new node to the list of full children
        new_node.parent = self
        new_node.mark_full()

        # Only one children remain
        if self.endmost_children[0] == self.endmost_children[1]:
            # Special case for the last iteration. We could have
            # Q-node as a root with single empty P-node child
            if len(self.endmost_children[0].circular_link) == 0:
                return adjacency_list
            self.replace_qnode(self.endmost_children[0])

        if not self.is_valid_qnode():
            self.update_to_pnode()

        return adjacency_list

    def is_valid_qnode(self):
        assert self.node_type == Type.Q_NODE
        assert self.endmost_children[0].get_num_siblings() != 0 and \
               self.endmost_children[1].get_num_siblings() != 0

        if self.endmost_children[0].has_sibling(self.endmost_children[1]) or \
           self.endmost_children[1].has_sibling(self.endmost_children[0]):
            return False

        return True

    def update_to_pnode(self):
        for child in self.iter_children():
            child.circular_list_node = self.circular_link.append(child)

        self.clear_endmost()
        self.clear_siblings()
        self.node_type = Type.P_NODE

    def has_sibling(self, node):
        return self.immediate_sublings[0] == node or \
               self.immediate_sublings[1] == node

    def replace_qnode(self, new_node):
        raise NotImplementedError()

    def count_siblings(self):
        count = 0
        for i in range(2):
            if self.immediate_sublings[i] is not None:
                count += 1
        return count

    def count_endmost(self):
        count = 0
        for i in range(2):
            if self.endmost_children[i] is not None:
                count += 1
        return count

    def replace_sibling(self, old_node, new_node):
        for i in range(2):
            if self.immediate_sublings[i] is not None and \
               self.immediate_sublings[i] == old_node:
                self.immediate_sublings[i] = new_node

        if new_node is not None:
            new_node.immediate_sublings[new_node.count_siblings()] = self

    def remove_sibling(self, sibling):
        assert sibling in self.immediate_sublings

        if self.immediate_sublings[1] == sibling:
            self.immediate_sublings[1] = None
        elif self.immediate_sublings[0] == sibling:
            self.immediate_sublings[0] = self.immediate_sublings[1]
            self.immediate_sublings[1] = None

    def add_sibling(self, node):
        idx = self.count_siblings()
        assert idx < 2
        self.immediate_sublings[idx] = node

    def add_endmost_child(self, node):
        idx = self.count_endmost()
        assert idx < 2
        self.endmost_children[idx] = node

    def replace_endmost_child(self, old_node, new_node):
        assert self.node_type == Type.Q_NODE
        for i in range(2):
            if self.endmost_children[i] == old_node:
                self.endmost_children[i] = new_node
                return
        return

    # Replace old_child with new_child which is partial q-node
    def replace_partial_child(self, old_child, new_child):
        new_child.parent = self

        # Add to list of partial children for each type of node
        new_child.partial_list_node = self.partial_children.append(new_child)
        if old_child in self.partial_children:
            self.partial_children.remove(old_child.partial_list_node)

        self.replace_child(old_child, new_child)

    # Generic routine for searching in self.endmost_children
    # or self.immediate_sibling with specific label
    @staticmethod
    def __get_with_label(array, label):
        for i in range(2):
            if array[i] is None:
                return None
            if array[i].label == label:
                return array[i]
        return None

    def get_endmost_child_with_label(self, label):
        assert self.node_type == Type.Q_NODE
        return self.__get_with_label(self.endmost_children, label)

    def get_sibling_with_label(self, label):
        return self.__get_with_label(self.immediate_sublings, label)

    def get_siblings_with_label(self, label):
        return (self.__get_with_label(self.immediate_sublings, label),
                self.__get_with_label(self.immediate_sublings[1:], label))

    # TODO: should avoid "in" operator here
    def mark_full(self):
        self.label = Label.FULL
        if self.parent is not None and \
           self not in self.parent.full_children:
            self.full_list_node = self.parent.full_children.append(self)

    def mark_empty(self):
        self.label = Label.EMPTY

    # TODO: the same as for mark_full
    def mark_partial(self):
        self.label = Label.PARTIAL
        if self.parent is not None and \
           self not in self.parent.partial_children:
            self.partial_list_node = self.parent.partial_children.append(self)

    def __str__(self):
        return str(self.data)

    def reset(self):
        if self.node_type != Type.LEAF:
            for child in self.iter_children():
                child.reset()

        # Common part for all nodes
        self.full_children = dllist()
        self.partial_children = dllist()
        self.pertinent_child_count = 0
        self.pertinent_leaf_count = 0
        self.mark = Mark.UNMARKED
        self.label = Label.EMPTY
        self.is_pseudo_node = False

    def full_reset_node(self):
        self.full_children = dllist()
        self.partial_children = dllist()
        self.pertinent_child_count = 0
        self.pertinent_leaf_count = 0
        self.mark = Mark.UNMARKED
        self.label = Label.EMPTY
        self.clear_siblings()
        self.clear_endmost()
        self.circular_link = dllist()
        self.is_pseudo_node = False

    def add_child(self, node_type, data=None):
        new_node = PQnode(node_type=node_type, data=data)
        new_node.parent = self

        if self.node_type == Type.P_NODE:
            new_node.circular_list_node = self.circular_link.append(new_node)
        else:
            if self.endmost_children[0] is not None:
                tmp_node = self.endmost_children[1]
                self.replace_endmost_child(tmp_node, new_node)
                if tmp_node is not None:
                    tmp_node.add_sibling(new_node)
                    new_node.add_sibling(tmp_node)
                else:
                    self.endmost_children[0].add_sibling(new_node)
                    new_node.add_sibling(self.endmost_children[0])
            else:
                # Actually, Q-node should have at least 3 children,
                # but let's break the rule for test purpose
                self.endmost_children[0] = new_node
        return new_node

    def iter_children(self):
        assert self.node_type != Type.LEAF

        if self.node_type == Type.P_NODE:
            return PnodeIterator(self)
        else:
            return QnodeIterator(self)

    def full_or_partial_children_are_consecutive(self):
        # TODO: understand or re-write
        if len(self.full_children) + len(self.partial_children) <= 1:
            return True

        label_count = {
            Label.EMPTY: 0,
            Label.FULL: 0,
            Label.PARTIAL: 0
        }

        for full_child in self.full_children:
            for i in range(2):
                if full_child.immediate_sublings[i]:
                    label_count[full_child.immediate_sublings[i].label] += 1

        for partial_child in self.partial_children:
            for i in range(2):
                if partial_child.immediate_sublings[i]:
                    label_count[partial_child.immediate_sublings[i].label] += 1

        if label_count[Label.PARTIAL] != len(self.partial_children):
            return False

        if label_count[Label.FULL] != (len(self.full_children) * 2) - (2 - label_count[Label.PARTIAL]):
            return False

        return True

    def collect_full_leaves(self, do_not_stringify=False):
        assert self.label == Label.FULL
        if self.node_type == Type.LEAF:
            return [self]
        full_leaves = []
        found_direction_indicators = []
        for child in self.iter_children():
            if child.prev_indicator:
                if child.prev_indicator not in found_direction_indicators:
                    found_direction_indicators.append(child.prev_indicator)
                    if do_not_stringify:
                        full_leaves.append(child.prev_indicator)
                else:
                    print("Repeated indicator 12")
            if child.next_indicator:
                if child.next_indicator not in found_direction_indicators:
                    found_direction_indicators.append(child.next_indicator)
                    if do_not_stringify:
                        full_leaves.append(child.next_indicator)
                else:
                    print("Repeated indicator 22")
            if child.node_type == Type.LEAF:
                full_leaves.append(child)
            else:
                full_leaves.extend(child.collect_full_leaves())
        return full_leaves

    def replace_direction_indicator(self, new_node, label=None):
        if not self.next_indicator and not self.prev_indicator:
            print("No indicator for the node")
            return

        if self.next_indicator:
            if self.next_indicator.replace_node_for_indicator(self, new_node, label):
                self.next_indicator = None

        if self.prev_indicator:
            if self.prev_indicator.replace_node_for_indicator(self, new_node, label):
                self.prev_indicator = None

    def has_indicator(self, other_node) -> bool:
        if self.prev_indicator:
            if self.prev_indicator.has_nodes(self, other_node):
                return True

        if self.next_indicator:
            if self.next_indicator.has_nodes(self, other_node):
                return True
        return False

    def get_indicator(self, other_node) -> DirectionIndicator:
        if self.prev_indicator:
            if self.prev_indicator.has_nodes(self, other_node):
                return self.prev_indicator

        if self.next_indicator:
            if self.next_indicator.has_nodes(self, other_node):
                return self.prev_indicator
        return None


