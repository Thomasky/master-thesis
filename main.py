#!/usr/bin/env python

import montecarlo
import numpy as np
import polygon
import qmc


def main():
    search_polygon = np.array([(0, 0), (1, 0), (1, 1), (0, 1)])

    base_polygon = polygon.get_regular_polygon(4)
    # base_polygon = polygon.get_sharp_triangle(np.pi / 18)

    nb_experiments = 8
    max_it = 2 ** 15
    scores = np.zeros((nb_experiments, np.log2(max_it).astype('int') + 1))
    for i in range(0, nb_experiments):
        [config, scores[i, :]] = montecarlo.search_montecarlo(
            search_polygon, base_polygon, max_it)
    poly = polygon.get_polygon_from_config(base_polygon, config[:, -1])

    polygon.plot_polygon(poly, scores)

    # qmc.search_nied_peart(square, 10**3)


if __name__ == '__main__':
    main()
