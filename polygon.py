import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


def get_sharp_triangle(angle):
	""" Returns the vertices of a triangle with a sharp angle and radius 1.
		angle must be between 0 and pi/2.
	"""
	assert angle > 0 and angle < np.pi/2
	
	# Initialize result
	result = np.zeros((3,2))
	
	# vertices are (0,1); (sin(a), -cos(a)); (-sin(a), -cos(a)) 
	result[0] = (0,1)
	result[1] = (np.sin(angle), -np.cos(angle))
	result[2] = (-np.sin(angle), -np.cos(angle))
	
	return result


def get_regular_polygon(number_sides):
	""" Returns the vertices of a regular polygon of radius 1.

	"""
	# Number of sides must be at least 3
	assert number_sides >= 3
	
	# Calculate angle between vertices
	angle = 2 * np.pi / number_sides
	
	# Create array of vertices
	return np.array([(np.cos(n * angle), np.sin(n * angle)) for n in range(0, number_sides)])


def rotate_polygon(polygon, angle, x, y):
	""" Rotates a 2D polygon around (x,y)

	"""
	
	# Translate to origin
	polygon = polygon - np.array([x, y])
	
	# Create rotation matrix
	transform = np.array([[np.cos(angle), -np.sin(angle)],
				  [np.sin(angle), np.cos(angle)]])
	
	# Rotate and Translate back to (x,y)			  
	return np.dot(polygon, transform) + np.array([x, y])
	
	
def get_possible_scale(polygon, x, y, angle):
	""" Calculates the maximum possible scale given x, y and angle.
		Leaves 1% margin.
	
	"""
	#Calculate vertices of the base polygon
	verts = rotate_polygon(polygon, angle, 0, 0)
	assert (verts != 0).all()
	
	scales = verts
	#for every vertex
	for s in scales:
		if s[0] < 0:
			s[0] = -x / s[0]
		else:
			s[0] = (1 - x) / s[0]
			
		if s[1] < 0:
			s[1] = -y / s[1]
		else:
			s[1] = (1 - y) / s[1]
	
	return np.min(scales)*0.99
	
	
def get_polygon_from_config(base_polygon, config):
	""" Returns the polygon corresponding to a configuration using the base
		polygon.
	
	"""
	# config must be an array of size 4
	assert len(config) == 4
	
	# transform the base polygon according to configuration
	return config[3, 0] * rotate_polygon(base_polygon, config[2, 0], 0, 0) + np.array([config[0, 0], config[1, 0]])

	
def evaluate_points(base_poly, configs):
	""" Evaluates the objective function for the given points.
		Returns a matrix containing all valid configurations and their evaluation.
	"""
	# configs must have 4 rows: x, y, angle, scale
	assert np.shape(configs)[0] == 4
	
	# Initialize results as empty matrix
	result = np.zeros((5, 1))
	
	# Iterate over each configuration
	for i in range(0, np.shape(configs)[1]):
		config = configs[:, i]
		
		# transform the base polygon according to configuration
		verts = get_polygon_from_config(base_poly, config)
			
		# If configuration is valid, calculate size squared and add it to results
		if (verts <= 1).all() and (verts >= 0).all():
			# Add result under current config
			res = np.vstack((config, np.matrix([config[3, 0] ** 2])))
			
			# Add to other results
			result = np.hstack((result, res))
		
	return result[:, 1:]
	

def plot_polygon(verts, errors):
	""" Plots a polygon with center (x,y)
	
	"""
	# Add first vertex at the end again
	verts = np.vstack((verts, verts[0,:]))
	
	
	# Configure polygon
	codes = [Path.LINETO] * (verts.shape[0] - 1)
	codes[0] = Path.MOVETO
	codes.append(Path.CLOSEPOLY)

	path = Path(verts, codes)

	# fig = plt.figure()
	ax = plt.subplot(211)
	patch = patches.PathPatch(path, facecolor='orange', lw=2)
	ax.add_patch(patch)
	plt.xlim(0, 1)
	plt.ylim(0, 1)
	plt.gca().set_aspect('equal', adjustable='box')
	
	plt.subplot(212)
	plt.loglog(errors[0], errors[1])
	plt.title('Convergence')
	
	plt.show()
