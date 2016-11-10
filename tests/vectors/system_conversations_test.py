import unittest
from math import sqrt, pi

from tests.vectors.utility.for_decorator import for_range
from vectors.vector import Vector, Horizontal


class HorizontalConversationTest(unittest.TestCase):
    def setUp(self):
        self.epsilon = 0.0001

    @staticmethod
    def distance(a: Horizontal, b: Horizontal):
        dh = (a.h - b.h)**2
        da = (a.a - b.a)**2
        dr = (a.r - b.r)**2
        return sqrt(da+dh+dr)

    @for_range('h', -180, 180)
    @for_range('a', -90, 90)
    def qtest_save_radius_as_length(self, h, a):
        hor = Horizontal(h, a, 1000)
        v = Vector.from_horizontal(*hor)
        self.assertLess(abs(1000 - v.length), self.epsilon, str(h) + ' ' + str(a))

    @for_range('h', -180, 180)
    @for_range('a', -90, 90)
    def qtest_save_length_as_radius(self, h, a):
        hor = Horizontal(h, a, 1000)
        v = Vector.from_horizontal(*hor)
        horr = v.to_horizontal()
        self.assertLess(abs(v.length - horr.r), self.epsilon, str(h) + ' ' + str(a))

    @for_range('h', -100, 100)
    @for_range('a', -80, 80)
    def test_correct_reconversion(self, h, a):
        hor = Horizontal(h, a, 5)
        v = Vector.from_horizontal(*hor)
        horr = v.to_horizontal()
        self.assertLess(self.distance(horr, hor), self.epsilon, str(hor) + '->' + str(horr))


if __name__ == '__main__':
    unittest.main()

