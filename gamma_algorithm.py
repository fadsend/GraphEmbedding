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

        # Segments are found, now start embedding procedure
        count_of_appropriate_faces = [0 for _ in range(len(segments))]
        face_to_embed = [None for _ in range(len(segments))]

        min_segment_id = -1
        min_faces_count = 0
        for idx in range(len(segments)):
            for face in faces:
                if graph.embedded_on_face(face, segments[idx]):
                    count_of_appropriate_faces[idx] += 1
                    face_to_embed[idx] = face

                if min_faces_count > count_of_appropriate_faces[idx]:
                    min_segment_id = idx
                    min_faces_count = count_of_appropriate_faces[idx]
        break

    raise NotImplementedError()