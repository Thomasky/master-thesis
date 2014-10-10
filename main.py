#!/usr/bin/env python

import numpy as np

import lattice
import polygon
import montecarlo


def search_nied_peart(polygon, num_points):
	""" Searches for the largest polygon in a unit square using
		Niederreiter & Peart's method (1986)
	
	"""
	
	# define evaluation points
	x = lattice.get_lattice_points(4, num_points)
	# x[2,:] = x[2,:]*2*np.pi
		
	epsilon = 0.5
	cube_centre = [0.5, 0.5, 0.5, 0.5]
	cube_edge = 0.5
	
	a = np.array([cube_centre, ] * num_points).T
	e = np.ones((4, num_points))
	
	g = a + epsilon * (2 * x - e)
	
	polygon.evaluate_points(g)
	
	print g


def main():
	square = polygon.get_regular_polygon(3)
	max_it = 10000
	[config, scores] = montecarlo.search_montecarlo(square, max_it)
	poly = polygon.get_polygon_from_config(square, config)
	var = [np.var(scores[0:i]) for i in scores]
	conv = np.vstack((np.arange(0,max_it).reshape(1,max_it),var))
	polygon.plot_polygon(poly, conv)
	
	# search_nied_peart(square, 10**(-2))
	

if __name__ == '__main__':
	main()
