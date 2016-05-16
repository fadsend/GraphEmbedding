from graph import Graph


def gamma_algorithm(graph):
    cycle = graph.find_cycle()
    print(cycle)

    faces = [cycle]
    outer_face = cycle[:]
    faces.append(outer_face)

    while True:
        segments = graph.get_segments(cycle)
        print(segments)
        break


    raise NotImplementedError()