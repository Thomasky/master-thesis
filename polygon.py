from matplotlib.path import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


def create_sharp_triangle(angle):
    """ Returns the vertices of a triangle with a sharp angle and radius 1.
            angle must be between 0 and pi/2.
    """
    assert angle > 0 and angle < np.pi / 2

    # Initialize result
    centre = np.array([0, 0])
    radius = 1
    vertices = np.zeros((3, 2))

    # vertex consists of radius and angle
    vertices[0] = (radius, 0)
    vertices[1] = (radius, np.pi - angle)
    vertices[2] = (radius, np.pi + angle)

    return centre, vertices


def create_regular_polygon(number_sides):
    """ Returns the centre and vertices of a regular polygon of radius 1.
        The first vertex is (r=1, theta=0) and the subsequent vertices are generated in 
        counterclockwise direction.
    """
    # Number of sides must be at least 3
    assert number_sides >= 3

    # Initialize result
    centre = np.array([0, 0])
    radius = 1

    # Calculate angle between vertices
    angle = 2 * np.pi / number_sides

    # create vertices
    vertices = np.array([[radius, n * angle] for n in range(0, number_sides)])

    # return centre and vertices
    return centre, vertices


def translate(polygon, point):
    """ Translates a 2D polygon by a vector 'point'

    """

    # return new centre and same vertices
    return polygon[0] + point, polygon[1]


def rotate(polygon, angle):
    """ Rotates a 2D polygon around its own centre

    """

    nb_vertices = np.shape(polygon[1])[0]

    # vertices only need to add the rotation angle to their angles
    temp = np.hstack((np.zeros((nb_vertices, 1)), np.ones((nb_vertices, 1))))
    vertices = polygon[1] + angle * temp

    # Rotate and Translate back to (x,y)
    return polygon[0], vertices


def scale(polygon, scale):
    """ Scales a 2D polygon around its own centre

    """

    nb_vertices = np.shape(polygon[1])[0]

    # vertices only need to multiply their radii with scale
    temp = np.ones((nb_vertices, 1)) * np.array([scale, 1]).reshape((1, 2))
    vertices = np.multiply(polygon[1], temp)

    # Rotate and Translate back to (x,y)
    return polygon[0], vertices


def get_possible_scale(search_polygon, base_polygon, x, y, angle):
    """ Calculates the maximum possible scale given x, y and angle.
            Leaves .01% margin.

    """
    # Calculate vertices of the base polygon
    verts = rotate(base_polygon, angle)
    assert (verts != 0).all()

    scales = verts
    # for every vertex
    for s in scales:
        if s[0] < 0:
            s[0] = -x / s[0]
        else:
            s[0] = (1 - x) / s[0]

        if s[1] < 0:
            s[1] = -y / s[1]
        else:
            s[1] = (1 - y) / s[1]

    return np.min(scales) * 0.9999


def get_polygon_from_config(base_polygon, config):
    """ Returns the polygon corresponding to a configuration using the base
            polygon.

    """
    # config must be an array of size 4
    assert len(config) == 4

    # first rotate, then scale vertices, then translate
    return translate(scale(rotate(base_polygon, config[2]), config[3]), config[0:2])


def evaluate_points(search_polygon, base_poly, configs):
    """ Evaluates the objective function for the given points.
            Returns a row containing all configuration scores.
            The score for an invalid config is 0.
    """
    # configs must have 4 rows: x, y, angle, scale
    assert np.shape(configs)[0] == 4

    # Initialize results as empty row
    result = np.zeros(np.shape(configs)[1])

    # Iterate over each configuration
    for i in range(0, np.shape(configs)[1]):
        config = configs[:, i]

        # transform the base polygon according to configuration
        verts = get_polygon_from_config(base_poly, config)

        # If configuration is valid, calculate size squared and add it to
        # results
        if includes_polygon(search_polygon, verts):
            # Add scale**2 to result
            result[i] = config[3]
        else:
            # Add result for invalid config
            result[i] = 0

    return result


def includes_polygon(search_polygon, polygon):
    """	Checks if a 2D search area includes a polygon entirely.
            The search area must be convex (!)
    """
    assert np.size(search_polygon, axis=1) == 2
    assert np.size(polygon, axis=1) == 2

    for p in polygon:
        if not includes_point(search_polygon, p):
            return False
    return True


# def includes_point(polygon, point):
#     """	Checks if a 2D polygon contains a point.
#             Based on algorithm in [O'Rourke (1998) - Computational Geometry in C, p. 244]
#             The polygon must be convex (!)
#     """
# r_cross = 0  # number of right edge crossings
# l_cross = 0  # number of left edge crossings
# r_strad = 0  # boolean false
# l_strad = 0  # blooean false
#
#     n = np.size(polygon, axis=0)
#
# Loop over all edges
#     for i in range(0, n):
# check if point is a vertex
#         if (polygon[i, :] == point).all():
#             return True
#         i1 = (i + n - 1) % n
#
# check if edge straddles horizontal ray
#         r_strad = (polygon[i, 1] > point[1]) != (polygon[i1, 1] > point[1])
#         l_strad = (polygon[i, 1] < point[1]) != (polygon[i1, 1] < point[1])
#
#         if r_strad or l_strad:
# Intersection of edge and ray
#             x = polygon[i1, 0] + (point[1] - polygon[i1, 1]) * (
#                 polygon[i, 0] - polygon[i1, 0]) / (polygon[i, 1] - polygon[i1, 1])
#
#         if r_strad and x > point[0]:
#             r_cross = r_cross + 1
#         if l_strad and x < point[0]:
#             l_cross = l_cross + 1
#
#     if (r_cross & 1) != (l_cross & 1):
# Point is on the edge
#         return True
#
#     return r_cross & 1


def includes_point(polygon, point):
    """ Checks if polygon includes point in log(n) time

    """
    centre = polygon[0]

    # Get angle between centre of polygon and point
    angle = np.arctan((centre[1] - point[1]) / (centre[0] - point[0]))

    # Perform a binary search on the angles to find the important edge
    vertices = binary_angle_search(angle, polygon[1])

    # Determine if point lies further away from centre than edge in question

    return angle


def binary_angle_search(angle, vertices):
    """ Performs a binary search on an array of angles and returns the radii
        and angles of the two encapsulating vertices.

    """


def plot_polygon(verts, scores):
    """ Plots a polygon with center (x,y)

    """
    # Add first vertex at the end again
    verts = np.vstack((verts, verts[0, :]))

    # Configure polygon
    codes = [Path.LINETO] * (verts.shape[0] - 1)
    codes[0] = Path.MOVETO
    codes.append(Path.CLOSEPOLY)

    path = Path(verts, codes)

    var = np.zeros(np.size(scores, axis=1))
    for i in range(0, np.size(scores, axis=1)):
        var[i] = np.var(scores[:, i])

    x1 = [2 ** i for i in range(0, np.size(scores, axis=1))]
    conv = np.vstack((x1, var))

    # fig = plt.figure()
    ax = plt.subplot(211)
    patch = patches.PathPatch(path, facecolor='orange', lw=2)
    ax.add_patch(patch)
    plt.title('Score: ' + scores[-1, -1].astype('str'))
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal', adjustable='box')

#     plt.subplot(212)
#     plt.loglog(conv[0], conv[1])
#     plt.title('Convergence')

    plt.show()
