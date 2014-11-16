import numpy as np
import polygon


def search_montecarlo(search_polygon, base_polygon, max_N):
    """ Searches for the largest polygon in a unit square using the montecarlo method

    """
    # Create random seed
    # np.random.seed(48951)

    # Initialize config
    best_config = np.zeros((4, np.log2(max_N) + 1))
    best_scores = np.zeros(np.log2(max_N) + 1)

    N = 1
    # iterates for set number of loops
    while N <= max_N:

        # find a random configuration
        x = np.random.uniform(0, 1, N)
        y = np.random.uniform(0, 1, N)
        angle = np.random.uniform(0, 2 * np.pi, N)

        # for every combo of x, y, angle: calculate max scale
        scale = [polygon.get_possible_scale(
            search_polygon, base_polygon, x[i], y[i], angle[i]) for i in range(0, N)]

        # set configurations
        configs = np.array([x, y, angle, scale])

        # calculate scores using objective function
        scores = polygon.evaluate_points(search_polygon, base_polygon, configs)

        argmax = np.argmax(scores)

        best_config[:, np.log2(N)] = configs[:, argmax]
        best_scores[np.log2(N)] = scores[argmax]

        N = 2 * N

    return best_config, best_scores
