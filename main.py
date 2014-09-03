#!/usr/bin/env python
#Thomas

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


def rotate_polygon(polygon, angle, x, y):
	""" Rotates a 2D polygon around (x,y)

	"""
	polygon = polygon - np.array([x,y])
	transform = np.array([[np.cos(angle), -np.sin(angle)],
						  [np.sin(angle), np.cos(angle)]])
	return np.dot(polygon, transform) + np.array([x,y])


def search_polygon(polygon, nb_iterations):
	""" Searches for the largest polygon in a unit square

	"""

	max_polygon = polygon
	max_scale = 0

	#iterates for set number of loops
	for i in range(1, nb_iterations):

		#find a fitting configuration
		x = np.random.uniform(0, 1)
		y = np.random.uniform(0, 1)
		angle = np.random.uniform(0,2*np.pi)
		scale = np.random.uniform(0, 0.2)

		#transform the base polygon according to configuration
		verts = scale * rotate_polygon(polygon, angle, 0, 0) + np.array([x,y])

		#make checks and adjust max if necessary
		if (verts > 0).all() and (verts < 1).all() and scale > max_scale:
				max_polygon = verts
				max_scale = scale

	print verts, (verts > 0).all(), (verts < 1).all()
	print scale, max_scale   
	return max_polygon


def plot_polygon(verts):
	""" Plots a polygon (square) with center (x,y)
	
	"""

	codes = [	Path.MOVETO,
				Path.LINETO,
				Path.LINETO,
				Path.LINETO,
				Path.CLOSEPOLY,
				]

	path = Path(verts, codes)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	patch = patches.PathPatch(path, facecolor='orange', lw=2)
	ax.add_patch(patch)
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.gca().set_aspect('equal', adjustable='box')
	plt.show()


def define_polygon(number_sides):
	""" Returns an array with the coordinates of a regular polygon with radius 1

	"""
	
	result = []
	angle = 2*np.pi/number_sides

	#iterate over number of sides
	for n in range(0,number_sides + 1):
		result.append((np.cos(n*angle), np.sin(n*angle)))

	return result


def main():
	square = define_polygon(4)
	max_square = search_polygon(square, 1000)
	plot_polygon(max_square)

if __name__ == '__main__':
	main()
