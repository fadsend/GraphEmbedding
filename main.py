from graph import Graph
from linear_algorithm import planar_testing


def main():
    edges = [(1, 2),
             (1, 3),
             (2, 3),
             (2, 4),
             (3, 4)]

    graph = Graph()
    graph.construct_graph(edges)
    result = planar_testing(graph)

    if result:
        print("Graph is planar")
    else:
        print("Graph is none planar")

if __name__ == "__main__":
    main()
