from graph import Graph
from linear_algorithm import upward_embed, embed
from gamma_algorithm import gamma_algorithm
from random_graph_generation import generate_random_graph, show_graph, Point
from graph import Edge
import time
import sys


def main():
    planar_6 = {
        1: [2, 3, 5, 6],
        2: [1, 3, 4, 5],
        3: [1, 2, 4, 6],
        4: [2, 3, 5, 6],
        5: [1, 2, 4, 6],
        6: [1, 3, 4, 5]
    }

    planar_10 = {
        1: [2, 3, 4, 5],
        2: [1, 3, 7],
        3: [1, 2, 4, 6, 7],
        4: [1, 3, 5, 6],
        5: [1, 4, 9],
        6: [3, 4, 9, 8, 7],
        7: [2, 3, 6, 10],
        8: [6, 10],
        9: [5, 6, 10],
        10: [7, 8, 9]
    }

    planar_20 = {
        1: [2, 3, 5, 6],
        2: [1, 5, 8, 4],
        3: [1, 7],
        4: [2, 10],
        5: [1, 2, 9, 12, 6],
        6: [1, 14, 15, 5, 7],
        7: [3, 15, 6],
        8: [2, 10, 11, 12],
        9: [5, 13, 14],
        10: [4, 8, 16],
        11: [8, 20],
        12: [5, 8, 13, 17],
        13: [9, 12, 14, 17],
        14: [9, 6, 13, 18],
        15: [6, 7, 18],
        16: [10, 20],
        17: [12, 13, 20, 19],
        18: [14, 15, 19],
        19: [18, 20, 17],
        20: [16, 17, 19, 11],
    }

    graphs_lists = [
        # planar_6,
        # planar_10,
        # planar_20,
        # random_25,
        # random_50,
        # random_100
    ]

    for i in [100]:
        tmp_graph = Graph()
        #tmp_graph.construct_graph_from_adj_list({0: [4, 5, 2, 9], 1: [4, 5, 3, 7, 8, 9], 2: [3, 6, 0, 9], 3: [2, 6, 1, 7, 9], 4: [0, 5, 1, 9], 5: [4, 0, 1, 8], 6: [2, 3, 7], 7: [3, 1, 6, 8], 8: [1, 5, 7], 9: [1, 3, 2, 0, 4]})
        #points_t = [(96, 53), (-82, 78), (61, -98), (-71, -89), (85, 99), (124, 190), (-21, -146), (-156,-103), (-177,147), (27,60)]
        tmp_graph.construct_graph_from_adj_list({0: [1, 2, 3], 1: [0, 2, 8, 5], 2: [0, 1, 3, 7, 6, 8], 3: [0, 2, 7, 9], 4: [5, 8, 6, 9], 5: [1, 8, 4], 6: [2, 7, 8, 4, 9], 7: [3, 2, 6, 9], 8: [2, 1, 6, 5, 4], 9: [6, 4, 7, 3]})
        points_t = [(-183,-5), (-112,-157), (-171,11), (-184,172), (123,3), (-9,-156), (-53,68), (-122,81), (-15,-130), (-90,183)]
        points = []
        for i, p in enumerate(points_t):
            points.append(Point(p[0], p[1], i))
        #tmp_graph, points = generate_random_graph(i, return_points=True)
        #show_graph(tmp_graph, points, True)
        graphs_lists.append(tmp_graph.adj_list)
        print("GRAPH" + str(tmp_graph.adj_list))
        print("POINTS " + str([str(i) for i in points]))

    count_edges = []
    count = 0

    for gr in graphs_lists:
        count_edges.append(0)
        for v in gr.keys():
            count_edges[count] += len(gr[v])
        count_edges[count] /= 2
        count += 1

    num_of_vertices = [len(t.keys()) for t in graphs_lists]


    test_result = {}

    run = {
        "linear": True,
        "gamma": True,
        "retries": 1
    }

    results = {
        "linear": [],
        "gamma": []
    }

    if run["linear"]:
        run_count = run["retries"]

        for i in range(run_count):
            time_list = []
            for g in graphs_lists:
                print("##############Iteration#############")
                graph = Graph()
                graph.construct_graph_from_adj_list(g)
                print("Running linear algorithm with PQ-tree")
                start_time = time.time()
                result = upward_embed(graph)
                if result:
                    print("Graph is planar")
                    embedded_graph = embed(graph)
                    embedded_graph.print_adj()
                else:
                    print("Graph is none planar")
                end_time = time.time()
                time_list.append(end_time - start_time)
            print("##############End####################")
            test_result[i] = time_list[:]

        print("##########Result############")
        final_results = [0] * len(graphs_lists)
        for j in range(len(graphs_lists)):
            for i in range(run_count):
                final_results[j] += test_result[i][j]
        for i in range(len(graphs_lists)):
            final_results[i] /= run_count

        results["linear"] = final_results

    if run["gamma"]:
        run_count = run["retries"]

        for i in range(run_count):
            time_list = []
            for g in graphs_lists:
                graph = Graph()
                graph.construct_graph_from_adj_list(g)
                print("#######################################################")
                print("###############Running gamma algorithm#################")
                print("#######################################################")
                start_time = time.time()
                result, faces, outer = gamma_algorithm(graph)
                if result:
                    print("Graph is planar")
                    print(faces)
                    print(outer)
                else:
                    print("Graph is none planar")
                end_time = time.time()
                time_list.append(end_time - start_time)
            test_result[i] = time_list[:]

        print("##########GAMMA Result############")
        final_results = [0] * len(graphs_lists)
        for j in range(len(graphs_lists)):
            for i in range(run_count):
                final_results[j] += test_result[i][j]
        for i in range(len(graphs_lists)):
            final_results[i] /= run_count

        results["gamma"] = final_results

    print("##########RESULTS##############")
    print("NUM OF VERTICES: " + str(num_of_vertices))
    print("NUM OF EDGES: " + str(count_edges))
    print("LINEAR: " + str(results["linear"]))
    print("GAMMA: " + str(results["gamma"]))
    print("###############################")
    return 0


if __name__ == "__main__":
    sys.exit(main())
