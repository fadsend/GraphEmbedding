from graph import Graph
from linear_algorithm import upward_embed, embed
from gamma_algorithm import gamma_algorithm
import sys


def main():
    edges_full = {
        1: [2, 3, 4, 5],
        2: [1, 3, 4, 5],
        3: [1, 2, 4, 5],
        4: [1, 2, 3, 5],
        5: [1, 2, 3, 4]
    }

    edges_planar5 = {
        1: [2, 3, 5],
        2: [1, 3, 4, 5],
        3: [1, 2, 4, 5],
        4: [2, 3, 5],
        5: [4, 2, 3, 1]
    }

    edges_planar6 = {
        1: [2, 3, 5, 6],
        2: [1, 3, 4, 5],
        3: [1, 2, 4, 6],
        4: [2, 3, 5, 6],
        5: [1, 2, 4, 6],
        6: [1, 3, 4, 5]
    }

    edges_non_planar6 = {
        1: [2, 3, 5, 6],
        2: [1, 3, 4, 5, 6],
        3: [1, 2, 4, 6],
        4: [2, 3, 5, 6],
        5: [1, 2, 4, 6],
        6: [1, 2, 3, 4, 5]
    }

    graph = Graph()
    # graph.construct_graph_from_list(data2)
    # graph.generate_random_graph(10, 0.5)
    graph.construct_graph_from_adj_list(edges_planar6)
    print("Running linear algorithm with PQ-tree")
    result = upward_embed(graph)
    if result:
        print("Graph is planar")
    else:
        print("Graph is none planar")
        return 1
    embedded_graph = embed(graph)
    embedded_graph.print_adj()

    test_graph1 = {
        1: [6, 3, 5, 2],
        2: [1, 3, 5],
        3: [1, 2, 4, 7],
        4: [3, 7, 8, 5, 6],
        5: [2, 1, 6, 4],
        6: [1, 5, 4, 7],
        7: [6, 3, 4],
        8: [4, 7],
    }

    test_graph2 = {

    }

    graph = Graph()
    graph.construct_graph_from_adj_list(test_graph1)
    # graph.construct_graph_from_adj_list(edges_planar6)
    print("#######################################################")
    print("###############Running gamma algorithm#################")
    print("#######################################################")
    result = gamma_algorithm(graph)
    if result:
        print("Graph is planar")
    else:
        print("Graph is none planar")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
