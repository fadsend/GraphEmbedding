from graph import Graph
from LinearAlgorithm import planarTesting


def main():
    edges = [(1, 2),
             (1, 3),
             (2, 3),
             (2, 4),
             (3, 4)]

    graph = Graph()
    graph.constructGraph(edges)
    result = planarTesting(graph)

    if result:
        print("Graph is planar")
    else:
        print("Graph is none planar")

if __name__ == "__main__":
    main()
