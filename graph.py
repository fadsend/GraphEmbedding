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

    def __eq__(self, other):
        return self.vertices[0] == other.vertices[0] and self.vertices[1] == other.vertices[1] or \
               self.vertices[0] == other.vertices[1] and self.vertices[1] == other.vertices[0]

    def __hash__(self):
        return hash(self.vertices)


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
                if edge.vertices[i] not in tmp_vertices:
                    self.num_of_vertices += 1
                    self.adj_list[edge.vertices[i]] = []
                    self.new_adj_list[edge.vertices[i]] = []
                    tmp_vertices.append(edge.vertices[i])

            self.edges_list.append(Data(UndirectedEdge(edge.vertices[0], edge.vertices[1])))
            self.adj_list[edge.vertices[0]].append(edge.vertices[1])
            self.adj_list[edge.vertices[1]].append(edge.vertices[0])

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

    def has_edge(self, v, k):
        return v in self.adj_list.keys() and k in self.adj_list[v]

    def get_num_of_vertices(self):
        return self.num_of_vertices

    def find_cycle(self):
        cycle = []
        marks = {i: 0 for i in self.adj_list.keys()}

        def dfs_cycle(c, m, p, v):
            m[v] = 1
            for k in self.adj_list[v]:
                if k == p:
                    continue
                if not m[k]:
                    c.append((v, k))
                    if dfs_cycle(c, m, v, k):
                        return True
                    else:
                        c.pop()
                if m[k] == 1:
                    c.append((v, k))
                    tmp_c = []
                    for n in c:
                        if n[0] == k:
                            tmp_c.extend(c[n[0]:])
                            c = tmp_c[:]
                            return True
                    return True
            m[v] = 2
            return False

        if not dfs_cycle(cycle, marks, -1, list(self.adj_list.keys())[0]):
            return []
        else:
            result = []
            for e in cycle:
                result.append(e[0])
            return result

    def get_adjacent_vertices(self, vertex):
        return self.adj_list[vertex]

    def get_segments(self, cycle, neighbors):
        segments = []

        cycle_list = {i: False for i in self.adj_list.keys()}
        for i in cycle:
            cycle_list[i] = True

        already_processed = {i : False for i in self.adj_list.keys()}
        # Search for single-edge segments
        for v in cycle:
            for n in self.adj_list[v]:
                if already_processed[n]:
                    continue
                if not neighbors[v][n] and cycle_list[n]:
                    seg = Graph()
                    seg.construct_graph_from_list([Edge(v, n)])
                    segments.append(seg)
                    already_processed[v] = True

        def dfs_segment(start, dfs_marks, graph_cycle, segment):
            stack = [start]

            while len(stack) > 0:
                vertex = stack.pop()
                if not dfs_marks[vertex]:
                    dfs_marks[vertex] = True
                    for adj_vertex in self.adj_list[vertex]:
                        if not(vertex in graph_cycle and neighbors[vertex][adj_vertex]):
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
                if seg.get_num_of_vertices() != 0:
                    segments.append(seg)

        return segments

    def dfs_chain(self, marks, partial_embedding, chain, v):
        marks[v] = True
        chain.append(v)
        if len(chain) > 5:
            print("12")
        count_marks = 0
        for adj_v in self.adj_list[v]:
            if not marks[adj_v]:
                if adj_v not in partial_embedding:
                    if self.dfs_chain(marks, partial_embedding, chain, adj_v):
                        continue
                else:
                    chain.append(adj_v)
                return
            else:
                count_marks += 1
                if count_marks == len(self.adj_list[v]):
                    for t in self.adj_list[v]:
                        if t in partial_embedding:
                            return
                    chain.pop()
                    return True


    def get_chain(self, partial_embedding):
        chain = []
        marks = {i: False for i in self.adj_list.keys()}
        for v in self.adj_list.keys():
            if v in partial_embedding:
                if len(self.adj_list[v]) != 0:
                    self.dfs_chain(marks, partial_embedding, chain, v)
                    break

        print(chain)
        return chain

    # TODO: understand
    def face_has_segment(self, face, segment, partial_embedding):
        for v in self.adj_list.keys():
            for k in self.adj_list[v]:
                if segment.has_edge(v, k):
                    if v in partial_embedding and v not in face or \
                       k in partial_embedding and k not in face:
                        return False
        return True

    def compute_st_numbering(self):
        return None

    def get_edges(self):
        return self.edges_list

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
