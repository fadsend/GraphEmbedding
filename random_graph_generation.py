import random
from graph import Edge, Graph
import pylab
import matplotlib.lines as lines


# TODO: understand how it works
class Point(object):

    def __init__(self, x, y, ident=-1):
        self.x = x
        self.y = y
        self.id = ident

    def __str__(self):
        return str(self.id) + "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.id)


class Triangle(object):

    def __init__(self, points):
        assert len(points) == 3
        self.points = points

    def has_vertex(self, vertex):
        return self.points[0] == vertex or \
               self.points[1] == vertex or \
               self.points[2] == vertex

    def circum_circle_contains(self, vertex):
        ab = self.points[0].x ** 2 + self.points[0].y ** 2
        cd = self.points[1].x ** 2 + self.points[1].y ** 2
        ef = self.points[2].x ** 2 + self.points[2].y ** 2

        circum_x = (ab * (self.points[2].y - self.points[1].y) + cd * (self.points[0].y - self.points[2].y) +
                    ef * (self.points[1].y - self.points[0].y)) / \
                    (self.points[0].x * (self.points[2].y - self.points[1].y) + self.points[1].x *
                    (self.points[0].y - self.points[2].y) + self.points[2].x * (self.points[1].y - self.points[0].y)) / 2

        circum_y = (ab * (self.points[2].x - self.points[1].x) + cd * (self.points[0].x - self.points[2].x) +
                    ef * (self.points[1].x - self.points[0].x)) / \
                    (self.points[0].y * (self.points[2].x - self.points[1].x) + self.points[1].y *
                    (self.points[0].x - self.points[2].x) + self.points[2].y * (self.points[1].x - self.points[0].x)) / 2

        circum_radius = (((self.points[0].x - circum_x) ** 2) + ((self.points[0].y - circum_y) ** 2)) ** 0.5

        dist = ((vertex.x - circum_x) ** 2 + (vertex.y - circum_y) ** 2) ** 0.5
        return dist <= circum_radius

    def has_edge(self, edge: Edge) -> bool:
        v = edge.vertices
        assert v[0] != v[1]

        return v[0] in self.points and v[1] in self.points

    def get_edges(self):
        return [Edge(self.points[0], self.points[1]),
                Edge(self.points[1], self.points[2]),
                Edge(self.points[2], self.points[0])]

    def __str__(self):
        return "<" + "".join([str(i) for i in self.points]) + ">"


def generate_random_points(num, low_range, high_range):
    points = []
    for i in range(num):
        points.append(Point(random.randint(low_range, high_range),
                            random.randint(low_range, high_range), i))
    # TODO: check for repeats
    return points


def __get_max_min_points(points):

    assert len(points) > 0

    x_min = points[0].x
    x_max = points[0].x
    y_min = points[0].y
    y_max = points[0].y

    for i in range(len(points)):
        x_min = min(points[i].x, x_min)
        x_max = max(points[i].x, x_max)

        y_min = min(points[i].y, y_min)
        y_max = max(points[i].y, y_max)

    return [x_min, x_max, y_min, y_max]


def __get_triangle_around_points(points):
    x_min, x_max, y_min, y_max = __get_max_min_points(points)

    # x_median = (x_min + x_max) / 2
    # y_coord = y_max * 10
    #
    # # Fount top point of super triangle
    # top = Point(x_median, y_coord, -1)
    #
    # m1 = (y_coord - y_max) / (x_median - x_min)
    # x2 = (y_min - y_coord + m1 * x_median) / m1
    # # Found leftmost point of triangle
    # left = Point(x2, y_min, -1)
    #
    # m2 = (y_coord - y_max) / (x_median - x_max)
    # x3 = (y_min - y_coord + m2 * x_median) / m2
    #
    # right = Point(x3, y_min, -1)
    #
    # return Triangle((top, left, right))

    dx = x_max - x_min
    dy = y_max - y_min
    delta_max = max(dx, dy)
    x_mid = (x_min + x_max) / 2
    y_mid = (y_min + y_max) / 2

    p1 = Point(x_mid - 20 * delta_max, y_mid - delta_max)
    p2 = Point(x_mid, y_mid + 20 * delta_max)
    p3 = Point(x_mid + 20 * delta_max, y_mid - delta_max)
    return Triangle((p1, p2, p3))


def __check_if_edge_in_triangles(edge, triangles) -> bool:
    count = 0
    for triangle in triangles:
        if triangle.has_edge(edge):
            count += 1
    return count > 1


def __get_graph_from_triangulation(triangulation):
    g = Graph()
    included_edges = []
    for triangle in triangulation:
        for edge in triangle.get_edges():
            if edge not in included_edges:
                included_edges.append(edge)
                g.add_edge(Edge(edge.vertices[0].id, edge.vertices[1].id))
    return g


def generate_random_graph(num, return_points=False):
    assert num > 0
    points = generate_random_points(num, -num * 20, num * 20)

    # points = [Point(p[0],p[1], i) for i, p in enumerate([(15,32), (58,17), (42,-31), (-96,-90), (75,-95)])]
    print([str(i) for i in points])

    # Initialize empty list of triangles
    triangulation = []

    # Create super triangle(which contains all points inside) and add it to the list
    super_triangle = __get_triangle_around_points(points)
    triangulation.append(super_triangle)

    for point in points:
        bad_triangles = []
        polygon = []

        for triangle in triangulation:
            if triangle.circum_circle_contains(point):
                bad_triangles.append(triangle)
                for edge in triangle.get_edges():
                    polygon.append(edge)

        for triangle in bad_triangles:
            triangulation.remove(triangle)

        bad_edges = []

        #processed = []
        # polygon = list(set(polygon))
        for i in range(len(polygon)):
            for j in range(len(polygon)):
                if i == j:
                    continue
                if polygon[i] == polygon[j]:
                    #if (j, i) in processed:
                    #    continue
                    #processed.append((i, j))
                    bad_edges.append(polygon[i])
                    bad_edges.append(polygon[j])

        for edge in bad_edges:
            if edge in polygon:
                polygon.remove(edge)

        for edge in polygon:
            triangulation.append(Triangle((edge.vertices[0], edge.vertices[1], point)))

    for triangle in triangulation[:]:
        for p in super_triangle.points:
            if triangle.has_vertex(p):
                triangulation.remove(triangle)
                break

    g = __get_graph_from_triangulation(triangulation)
    if return_points:
        return g, points
    else:
        return g

def show_graph(g, p, static_graph=False):
    ax = pylab.subplot()
    bx = pylab.subplot()

    x = list(map(lambda w: w.x, p))
    y = list(map(lambda w: w.y, p))
    num = list(range(len(x)))

    tmp_lines = []
    for edge in g.get_edges():
        if static_graph:
            e1 = edge.data.vertices[0]
            e2 = edge.data.vertices[1]
        else:
            e1 = edge.vertices[0]
            e2 = edge.vertices[1]
        tmp_lines.append([(x[e1], y[e1]), (x[e2], y[e2])])

    for i, n in enumerate(num):
        bx.annotate(n, (x[i], y[i]))

    converted_lines = []
    for line in tmp_lines:
        tmp = list(zip(*line))
        print(line, tmp)
        ax.add_line(lines.Line2D(tmp[0], tmp[1], linewidth=1, color='b'))

    pylab.scatter(x, y, s=5, marker='o', c='b')
    pylab.plot()

    pylab.show()

    print(g)


if __name__ == "__main__":
    g, p = generate_random_graph(100, return_points=True)
    show_graph(g, p)