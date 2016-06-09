from graph import Graph
from linear_algorithm import upward_embed, embed
from gamma_algorithm import gamma_algorithm
from random_graph_generation import generate_random_graph, show_graph, Point, get_random_non_planar_graph
from graph import Edge
import time
import sys
import os
from sys import setrecursionlimit
import matplotlib.pyplot as plt


def main():
    # Set max number of recursion frames
    setrecursionlimit(50000)
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

    graphs_lists = []

    # TODO: change
    tmp_stdout = sys.stdout
    f = open(os.devnull, "w")
    sys.stdout = f

    points_list = {}

    vertices = [10 * 2 ** i for i in range(9)]
    NON_PLANAR = False
    # TODO: change
    for idx, i in enumerate(vertices):
        # TODO: create testsuite for this graphs
        tmp_graph = Graph()
        points = []

        #tmp_graph.construct_graph_from_adj_list({0: [2, 4, 5], 1: [3, 4, 5], 2: [0, 4, 5], 3: [1, 4], 4: [0, 2, 1, 3, 5], 5: [2, 0, 4, 1]})
        #points_t = [(-114,-81), (35,97), (-104,-59), (-34,100), (-102,-42), (28,-106)]

        #tmp_graph.construct_graph_from_adj_list({0: [2, 5, 1, 6], 1: [0, 6, 3], 2: [0, 5, 6], 3: [1, 6, 4], 4: [3, 6], 5: [0, 2], 6: [0, 1, 3, 2, 4]})
        #points_t = [(5,68), (-83,34), (65,-21), (-90,1),(-110,-121),(77,58), (-3,-63)]

        # Check later
        #tmp_graph.construct_graph_from_adj_list({0: [1, 3, 2, 4, 6], 1: [0, 3, 5, 4], 2: [0, 4, 5, 6], 3: [0, 1, 5, 6], 4: [0, 2, 5, 1], 5: [3, 1, 4, 2, 6], 6: [2, 0, 3, 5]})
        #points_t = [(-107,104), (-127,-130), (-22,-27), (-113,-54), (77,-124), (-54,-111), (-35,-34)]

        #tmp_graph.construct_graph_from_adj_list({0: [1, 5, 7, 6, 4, 8, 9], 1: [0, 5, 3, 7], 2: [6, 7, 4, 8], 3: [1, 5, 9], 4: [2, 8, 0, 9], 5: [0, 1, 3, 9], 6: [2, 7, 0, 8], 7: [6, 2, 1, 0], 8: [4, 2, 6, 0], 9: [4, 0, 5, 3]})
        #points_t = [(-38,-31), (-44,128), (200,-73), (-128,126), (179,-111), (-96,58),(149,28), (123,85), (159,-1), (-115,-180)]


        #tmp_graph.construct_graph_from_adj_list({0: [2, 3, 8, 6], 1: [4, 6, 9, 7], 2: [0, 3, 4, 5, 6], 3: [0, 2, 6, 8], 4: [2, 5, 6, 1, 9, 7], 5: [4, 2], 6: [3, 2, 4, 1, 0, 8], 7: [1, 9, 4], 8: [0, 3, 6], 9: [1, 4, 7]})
        #points_t = [(187,95),(-94,-139),(-11,183),(106,69),(-170,94),(-162,133),(-3,-82),(-190,-200),(110,61),(-149,-146)]

        # TODO: run and fix
        #tmp_graph.construct_graph_from_adj_list({0: [2, 5, 3, 9, 4], 1: [2, 7, 6, 8], 2: [0, 5, 1, 7, 8, 9], 3: [0, 5], 4: [6, 8, 0, 9], 5: [0, 2, 3], 6: [1, 7, 8, 4], 7: [2, 1, 6], 8: [1, 2, 6, 4, 9], 9: [2, 0, 8, 4]})
        #points_t = [(-103,-156), (8,79), (-130,35), (-158,-134),(197,-177),(-189,-40),(198,-3),(88,172),(70,-32),(45,-125)]

        #tmp_graph.construct_graph_from_adj_list({0: [1, 4, 5, 6, 8, 9], 1: [0, 4, 3, 7, 8], 2: [3, 5, 7, 4, 9], 3: [2, 5, 1, 7], 4: [0, 1, 7, 2, 9], 5: [2, 3, 0, 6, 9], 6: [0, 5, 8], 7: [1, 3, 4, 2], 8: [1, 0, 6], 9: [4, 2, 0, 5]})
        #points_t = [(18,-41), (-177,178),(17,-103),(-110,-196),(2,-59),(65,-119),(95,121),(-100,-112),(-141,194),(20,-102)]
        # Graph.st_edge = (0, 5)
        #for i, p in enumerate(points_t):
        #    points.append(Point(p[0], p[1], i))
        tmp_graph, points = generate_random_graph(i, return_points=True)
        #tmp_graph = get_random_non_planar_graph(i)
        # show_graph(tmp_graph, points, True)
        graphs_lists.append(tmp_graph.adj_list)
        print("GRAPH" + str(tmp_graph.adj_list))
        print("POINTS " + str([str(i) for i in points]))
        points_list[idx] = str([str(i) for i in points])

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
        # TODO: change
        "retries": 10
    }

    results = {
        "linear": [],
        "gamma": []
    }

    result_str = {
        "linear": "",
        "gamma": ""
    }

    if run["linear"]:
        run_count = run["retries"]

        for i in range(run_count):
            time_list = []
            for index, g in enumerate(graphs_lists):
                print("##############Iteration#############")
                graph = Graph()
                graph.construct_graph_from_adj_list(g)
                print("Running linear algorithm with PQ-tree")
                start_time = time.time()
                result = upward_embed(graph)
                if result:
                    print("Graph is planar")
                    embedded_graph = embed(graph)
                    print("###RESULT linear")
                    embedded_graph.print_adj()
                    result_str["linear"] = "PLANAR"
                else:
                    print("Graph is none planar")
                    result_str["linear"] = "NOT PLANAR"
                    if not NON_PLANAR:
                        assert False
                end_time = time.time()
                time_list.append(end_time - start_time)
            print("##############End####################")
            test_result[i] = time_list[:]

        # print("##########Result############")
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
            for gamma_index, g in enumerate(graphs_lists):
                graph = Graph()
                graph.construct_graph_from_adj_list(g)
                print("#######################################################")
                print("###############Running gamma algorithm#################")
                print("#######################################################")
                start_time = time.time()
                result, faces, outer = gamma_algorithm(graph)
                if result:
                    print("Graph is planar")
                    print("###RESULT gamma")
                    print(faces)
                    print(outer)
                    result_str["gamma"] = "PLANAR"
                else:
                    print("Graph is none planar")
                    result_str["gamma"] = "NOT PLANAR"
                    if not NON_PLANAR:
                        assert False
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

    sys.stdout = tmp_stdout

    print("##########RESULTS##############")
    print("NUM OF VERTICES: " + str(num_of_vertices))
    print("NUM OF EDGES: " + str(count_edges))
    print("RESULT LINEAR: " + result_str["linear"])
    print("RESULT GAMMA: " + result_str["gamma"])
    print("LINEAR: " + str(results["linear"]))
    print("GAMMA: " + str(results["gamma"]))
    print("###############################")
    if len(results["linear"]) > 1:
        plt.plot(num_of_vertices, results["linear"], "r")
        plt.plot(num_of_vertices, results["gamma"], "b")
        plt.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
