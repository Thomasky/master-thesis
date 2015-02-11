import unittest
import lattice
import matplotlib.pyplot as plt
import numpy as np


class Test(unittest.TestCase):

    def test_get_lattice_points(self):
        num_dimensions = 2
        num_points = 100
        lattice_points = lattice.get_lattice_points(num_dimensions, num_points)

        plt.figure()
        plt.plot(lattice_points[0, :], lattice_points[1, :], 'b.')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        self.assertEqual(lattice_points[0, 0], 0)

    def test_montecarlo(self):
        np.random.seed(123458)

        num_points = 100
        samplesx = np.random.uniform(0, 1, num_points)
        samplesy = np.random.uniform(0, 1, num_points)

        plt.figure()
        plt.plot(samplesx, samplesy, 'b.')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        self.assertEqual(samplesx[0, 0], 0)
