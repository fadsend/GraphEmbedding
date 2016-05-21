from pqtree import PQtree
from pqtree import reduce_tree, ReductionFailed
from pqnode import Type, DirectionIndicator
import copy


def upward_embed(graph):
    graph.compute_st_numbering()
    universe = graph.get_edges_lower(1)
    n = graph.get_num_of_vertices()
    tree = PQtree(universe)
    for iteration in range(2, n + 1):
        subset = graph.get_edges_higher(iteration)
        # if len(subset) == 0:
        #    continue
        try:
            tree = reduce_tree(tree, subset)
        except ReductionFailed:
            return False
        tmp_list = DirectionIndicator.list_of_instances

        print([str(i) for i in tmp_list])

        subset1 = graph.get_edges_lower(iteration)

        # Save pertinent root before its re-written on the next iteration
        pertinent_root = tree.get_pertinent_root(subset)
        assert pertinent_root is not None

        print("---------------END of reduction --------------")
        print(tree)
        if pertinent_root.node_type == Type.Q_NODE:
            print("Replacing Q-node")
            adj_list = tree.replace_full_children(pertinent_root, PQtree(subset1, True).get_root(), iteration)
        else:
            print("Replacing P-node")
            adj_list = tree.replace_node(pertinent_root, PQtree(subset1, True).get_root())

        print(tree)
        tmp123 = []
        for tmp in adj_list:
            if type(tmp) == str:
                tmp123.append(tmp)
            else:
                tmp123.append(tmp.data.data.vertices[0])
        for vertex in tmp123:
            graph.new_adj_list[iteration].append(vertex)

    print(graph.new_adj_list)
    #graph.new_adj_list[6] = [3, 4]
    #graph.new_adj_list[9] = [6, 5]
    graph.new_adj_list = correct_direction(graph.new_adj_list, n)
    print(graph.new_adj_list)
    return True


# TODO: re-write
def correct_direction(adj_list, n):
    for i in range(n, 1, -1):
        for j in range(len(adj_list[i])):
            if type(adj_list[i][j]) == str:
                if adj_list[i][j][0] == "|":
                    should_revers = False
                elif adj_list[i][j][0] == "<":
                    should_revers = True
                else:
                    assert False

                tmp_id = int(adj_list[i][j][1:-1])
                # should_revers = False
                if should_revers:
                    if len(adj_list[tmp_id]) % 2 == 1:
                        p = len(adj_list[tmp_id]) // 2
                        if type(adj_list[tmp_id][p]) == str:
                            if adj_list[tmp_id][p][0] == "|":
                                adj_list[tmp_id][p] = "< " + adj_list[tmp_id][p][1] + "|"
                            elif adj_list[tmp_id][p][0] == "<":
                                adj_list[tmp_id][p] = "|" + adj_list[tmp_id][p][1] + ">"
                            else:
                                assert False

                    for k in range(len(adj_list[tmp_id]) // 2):
                        idx1 = k
                        idx2 = len(adj_list[tmp_id]) - 1 - k
                        adj_list[tmp_id][idx1], adj_list[tmp_id][idx2] = adj_list[tmp_id][idx2], adj_list[tmp_id][idx1]
                        for p in [k, len(adj_list[tmp_id]) - 1 - k]:
                            if type(adj_list[tmp_id][p]) == str:
                                if adj_list[tmp_id][p][0] == "|":
                                    adj_list[tmp_id][p] = "< " + adj_list[tmp_id][p][1] + "|"
                                elif adj_list[tmp_id][p][0] == "<":
                                    adj_list[tmp_id][p] = "|" + adj_list[tmp_id][p][1] + ">"
                                else:
                                    assert False
                adj_list[i][j] = -1
    for tmp in adj_list.keys():
        while -1 in adj_list[tmp]:
            adj_list[tmp].remove(-1)
    return adj_list


# Assumed that upward_embed has been called for graph
def embed(graph):
    assert len(graph.new_adj_list.keys()) > 0
    marks = {i: False for i in graph.new_adj_list.keys()}
    # Use deepcopy since dict has an lists as its values
    graph.adj_list = copy.deepcopy(graph.new_adj_list)
    dfs(list(graph.new_adj_list.keys())[-1], graph, marks)
    return graph


def dfs(vertex, graph, marks=None):
    marks[vertex] = True
    for adj_v in graph.new_adj_list[vertex]:
        graph.adj_list[adj_v].insert(0, vertex)
        if not marks[adj_v]:
            dfs(adj_v, graph, marks)



