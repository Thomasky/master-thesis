#!/usr/bin/env python

import numpy as np
import plots
import polygon
import search

# Create random seed
np.random.seed(48951)

search_polygon = np.array([(0, 0), (1, 0), (1, 1), (0, 1)])

inclusions = np.vstack(
    (np.random.uniform(0, 1, 3), np.random.uniform(0, 1, 3))).T

base_polygon = polygon.get_regular_polygon(4)
# base_polygon = polygon.get_sharp_triangle(np.pi / 18)

nb_experiments = 1
max_it = 2 ** 15
scores = np.zeros((nb_experiments, np.log2(max_it).astype('int') + 1))
for i in range(0, nb_experiments):
    [config, scores[i, :]] = search.montecarlo(
        search_polygon, inclusions, base_polygon, max_it)
poly = polygon.get_polygon_from_config(base_polygon, config[:, -1])

plots.plot_polygons([poly, search_polygon], inclusions)
plots.plot_scores(scores)

# qmc.search_nied_peart(square, 10**3)
