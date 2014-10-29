#!/usr/bin/env python

import numpy as np

import polygon
import montecarlo, qmc

def main():
	# base = polygon.get_regular_polygon(5)
	base = polygon.get_sharp_triangle(np.pi/18)
	
	max_it = 2 ** 17
	[config, scores] = montecarlo.search_montecarlo(base, max_it)
	poly = polygon.get_polygon_from_config(base, config[:, -1])
	
	var = np.zeros(np.log2(max_it).astype(int))
	for i in range(1,np.log2(max_it).astype(int)):
		var[i] = np.var(scores[0:i])/i
	
	x1 = [2 ** i for i in range(0, np.log2(max_it).astype(int))]
	conv = np.vstack((x1, var))
	polygon.plot_polygon(poly, conv)
	
	#qmc.search_nied_peart(square, 10**3)
	

if __name__ == '__main__':
	main()
