from pqnode import PQnode, Type, Label


# Template L1
# Only applicable for leafs
# If leaf is in subset then mark it as full
# otherwise mark it as empty
def template_l1(node: PQnode, subset: set(PQnode)) -> bool:
    if node.node_type != Type.LEAF:
        return False

    if node in subset:
        node.label = Label.FULL
    else:
        node.label = Label.EMPTY
    return True


# Template P1
# Match P-node only
# If all children of P-node are empty, mark node as empty
# If all are full then mark node as full
def template_p1(node: PQnode) -> bool:
    if node.node_type != Type.P_NODE:
        return False

    if len(node.full_children) == node.child_count:
        node.label = Label.FULL
    elif len(node.full_children) == 0 and node.child_count != 0:
        node.label = Label.EMPTY
    else:
        return False
    return True


def template_p2(node: PQnode) -> bool:
    if node.node_type != Type.P_NODE:
        return False
    return False


def template_p3(node: PQnode) -> bool:
    if node.node_type != Type.P_NODE:
        return False
    return False


def template_p4(node: PQnode) -> bool:
    if node.node_type != Type.P_NODE:
        return False
    pass


def template_p5(node: PQnode) -> bool:
    if node.node_type != Type.P_NODE:
        return False

    if len(node.partial_children) != 1:
        return False

    partial_node = node.partial_children[0]
    # TODO: complete implementation

    return False


def template_p6(node: PQnode) -> bool:
    if node.node_type != Type.P_NODE:
        return False
    pass


def template_q1(node: PQnode) -> bool:
    if node.node_type != Type.Q_NODE:
        return False
    pass


def template_q2(node: PQnode) -> bool:
    if node.node_type != Type.Q_NODE:
        return False
    pass


def template_q3(node: PQnode) -> bool:
    if node.node_type != Type.Q_NODE:
        return False
    return False
