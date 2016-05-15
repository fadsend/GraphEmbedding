from pqnode import Data
from enum import Enum


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


class GraphException(Exception):
    pass


class Color(Enum):
    WHITE = 1
    GRAY = 2
    BLACK = 3


class Graph(object):

    # TODO: temporary implementation. It should be changed for adjacency list
    def __init__(self):
        self.adj_list = {}
        # Use another adjacency list to save initial graph
        self.new_adj_list = {}
        self.edges_list = []
        self.num_of_vertices = 0

    def construct_graph_from_list(self, list_of_edges):
        tmp_vertices = []
        for edge in list_of_edges:
            for i in range(2):
                if edge[i] not in tmp_vertices:
                    self.num_of_vertices += 1
                    self.adj_list[edge[i]] = []
                    self.new_adj_list[edge[i]] = []
                    tmp_vertices.append(edge[i])

            self.edges_list.append(Data(UndirectedEdge(edge[0], edge[1])))
            self.adj_list[edge[0]].append(edge[1])
            self.adj_list[edge[1]].append(edge[0])

    def construct_graph_from_adj_list(self, adj_list: dict):
        for i in adj_list.keys():
            self.num_of_vertices += 1
            for j in adj_list[i]:
                if j < i:
                    continue
                self.edges_list.append(Data(UndirectedEdge(i, j)))
            self.new_adj_list[i] = []
        self.adj_list = adj_list.copy()

    def generate_random_graph(self, num_vertices, prob):
        raise NotImplementedError()

    def read_from_file(self, filename):
        parsed_edges = []
        f = open(filename, "r")
        for line in f.readlines():
            parsed = line.split("-")
            first_node = int(parsed[0])
            second_node = int(parsed[1])
            parsed_edges.append((first_node, second_node))
        raise NotImplementedError()

    def compute_st_numbering(self):
        raise NotImplementedError()

    # FIXME: implement more effectively
    def get_edges_lower(self, number):
        edges = []
        for edge in self.edges_list:
            if edge.data.get_lower() == number:
                edges.append(edge)
        return edges

    # FIXME: implement more effectively
    # Perhaps it would be better to use map for storing edges
    def get_edges_higher(self, number):
        edges = []
        for edge in self.edges_list:
            if edge.data.get_higher() == number:
                edges.append(edge)
        return edges

    def get_num_of_vertices(self):
        return self.num_of_vertices

    def find_cycle(self):
        marked = {v: False for v in self.adj_list.keys()}
        path = []

        #for v in self.adj_list.keys():
        #    res = False
        #    if not marked[v]:
        #        path, res = self.dfs(v, True)
        #    if res:
        #        break
        #return path

    # TODO: Implement working version
    def dfs_cycle(self, start=1):
        stack = []
        labels = {i: Color.WHITE for i in self.adj_list.keys()}
        path = []
        labels[start] = Color.GRAY
        stack.append(start)
        while len(stack) > 0:
            v = stack.pop()
            for neighbour in self.get_adjacent_vertices(v):
                if labels[neighbour] == Color.GRAY:
                    return path
                elif labels[neighbour] == Color.WHITE:
                    labels[neighbour] = Color.GRAY
                    stack.append(neighbour)
                else:
                    # XXX: How it could happend???
                    pass
            path.append(v)
            if not labels[v]:
                labels[v] = True
                for new_vertex in self.get_adjacent_vertices(v):
                    if not labels[new_vertex]:
                        stack.append(new_vertex)
        return path, False

    def get_adjacent_vertices(self, vertex):
        return self.adj_list[vertex]

    def __str__(self):
        tmp_str = ""
        for edge in self.edges_list:
            tmp_str += " " + str(edge) + " "
        return tmp_str

    def print_adj(self):
        print(self.adj_list)

if __name__ == "__main__":
    graph = Graph()
    print(graph)
