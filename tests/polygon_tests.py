import unittest
import numpy as np
import polygon as p


class Test(unittest.TestCase):

    def test_get_sharp_traingle(self):
        tri = p.create_sharp_triangle(np.pi / 3)
        self.assertEquals(tri[0, 0], 0)

    def test_includes_point(self):
        polygon = p.get_regular_polygon(4)
        point = (-0.5, 0.5)
        self.assertTrue(p.includes_point(polygon, point))

    def test_includes_polygon(self):
        search_polygon = p.get_regular_polygon(4)
        polygon = p.create_sharp_triangle(np.pi / 10)
        self.assertFalse(p.includes_polygon(search_polygon, polygon))
