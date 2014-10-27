#!/usr/bin/env python

import numpy as np

import polygon
import montecarlo, qmc

def main():
	# base = polygon.get_regular_polygon(4)
	base = polygon.get_sharp_triangle(np.pi/18)
	
	max_it = 100000
	[config, scores] = montecarlo.search_montecarlo(base, max_it)
	poly = polygon.get_polygon_from_config(base, config)
	
	var = np.zeros((1,max_it))
	for i in np.arange(0,max_it):
		var[0,i] = np.var(scores[0,0:i])
		
	conv = np.vstack((np.arange(0,max_it).reshape(1,max_it),var))
	polygon.plot_polygon(poly, conv)
	
	#qmc.search_nied_peart(square, 10**3)
	

if __name__ == '__main__':
	main()
