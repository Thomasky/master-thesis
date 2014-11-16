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
        plt.show()
        self.assertEqual(lattice_points[0, 0], 0)
