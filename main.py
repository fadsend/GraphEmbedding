from graph import Graph
from linear_algorithm import planar_testing


def main():
    edges = {
        1: [2, 3, 4, 5],
        2: [1, 3, 4, 5],
        3: [1, 2, 4, 5],
        4: [1, 2, 3, 5],
        5: [1, 2, 3, 4]
    }

    edges1 = {
        1: [2, 3, 5],
        2: [1, 3, 4, 5],
        3: [1, 2, 4, 5],
        4: [2, 3, 5],
        5: [1, 2, 3, 4]
    }

    graph = Graph()
    # graph.construct_graph_from_list(data2)
    # graph.generate_random_graph(10, 0.5)
    graph.construct_graph_from_adj_list(edges1)
    result = planar_testing(graph)

    if result:
        print("Graph is planar")
    else:
        print("Graph is none planar")

if __name__ == "__main__":
    main()
