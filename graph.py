class Graph(object):

    def __init__(self):
        self.adjList = {}

    # Format:
    # edges: [(from, to)]
    def construct_graph(self, edges):
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
    def read_from_file(self, filename):
        parsed_edges = []
        f = open(filename, "r")
        for line in f.readlines():
            parsed = line.split("-")
            first_node = int(parsed[0])
            second_node = int(parsed[1])
            parsed_edges.append((first_node, second_node))

        self.construct_graph(parsed_edges)

    def compute_st_numbering(self):
        # FIXME: implement
        pass

    def get_edges_lower(self, number):
        edges = []
        for vertex in self.adjList.keys():
            if vertex == number:
                for adj_vertex in self.adjList[vertex]:
                    edges.append((vertex, adj_vertex))

        return edges

    def get_edges_higher(self, number):
        edges = []
        for vertex in self.adjList.keys():
            for adj_vertex in self.adjList[vertex]:
                if adj_vertex == number:
                    edges.append((vertex, adj_vertex))
        return edges

    def get_num_of_vertices(self):
        return len(self.adjList)

    def __str__(self):
        tmp_str = ""
        for vertex in self.adjList:
            tmp_str += str(vertex) + "-->" + str(self.adjList[vertex]) + "\n"
        return tmp_str

if __name__ == "__main__":
    graph = Graph()
    graph.read_from_file("tmp.txt")
    print(graph)
