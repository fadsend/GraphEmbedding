from pqnode import Data
import random


class Edge(object):
    def __init__(self, vertex1, vertex2):
        self.vertices = (vertex1, vertex2)

    def get_higher(self):
        return max(self.vertices[0], self.vertices[1])

    def get_lower(self):
        return min(self.vertices[0], self.vertices[1])


class UndirectedEdge(Edge):

    def __eq__(self, other):
        return (self.vertices[0] == other.vertices[0] or self.vertices[0] == other.vertices[1]) and \
               (self.vertices[1] == other.vertices[0] or self.vertices[1] == other.vertices[1])

    def __str__(self):
        return str(self.vertices[0]) + " -- " + str(self.vertices[1])


class DirectedEdge(Edge):
    pass


class Graph(object):

    # TODO: temporary implementation. It should be changed for adjacency list
    def __init__(self):
        self.adj_list = {}
        self.edges_list = []
        self.num_of_vertices = 0

    def construct_graph_from_list(self, list_of_edges):
        tmp_vertices = []
        for edge in list_of_edges:
            if edge[0] not in tmp_vertices:
                self.num_of_vertices += 1
                tmp_vertices.append(edge[0])
            if edge[1] not in tmp_vertices:
                self.num_of_vertices += 1
                tmp_vertices.append(edge[1])

            self.edges_list.append(Data(UndirectedEdge(edge[0], edge[1])))

    def construct_graph_from_adj_list(self, adj_list):
        for i in adj_list.keys():
            self.num_of_vertices += 1
            for j in adj_list[i]:
                if j < i:
                    continue
                self.edges_list.append(Data(UndirectedEdge(i, j)))

    # 1 :[3, 4, 5]
    # 2: [4, 5, 6]
    # Format:
    # edges: [(from, to)]
    def construct_graph(self, edges):
        # Construct global list of all edges to use it as a reference
        tmp_list = []
        for edge in edges:
            tmp_list.append(Data(edge))
            self.edges_list[edge] = Data(edge)

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
        raise NotImplemented

    def get_edges_lower(self, number):
        #edges = []
        #for vertex in self.adjList.keys():
        #    if vertex == number:
        #        for adj_vertex in self.adjList[vertex]:
        #            if adj_vertex < vertex:
        #                continue
        #            if (vertex, adj_vertex) in self.edges_list.keys():
        #                edges.append(self.edges_list[(vertex, adj_vertex)])
        #            else:
        #                edges.append(self.edges_list[(adj_vertex, vertex)])
        #return edges
        edges = []
        for edge in self.edges_list:
            if edge.data.get_lower() == number:
                edges.append(edge)
        return edges

    def get_edges_higher(self, number):
        edges = []
        for edge in self.edges_list:
            if edge.data.get_higher() == number:
                edges.append(edge)
        return edges

        #edges = []
        #for vertex in self.adjList.keys():
        #    for adj_vertex in self.adjList[vertex]:
        #        if adj_vertex < vertex:
        #            continue
        #        if adj_vertex == number:
        #            if (vertex, adj_vertex) in self.edges_list:
        #                edges.append(self.edges_list[(vertex, adj_vertex)])
        #            else:
        #                edges.append(self.edges_list[(adj_vertex, vertex)])
        #return edges

    def get_num_of_vertices(self):
        # return len(self.adjList)
        return self.num_of_vertices

    def generate_random_graph(self, num_vertices, prob):
        adj_list = {}
        for i in range(num_vertices):
            for j in range(num_vertices):
                adj_list[i] = []
                if random.random() < prob:
                    adj_list[i].append(j)

        self.construct_graph_from_adj_list(adj_list)


    def __str__(self):
        tmp_str = ""
        for edge in self.edges_list:
            tmp_str += " " + str(edge) + " "
        #for vertex in self.adjList:
        #    tmp_str += str(vertex) + "-->" + str(self.adjList[vertex]) + "\n"
        return tmp_str

if __name__ == "__main__":
    graph = Graph()
    print(graph)
