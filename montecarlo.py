import numpy as np
import polygon

def search_montecarlo(base_polygon, max_it):
	""" Searches for the largest polygon in a unit square using the montecarlo method

	"""
	# Create random seed
	np.random.seed(48951)

	# Initialize config
	best_config = np.zeros((4, 1))
	best_scores = np.zeros((1, max_it))
	best_score = 0

	# iterates for set number of loops
	for i in range(0, max_it):

		# find a random configuration
		x = np.random.uniform(0, 1)
		y = np.random.uniform(0, 1)
		angle = np.random.uniform(0, 2 * np.pi)
		# scale = np.random.uniform(0, get_possible_scale(base_polygon, x, y, angle))
		scale = polygon.get_possible_scale(base_polygon, x, y, angle)

		# set configuration
		config = np.matrix([x, y, angle, scale]).T
		
		# calculate score using objective function
		score = polygon.evaluate_points(base_polygon, config)

		# adjust max if necessary
		if score[4, 0] > best_score:
			best_config = config
			best_score = score[4, 0]
		
		best_scores[0, i] = best_score

	return best_config, best_scores
