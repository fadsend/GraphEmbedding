from pqnode import Data
from enum import Enum
import random


class Edge(object):
    def __init__(self, vertex1, vertex2):
        self.vertices = (vertex1, vertex2)

    def get_higher(self):
        return max(self.vertices[0], self.vertices[1])

    def get_lower(self):
        return min(self.vertices[0], self.vertices[1])

    def get_opposite(self, v):
        if self.vertices[0] == v:
            return self.vertices[1]
        elif self.vertices[1] == v:
            return self.vertices[0]
        else:
            assert False

    def __str__(self):
        return "(" + str(self.vertices[0]) + ", " + str(self.vertices[1]) + ")"

    def __eq__(self, other):
        if other is None:
            return False
        return self.vertices[0] == other.vertices[0] and self.vertices[1] == other.vertices[1] or \
               self.vertices[0] == other.vertices[1] and self.vertices[1] == other.vertices[0]

    def __hash__(self):
        return hash(tuple(sorted(self.vertices)))


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
    # TODO: temporary, should be removed
    st_edge = None
    # TODO: temporary implementation. It should be changed for adjacency list
    def __init__(self):
        self.adj_list = {}
        # Use another adjacency list to save initial graph
        self.new_adj_list = {}
        self.edges_list = []
        self.num_of_vertices = 0
        # Store old vertex numbers when st-numbering is computed
        self.vertex_mapping = {}
        self.st_edge = Graph.st_edge
        self.adj_edges_list = {}

        self.use_matrix = False
        self.adj_matrix = []

    def fill_adj_matrix(self):
        self.adj_matrix = [[False] * len(self.adj_list.keys())] * len(self.adj_list.keys())
        for i in self.adj_list.keys():
            for j in self.adj_list[i]:
                self.adj_matrix[i][j] = True
                self.adj_matrix[j][i] = True

    def set_matrix_use(self, max_size):
        self.use_matrix = True
        self.adj_matrix = [[False for _ in range(max_size)] for _ in range(max_size)]

    def add_edge(self, edge):
        assert type(edge) == Edge
        self.edges_list.append(edge)
        v0 = edge.vertices[0]
        v1 = edge.vertices[1]

        if v0 not in self.adj_edges_list:
            self.adj_edges_list[v0] = []

        self.adj_edges_list[v0].append(edge)

        if v1 not in self.adj_edges_list:
            self.adj_edges_list[v1] = []

        self.adj_edges_list[v1].append(edge)

        if self.use_matrix:
            self.adj_matrix[v1][v0] = True
            self.adj_matrix[v0][v1] = True

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

    def construct_graph_from_list(self, list_of_edges, with_data=True):
        tmp_vertices = []
        for edge in list_of_edges:
            for i in range(2):
                if edge.vertices[i] not in tmp_vertices:
                    self.num_of_vertices += 1
                    self.adj_list[edge.vertices[i]] = []
                    self.new_adj_list[edge.vertices[i]] = []
                    tmp_vertices.append(edge.vertices[i])
            if with_data:
                self.edges_list.append(Data(UndirectedEdge(edge.vertices[0], edge.vertices[1])))
            else:
                self.edges_list.append(UndirectedEdge(edge.vertices[0], edge.vertices[1]))

            self.adj_list[edge.vertices[0]].append(edge.vertices[1])
            self.adj_list[edge.vertices[1]].append(edge.vertices[0])

            if self.use_matrix:
                self.adj_matrix[edge.vertices[0]][edge.vertices[1]] = True
                self.adj_matrix[edge.vertices[1]][edge.vertices[0]] = True

    def construct_graph_from_adj_list(self, adj_list: dict):
        for i in adj_list.keys():
            self.num_of_vertices += 1
            for j in adj_list[i]:
                if j < i:
                    continue
                edge = Data(UndirectedEdge(i, j))
                self.edges_list.append(edge)
                if i not in self.adj_edges_list:
                    self.adj_edges_list[i] = []
                self.adj_edges_list[i].append(edge)
                if j not in self.adj_edges_list:
                    self.adj_edges_list[j] = []
                self.adj_edges_list[j].append(edge)
                if self.use_matrix:
                    self.adj_matrix[j][i] = True
                    self.adj_matrix[i][j] = True

            self.new_adj_list[i] = []
        self.adj_list = adj_list.copy()

    # FIXME: implement more effectively
    def get_edges_lower(self, number):
        edges = []
        for edge in self.adj_edges_list[number]:
            if edge.data.get_lower() == number:
                edges.append(edge)
        return edges

    def get_edges_higher(self, number):
        edges = []
        for edge in self.adj_edges_list[number]:
            if edge.data.get_higher() == number:
                edges.append(edge)
        return edges

    def has_edge(self, v, k):
        if self.use_matrix:
            return self.__has_edge_fast(v, k)
        else:
            try:
                return k in self.adj_list[v]
            except KeyError:
                return False

    def __has_edge_fast(self, v, k):
        return self.adj_matrix[v][k]

    def get_num_of_vertices(self):
        return self.num_of_vertices

    def find_cycle(self):
        cycle = []
        marks = {i: 0 for i in self.adj_list.keys()}

        def dfs_cycle(p, v):
            nonlocal cycle, marks
            marks[v] = 1
            for k in self.adj_list[v]:
                if k == p:
                    continue
                if not marks[k]:
                    cycle.append((v, k))
                    if dfs_cycle(v, k):
                        return True
                    else:
                        cycle.pop()
                if marks[k] == 1:
                    cycle.append((v, k))
                    tmp_c = []
                    for i, n in enumerate(cycle):
                        if n[0] == k:
                            tmp_c.extend(cycle[i:])
                            cycle = tmp_c[:]
                            return True
                    return True
            marks[v] = 2
            return False

        if not dfs_cycle(-1, list(self.adj_list.keys())[0]):
            return []
        else:
            result = []
            for e in cycle:
                result.append(e[0])
            return result

    def get_adjacent_vertices(self, vertex):
        return self.adj_list[vertex]

    def get_segments(self, cycle, neighbors_tmp):
        segments = []

        neighbors = neighbors_tmp.copy()

        tmp_cycle = []
        for i in cycle.keys():
            if cycle[i]:
                tmp_cycle.append(i)

        # cycle_list = cycle.copy()

        # cycle_list = {i: False for i in self.adj_list.keys()}
        # for i in cycle:
        #    cycle_list[i] = True

        single_edge_segments = []

        # already_processed = {i: False for i in self.adj_list.keys()}
        # Search for single-edge segments
        for v in tmp_cycle:
            for n in self.adj_list[v]:
                #if already_processed[n]:
                #    continue
                if not neighbors[v][n] and cycle[n]:
                    seg = Graph()
                    # seg.set_matrix_use(len(self.adj_list.keys()))
                    e = Edge(v, n)
                    seg.construct_graph_from_list([e], False)
                    single_edge_segments.append(e)
                    segments.append(seg)
                    # already_processed[v] = True
                    neighbors[v][n] = True
                    neighbors[n][v] = True

        def __dfs_segment_recursive(vertex, dfs_marks, graph_cycle, segment, parent):
            nonlocal single_edge_segments

            dfs_marks[vertex] = True
            for adj in self.adj_list[vertex]:

                # Should not go through cycle
                if adj == parent or neighbors[vertex][adj]:
                    continue

                if not segment.has_edge(vertex, adj):
                    segment.add_edge(Edge(vertex, adj))

                if not dfs_marks[adj]:
                    # If reached cycle, add edge, but do not go to recursion
                    if graph_cycle[adj]:
                        # segment.add_edge(Edge(adj, vertex))
                        dfs_marks[adj] = True
                        continue

                    __dfs_segment_recursive(adj, dfs_marks, graph_cycle, segment, vertex)

        def dfs_segment(start, dfs_marks, graph_cycle, segment, parent):
            __dfs_segment_recursive(start, dfs_marks, graph_cycle, segment, parent)

        # Search for segments with multiple edges
        marks = {i: False for i in self.adj_list.keys()}
        for v in tmp_cycle:
            if not marks[v]:
                for adj in self.adj_list[v]:
                    if not neighbors[v][adj]:
                        marks[v] = True
                        seg = Graph()
                        # seg.set_matrix_use(len(self.adj_list.keys()))
                        seg.add_edge(Edge(v, adj))
                        __dfs_segment_recursive(adj, marks, cycle, seg, v)
                        # Ignore segments with 2 vertices since they already been added
                        if seg.get_num_of_vertices() > 2:
                            segments.append(seg)

        return segments

    def dfs_chain(self, marks, partial_embedding, chain, v):
        marks[v] = True
        chain.append(v)
        count_marks = 0
        for adj_v in self.adj_list[v]:
            if not marks[adj_v]:
                if not partial_embedding[adj_v]:
                #if adj_v not in partial_embedding:
                    if self.dfs_chain(marks, partial_embedding, chain, adj_v):
                        count_marks += 1
                        if count_marks == len(self.adj_list[v]):
                            #for t in self.adj_list[v]:
                            #    if t in partial_embedding:
                            #        return
                            chain.pop()
                            return True
                        continue
                else:
                    chain.append(adj_v)
                return
            else:
                count_marks += 1
                if count_marks == len(self.adj_list[v]):
                    for t in self.adj_list[v]:
                        if partial_embedding[t]:
                        #if t in partial_embedding:
                            chain.append(t)
                            return
                    chain.pop()
                    return True

    def get_chain(self, partial_embedding):
        chain = []
        marks = {i: False for i in self.adj_list.keys()}
        for v in self.adj_list.keys():
            if partial_embedding[v]:
            #if v in partial_embedding:
                if len(self.adj_list[v]) != 0:
                    self.dfs_chain(marks, partial_embedding, chain, v)
                    break

        #print(chain)
        return chain

    # TODO: understand
    def face_has_segment(self, face, segment, partial_embedding):
        face_dict = {i: False for i in self.adj_list.keys()}
        for i in face:
            face_dict[i] = True

        # for edge in self.edges_list:
        for edge in segment.edges_list:
        #for v in self.adj_list.keys():
        #    for k in self.adj_list[v]:
            v = edge.vertices[0]
            k = edge.vertices[1]
            #if segment.__has_edge_fast(v, k):
            if partial_embedding[v] and not face_dict[v] or \
               partial_embedding[k] and not face_dict[k]:
                return False

                #if v in partial_embedding and not v not in face or \
                #   k in partial_embedding and not k not in face:
                #        return False
        return True

    def __get_random_edge(self):
        idx = random.randint(0, len(self.edges_list) - 1)
        random_edge = self.edges_list[idx]
        return random_edge.data.get_lower(), random_edge.data.get_higher()

    def compute_st_numbering(self):
        count = 1
        numbering = {i: 0 for i in self.adj_list.keys()}
        low_number = {i: 0 for i in self.adj_list.keys()}
        dfs_number = {i: 0 for i in self.adj_list.keys()}
        dfs_incoming_edge = {i: None for i in self.adj_list.keys()}
        follow_low_path = {i: None for i in self.adj_list.keys()}
        marked_nodes = {i: False for i in self.adj_list.keys()}
        list_edges = []
        for i in self.adj_list.keys():
            for j in self.adj_list[i]:
                if i >= j:
                    continue
                list_edges.append(Edge(i, j))
        marked_edges = {i: False for i in list_edges}

        if self.st_edge is None:
            self.st_edge = self.__get_random_edge()
        print("S-T EDGE: " + str(self.st_edge))
        assert self.st_edge[1] in self.adj_list[self.st_edge[0]] and \
               self.st_edge[0] in self.adj_list[self.st_edge[1]]

        s = self.st_edge[0]
        t = self.st_edge[1]

        dfs_number[t] = count
        low_number[t] = count
        count += 1

        # Computes dfs number and low number for a graph
        def __st_search(vertex):
            nonlocal count
            dfs_number[vertex] = count
            low_number[vertex] = count
            count += 1

            for p in self.adj_list[vertex]:
                # Vertex has not been visited
                if dfs_number[p] == 0:
                    dfs_incoming_edge[p] = Edge(vertex, p)
                    __st_search(p)
                    if low_number[vertex] > low_number[p]:
                        low_number[vertex] = low_number[p]
                        follow_low_path[vertex] = Edge(vertex, p)

                elif low_number[vertex] > dfs_number[p]:
                    low_number[vertex] = dfs_number[p]
                    follow_low_path[vertex] = Edge(vertex, p)

        __st_search(s)

        # Why is needed???
        if low_number[t] < low_number[s]:
            low_number[t] = low_number[s]

        node_stack = [t, s]
        count = 1
        marked_edges[Edge(s, t)] = True
        marked_nodes[s] = True
        marked_nodes[t] = True

        v = node_stack.pop()
        adj = 0
        path = []

        def __st_path(vertex):
            global adj

            for p in self.adj_list[vertex]:
                e = Edge(p, vertex)
                if marked_edges[e]:
                    continue
                marked_edges[e] = True
                if dfs_incoming_edge[p] == e:
                    path.append(vertex)
                    w = p
                    while not marked_nodes[w]:
                        e = follow_low_path[w]
                        path.append(w)
                        marked_nodes[w] = True
                        marked_edges[e] = True
                        w = e.get_opposite(w)

                    return True
                elif dfs_number[vertex] < dfs_number[p]:
                    path.append(vertex)
                    w = p
                    while not marked_nodes[w]:
                        e = dfs_incoming_edge[w]
                        path.append(w)
                        marked_nodes[w] = True
                        marked_edges[e] = True
                        w = e.get_opposite(w)
                    return True
                else:
                    continue

            return False

        while v != t:
            if not __st_path(v):
                numbering[v] = count
                count += 1
                adj = 0
            else:
                while len(path) > 0:
                    node_stack.append(path.pop())
            v = node_stack.pop()
        numbering[t] = count
        self.__update_numbering(numbering)

    def __update_numbering(self, numbering):
        self.vertex_mapping = dict(zip(numbering.keys(), numbering.values()))
        new_adj_list = {}
        for v in self.adj_list:
            new_adj_list[numbering[v]] = []
            for k in self.adj_list[v]:
                new_adj_list[numbering[v]].append(numbering[k])

        self.old_adj_list = self.adj_list
        self.adj_list = new_adj_list

        self.new_adj_list = {}
        for v in self.adj_list.keys():
            self.new_adj_list[v] = []

        for edge in self.edges_list:
            edge.data.vertices = (numbering[edge.data.vertices[0]], numbering[edge.data.vertices[1]])
        new_edge_adj_list = {}
        for id in self.adj_edges_list.keys():
            new_edge_adj_list[numbering[id]] = self.adj_edges_list[id]

        self.adj_edges_list = new_edge_adj_list

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
