#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import itertools
import lattice


def search_nied_peart(polygon, max_dispersion):
	""" Searches for the largest polygon in a unit square using
		Niederreiter & Peart's method (1986)
	
	"""
	
	#define evaluation points
	x = get_lattice_points(3, max_dispersion)
	for i in x:
		print(i)
	

def search_montecarlo(polygon, nb_iterations):
	""" Searches for the largest polygon in a unit square using the montecarlo method

	"""

	max_polygon = polygon
	max_score = 0
	
	errors = np.zeros((2, nb_iterations - 1))

	#iterates for set number of loops
	for i in range(1, nb_iterations):

		#find a fitting configuration
		x = np.random.uniform(0, 1)
		y = np.random.uniform(0, 1)
		angle = np.random.uniform(0,2*np.pi)
		#scale = np.random.uniform(0, get_possible_scale(polygon, x, y, angle))
		scale = get_possible_scale(polygon, x, y, angle)

		#transform the base polygon according to configuration
		verts = scale * rotate_polygon(polygon, angle, 0, 0) + np.array([x,y])
		
		#calculate score using objective function
		score = get_score(x, y, angle, scale)
		errors[0,i-1] = i
		errors[1,i-1] = 0.7071 - max_score #0.5528 - max_score

		#make checks and adjust max if necessary
		if score > max_score and (verts < 1).all() and (verts > 0).all():
				max_polygon = verts
				max_score = score

	return max_polygon, errors


def get_possible_scale(polygon, x, y, angle):
	""" Calculates the maximum possible scale given x, y and angle
	
	"""
	
	verts = rotate_polygon(polygon, angle, 0, 0)
	assert (verts != 0).all()
	
	scales = verts
	for s in scales:
		if s[0] < x:
			s[0] = -x/s[0]
		else:
			s[0] = (1-x)/s[0]
			
		if s[1] < y:
			s[1] = -y/s[1]
		else:
			s[1] = (1-y)/s[1]
	
	return np.min(scales)


def get_score(x, y, angle, scale):
	""" Calculates score using objective function
	
	"""
	
	return scale


def define_polygon(number_sides):
	""" Returns an array with the coordinates of a regular polygon with radius 1

	"""
	assert number_sides >= 3
	
	angle = 2*np.pi/number_sides
	result = np.array( [(np.cos(n*angle), np.sin(n*angle)) for n in range(0, number_sides + 1)] )

	return result


def rotate_polygon(polygon, angle, x, y):
	""" Rotates a 2D polygon around (x,y)

	"""
	polygon = polygon - np.array([x,y])
	transform = np.array([[np.cos(angle), -np.sin(angle)],
						  [np.sin(angle), np.cos(angle)]])
	return np.dot(polygon, transform) + np.array([x,y])


def plot_polygon(verts, errors):
	""" Plots a polygon (square) with center (x,y)
	
	"""
	
	#Configure polygon
	codes =  [Path.LINETO] * (verts.shape[0] - 1)
	codes[0] = Path.MOVETO
	codes.append(Path.CLOSEPOLY)

	path = Path(verts, codes)

	#fig = plt.figure()
	ax = plt.subplot(211)
	patch = patches.PathPatch(path, facecolor='orange', lw=2)
	ax.add_patch(patch)
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.gca().set_aspect('equal', adjustable='box')
	
	plt.subplot(212)
	plt.loglog(errors[0], errors[1])
	plt.title('Convergence')
	
	plt.show()


def main():
	square = define_polygon(4)
	[max_square, errors] = search_montecarlo(square, 100000)
	plot_polygon(max_square, errors)
	
	#search_nied_peart(square, 10**(-2))
	

if __name__ == '__main__':
	main()
