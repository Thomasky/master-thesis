import lattice
import polygon
import numpy as np

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
	
	#Create config
	a = np.array([cube_centre, ] * num_points).T
	e = np.ones((4, num_points))
	
	g = a + epsilon * (2 * configs - e)
	
	res = polygon.evaluate_points(base_polygon, g)
	
	print np.shape(res)