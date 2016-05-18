from pqnode import Data
from enum import Enum


class Edge(object):
    def __init__(self, vertex1, vertex2):
        self.vertices = (vertex1, vertex2)

    def get_higher(self):
        return max(self.vertices[0], self.vertices[1])

    def get_lower(self):
        return min(self.vertices[0], self.vertices[1])

    def __str__(self):
        return "(" + str(self.vertices[0]) + ", " + str(self.vertices[1]) + ")"


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

    def add_edge(self, edge):
        assert type(edge) == Edge
        self.edges_list.append(edge)
        v0 = edge.vertices[0]
        v1 = edge.vertices[1]

        if v0 in self.adj_list and v1 in self.adj_list:
            if v0 in self.adj_list[v1] and v1 in self.adj_list[v0]:
                return

        if v0 not in self.adj_list.keys():
            self.adj_list[v0] = [v1]
            self.num_of_vertices += 1
        else:
            self.adj_list[v0].append(v1)

        if v1 not in self.adj_list.keys():
            self.adj_list[v1] = [v0]
            self.num_of_vertices += 1
        else:
            self.adj_list[v1].append(v0)

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
        max_cycle = []

        def dfs_visit(start):
            stack = []
            path = []
            marks = {i: False for i in self.adj_list.keys()}
            stack.append(start)

            while len(stack) > 0:
                v = stack.pop()
                if not marks[v]:
                    path.append(v)
                    marks[v] = True
                    for adj_v in self.get_adjacent_vertices(v):
                        stack.append(adj_v)
                else:
                    # Check for backward edges
                    if len(path) >= 2 and path[-2] == v:
                        continue
                    path.append(v)
                    # Remove excess vertices from path
                    return path[path.index(v):]
            return []

        # TODO: not sure it worth to check every vertex for cycle
        # or just stop when the first one is found
        # It seems that for every vertex dfs would return the same
        # cycle in most cases
        for i in self.adj_list.keys():
            cycle = dfs_visit(i)
            print(cycle)
            if len(cycle) > len(max_cycle):
                max_cycle = cycle
        return max_cycle[:-1]

    def get_adjacent_vertices(self, vertex):
        return self.adj_list[vertex]

    # TODO: use dict with True/False in vertex in cycle
    def get_segments(self, cycle):
        segments = []

        # Collect neighbours for the vertices in the cycle to
        # distinguish edges between them with one-edge segments
        neighbors = {}
        for i in range(1, len(cycle) - 1):
            neighbors[cycle[i]] = (cycle[i - 1], cycle[i + 1])
        neighbors[cycle[0]] = (cycle[1], cycle[-1])
        neighbors[cycle[-1]] = (cycle[-2], cycle[0])

        # Search for single-edge segments
        for v in cycle:
            for n in self.adj_list[v]:
                if n not in neighbors[v] and n in cycle:
                    seg = Graph()
                    seg.construct_graph_from_list([Edge(v, n)])
                    segments.append(seg)

        def dfs_segment(start, dfs_marks, graph_cycle, segment):
            stack = [start]

            while len(stack) > 0:
                vertex = stack.pop()
                if not dfs_marks[vertex]:
                    dfs_marks[vertex] = True
                    for adj_vertex in self.adj_list[vertex]:
                        if not(vertex in graph_cycle and adj_vertex in neighbors[vertex]):
                            segment.add_edge(Edge(vertex, adj_vertex))
                        if adj_vertex not in graph_cycle:
                            stack.append(adj_vertex)
                        else:
                            dfs_marks[adj_vertex] = True

        # Search for segments with multiple edges
        marks = {i: False for i in self.adj_list.keys()}
        for v in cycle:
            if not marks[v]:
                seg = Graph()
                dfs_segment(v, marks, cycle, seg)
                segments.append(seg)

        return segments

    def embedded_on_face(self, face, segment):
        raise NotImplementedError()

    def compute_st_numbering(self):
        return None
  #      raise NotImplementedError()

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
