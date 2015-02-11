import lattice as lat
import numpy as np
import polygon


def search_nied_peart(base_polygon, num_points):
    """ Searches for the largest polygon in a unit square using
            Niederreiter & Peart's method (1986)

    """

    # define configurations
    configs = lattice.get_lattice_points(4, num_points)

    # Define cube
    epsilon = 0.49
    cube_centre = [0.5, 0.5, 0.5, 0.5]
    cube_edge = 0.5

    # Create config
    a = np.array([cube_centre, ] * num_points).T
    e = np.ones((4, num_points))

    g = a + epsilon * (2 * configs - e)

    res = polygon.evaluate_points(base_polygon, g)

    print np.shape(res)


def lattice(search_polygon, inclusions, base_polygon, max_N):
    """ Searches for the largest polygon in a unit square using the lattice rules

    """
    # Create random seed
    # np.random.seed(48951)

    N = 1
    i_max = np.log2(max_N).astype(int)

    # Initialize config
    best_config = np.zeros((4, np.log2(max_N) + 1))
    best_scores = np.zeros(np.log2(max_N) + 1)

    # iterates for set number of loops
    for i in range(0, i_max + 1):

        # set configurations, but only x,y and angle
        configs = lat.get_lattice_points(3, N)
        x = configs[0]
        y = configs[1]
        angle = configs[2]

        # for every combo of x, y, angle: calculate max scale
        scale = [polygon.get_possible_scale(
            search_polygon, inclusions, base_polygon, x[j], y[j], angle[j]) for j in range(0, N)]

        # set configurations
        configs = np.array([x, y, angle, scale])

        # calculate scores using objective function
        scores = polygon.evaluate_points(search_polygon, base_polygon, configs)

        argmax = np.argmax(scores)

        best_config[:, i] = configs[:, argmax]
        best_scores[i] = scores[argmax]

        N = 2 * N

    return best_config, best_scores


def find_best_config(search_polygon, base_polygon, configs):
    """ Finds the config with the highest score and returns it along with its score.

    """
    # calculate scores using objective function
    # scores = polygon.evaluate_points(search_polygon, base_polygon, configs)
    scores = configs[3]

    # find the argmax of the scores
    argmax = np.argmax(scores)

    # return the best config and its score
    return configs[:, argmax], scores[argmax]


def montecarlo(search_polygon, inclusions, base_polygon, max_N):
    """ Searches for the largest polygon in a unit square using the montecarlo method

    """
    N = 1
    i_max = np.log2(max_N).astype(int)

    # Initialize results
    best_config = np.zeros((4, i_max + 1))
    best_scores = np.zeros(i_max + 1)

    # iterate for set number of loops
    for i in range(0, i_max + 1):

        # find a random configuration
        x = np.random.uniform(0, 1, N)
        y = np.random.uniform(0, 1, N)
        angle = np.random.uniform(0, 2 * np.pi, N)

        # for every combo of x, y, angle: calculate max scale
        scale = [polygon.get_possible_scale(
            search_polygon, inclusions, base_polygon, x[j], y[j], angle[j]) for j in range(0, N)]

        # set configurations
        configs = np.array([x, y, angle, scale])

        # find best config
        best = find_best_config(search_polygon, base_polygon, configs)

        # Remember best config and best score
        best_config[:, i] = best[0]
        best_scores[i] = best[1]

        # update N
        N = 2 * N

    return best_config, best_scores
