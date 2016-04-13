from pqnode import PQnode, Type


class PQtree(object):

    def __init__(self, univers, subset):
        self.univers = univers
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
        new_node = PQnode(parent, node_type, data)
        parent.add_child(new_node)


def reduce(tree, subset):
    pass


def bubble(tree, subset):
    pass
