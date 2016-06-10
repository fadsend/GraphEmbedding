from graph import Graph


def gamma_algorithm(graph):

    cycle = graph.find_cycle()
    print(cycle)

    faces = [cycle]
    outer_face = cycle[:]
    faces.append(outer_face)

    partial_embedding = {i: False for i in graph.adj_list.keys()}
    for c in cycle:
        partial_embedding[c] = True
    # partial_embedding = cycle[:]

    neighbors = [
        [False for _ in range(len(graph.adj_list) + 1)]
               for _ in range(len(graph.adj_list) + 1)
    ]

    for i in range(len(cycle) - 1):
        neighbors[cycle[i]][cycle[i + 1]] = True
        neighbors[cycle[i + 1]][cycle[i]] = True

    neighbors[cycle[0]][cycle[-1]] = True
    neighbors[cycle[-1]][cycle[0]] = True

    while True:
        segments = graph.get_segments(partial_embedding, neighbors)

        if len(segments) == 0:
            return True, faces, outer_face

        # Segments are found, now start embedding procedure
        count_of_appropriate_faces = [0 for _ in range(len(segments))]
        faces_to_embed = [None for _ in range(len(segments))]

        # Find segment which could be embedded in minimum number of faces
        min_segment_id = -1
        min_faces_count = 999999999

        for idx in range(len(segments)):
            for face in faces:
                if graph.face_has_segment(face, segments[idx], partial_embedding):
                    count_of_appropriate_faces[idx] += 1
                    faces_to_embed[idx] = face

        for idx in range(len(segments)):
            if min_faces_count > count_of_appropriate_faces[idx]:
                min_segment_id = idx
                min_faces_count = count_of_appropriate_faces[idx]
        # If there are no face to which segment could be embedded, graph is non planar
        if min_faces_count < 1:
            return False, None, None

        # Choose segment and face
        segment_to_embed = segments[min_segment_id]
        face_to_embed = faces_to_embed[min_segment_id]

        # Embed chain of segment to face
        chain = segment_to_embed.get_chain(partial_embedding)
        for v in chain:
            partial_embedding[v] = True
            #if v not in partial_embedding:
            #    partial_embedding.append(v)
        for i in range(len(chain) - 1):
            neighbors[chain[i]][chain[i + 1]] = True
            neighbors[chain[i + 1]][chain[i]] = True

        # Split face by its segment
        assert face_to_embed is not None
        start_v = -1
        end_v = -1
        # noinspection PyTypeChecker
        for idx in range(len(face_to_embed)):
            if face_to_embed[idx] == chain[0]:
                start_v = idx
            if face_to_embed[idx] == chain[-1]:
                end_v = idx

        #if end_v == -1:
        #    print("1r")
        assert start_v != -1 and end_v != -1

        face_size = len(face_to_embed)

        face1 = []
        face2 = []
        reverse_chain = list(reversed(chain))
        # Split face here
        if face_to_embed != outer_face:
            if start_v < end_v:
                # First part of split
                face1.extend(chain)
                i = (end_v + 1) % face_size
                while i != start_v:
                    face1.append(face_to_embed[i])
                    i = (i + 1) % face_size

                # Second part of split
                face2.extend(reverse_chain)
                i = (start_v + 1) % face_size
                while i != end_v:
                    face2.append(face_to_embed[i])
                    i = (i + 1) % face_size
            else:
                                # First part of split
                face2.extend(chain)
                i = (end_v + 1) % face_size
                while i != start_v:
                    face2.append(face_to_embed[i])
                    i = (i + 1) % face_size

                # Second part of split
                face1.extend(reverse_chain)
                i = (start_v + 1) % face_size
                while i != end_v:
                    face1.append(face_to_embed[i])
                    i = (i + 1) % face_size

            faces.remove(face_to_embed)
            faces.append(face1)
            faces.append(face2)
        else:
            new_outer_face = []
            if start_v < end_v:
                # First part of split
                new_outer_face.extend(chain)
                i = (end_v + 1) % face_size
                while i != start_v:
                    new_outer_face.append(face_to_embed[i])
                    i = (i + 1) % face_size

                # Second part of split
                face2.extend(reverse_chain)
                i = (start_v + 1) % face_size
                while i != end_v:
                    face2.append(face_to_embed[i])
                    i = (i + 1) % face_size
            else:
                # First part of split
                face2.extend(chain)
                i = (end_v + 1) % face_size
                while i != start_v:
                    face2.append(face_to_embed[i])
                    i = (i + 1) % face_size

                # Second part of split
                new_outer_face.extend(reverse_chain)
                i = (start_v + 1) % face_size
                while i != end_v:
                    new_outer_face.append(face_to_embed[i])
                    i = (i + 1) % face_size

            faces.remove(outer_face)
            faces.append(new_outer_face)
            faces.append(face2)
            outer_face = new_outer_face

    return True, faces, outer_face
