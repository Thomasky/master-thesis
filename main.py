#!/usr/bin/env python

import numpy as np
import polygon
import search

search_polygon = np.array([(0, 0), (1, 0), (1, 1), (0, 1)])

base_polygon = polygon.create_regular_polygon(4)
# base_polygon = polygon.create_sharp_triangle(np.pi / 300)

nb_experiments = 1
max_it = 2 ** 10
scores = np.zeros((nb_experiments, np.log2(max_it).astype('int') + 1))
for i in range(0, nb_experiments):
    [config, scores[i, :]] = search.montecarlo(
        search_polygon, base_polygon, max_it)
#     [config, scores[i, :]] = search.search_lattice(
#         search_polygon, base_polygon, max_it)
poly = polygon.get_polygon_from_config(base_polygon, config[:, -1])

polygon.plot_polygon(poly, scores)

# search.search_nied_peart(square, 10**3)
