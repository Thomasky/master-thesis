import numpy as np


def get_sharp_triangle(angle):
    """ Returns the vertices of a triangle with a sharp angle and radius 1.
            angle must be between 0 and pi/2.
    """
    assert angle > 0 and angle < np.pi / 2

    # Initialize result
    result = np.zeros((3, 2))

    # vertices are (0,1); (sin(a), -cos(a)); (-sin(a), -cos(a))
    result[0] = (0, 1)
    result[1] = (-np.sin(angle), -np.cos(angle))
    result[2] = (np.sin(angle), -np.cos(angle))

    return result


def get_regular_polygon(number_sides):
    """ Returns the vertices of a regular polygon of radius 1.
            The first vertex is (0,1) and the subsequent vertices are generated in counterclockwise direction
    """
    # Number of sides must be at least 3
    assert number_sides >= 3

    # Calculate angle between vertices
    angle = 2 * np.pi / number_sides

    # Create array of vertices
    return np.array([(-np.sin(n * angle), np.cos(n * angle)) for n in range(0, number_sides)])


def rotate_polygon(polygon, angle, x, y):
    """ Rotates a 2D polygon around (x,y)

    """

    # Translate to origin
    polygon = polygon - np.array([x, y])

    # Create rotation matrix
    transform = np.array([[np.cos(angle), -np.sin(angle)],
                          [np.sin(angle), np.cos(angle)]])

    # Rotate and Translate back to (x,y)
    return np.dot(polygon, transform) + np.array([x, y])


def get_possible_scale(search_polygon, inclusions, base_polygon, x, y, angle):
    """ Calculates the maximum possible scale given x, y and angle.
            Leaves .01% margin.

    """
    s = 1000

    # Calculate vertices of the base polygon
    base_verts = rotate_polygon(base_polygon, angle, 0, 0)
    base_verts = np.vstack((base_verts, base_verts[0, :]))

    # edges = search_verts - np.roll(base_verts, 1, 0)
    # For all edges of base ploygon:
    for i in range(np.shape(base_polygon)[0]):
        edge = base_verts[i] - base_verts[i + 1]
        norm = np.sqrt(np.dot(edge.T, edge))
        edge = edge / norm

        # Get distance from (x,y) to edge -> d
        d = np.cross(edge, np.array([x, y]) - base_verts[i])

        # Calculate max scale to every search polygon point and inclusion point
        for incl in np.vstack((search_polygon, inclusions)):
            l = np.cross(edge, incl - base_verts[i])

            # Check that (x,y) and point are on opposite sides of edge or |d| >
            # |l|
            if (not np.sign(d) == np.sign(l)) or (np.abs(d) <= np.abs(l)):
                s = np.min([s, np.abs((d - l) / d)])

    return s


def get_polygon_from_config(base_polygon, config):
    """ Returns the polygon corresponding to a configuration using the base
            polygon.

    """
    # config must be an array of size 4
    assert len(config) == 4

    # transform the base polygon according to configuration
    return config[3] * rotate_polygon(base_polygon, config[2], 0, 0) + np.array([config[0], config[1]])


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


def includes_point(polygon, point):
    """	Checks if a 2D polygon contains a point.
            Based on algorithm in [O'Rourke (1998) - Computational Geometry in C, p. 244]
            The polygon must be convex (!)
    """
    r_cross = 0  # number of right edge crossings
    l_cross = 0  # number of left edge crossings
    r_strad = 0  # boolean false
    l_strad = 0  # blooean false

    n = np.size(polygon, axis=0)

    # Loop over all edges
    for i in range(0, n):
        # check if point is a vertex
        if (polygon[i, :] == point).all():
            return True
        i1 = (i + n - 1) % n

        # check if edge straddles horizontal ray
        r_strad = (polygon[i, 1] > point[1]) != (polygon[i1, 1] > point[1])
        l_strad = (polygon[i, 1] < point[1]) != (polygon[i1, 1] < point[1])

        if r_strad or l_strad:
            # Intersection of edge and ray
            x = polygon[i1, 0] + (point[1] - polygon[i1, 1]) * (
                polygon[i, 0] - polygon[i1, 0]) / (polygon[i, 1] - polygon[i1, 1])

        if r_strad and x > point[0]:
            r_cross = r_cross + 1
        if l_strad and x < point[0]:
            l_cross = l_cross + 1

    if (r_cross & 1) != (l_cross & 1):
        # Point is on the edge
        return True

    return r_cross & 1
