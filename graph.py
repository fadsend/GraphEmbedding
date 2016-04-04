class Graph(object):

    def __init__(self):
        self.adjList = {}

    # Format:
    # edges: [(from, to)]
    def constructGraph(self, edges):
        for edge in edges:
            first = edge[0]
            second = edge[1]
            if first not in self.adjList:
                self.adjList[first] = []
            if second is not None:
                self.adjList[first].append(second)

            if second not in self.adjList:
                self.adjList[second] = []
            self.adjList[second].append(first)

    # Format:
    # 1 - 2
    # 3 - 2
    def readFromFile(self, filename):
        parsedEdges = []
        f = open(filename, "r")
        for line in f.readlines():
            parsed = line.split("-")
            firstNode = int(parsed[0])
            secondNode = int(parsed[1])
            parsedEdges.append((firstNode, secondNode))

        self.constructGraph(parsedEdges)

    def __str__(self):
        tmpStr = ""
        for vertex in self.adjList:
            tmpStr += str(vertex) + "-->" + str(self.adjList[vertex]) + "\n"
        return tmpStr

if __name__ == "__main__":
    graph = Graph()
    graph.readFromFile("tmp.txt")
    print(graph)
