from pqnode import PQnode, Type


class PQtree(object):

    def __init__(self, univers, subset):
        self.univers = univers
        self.subset = subset
        self.root = None

    def constructFromGraph(self, graph):
        edges = graph.getEdgeNumbers()

        # TODO: change to logger
        print("[PQtree::constructFromGraph] Edges: " + str(edges))

        self.root = PQnode(None, Type.P_NODE)

        for edge in edges:
            self.addNode(self.root, Type.LEAF, edge)

    def addChild(self, parent, nodeType, data):
        newNode = PQnode(parent, nodeType, data)
        parent.addChild(newNode)


def Reduce(tree, subset):
    pass


def Bubble(tree, subset):
    pass
