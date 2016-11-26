import unittest
from unittest import TestCase

from math import cos, radians, sin, tan

from geometry.horizontal import Horizontal
from tests.utility.for_decorator import for_range


def dcos(a):
    return cos(radians(a))


def dsin(a):
    return sin(radians(a))



class HorizontalShouldBeContinuumTest(TestCase):
    @for_range('a', range(0, 360))
    @for_range('h', range(0, 360))
    def test_h_coninuum(self, a, h):
        v = Horizontal(a, h)
        self.assertLess(abs(dsin(v.h) - dsin(h)), 1e-3, '{}, {} --> {}, {}'.format(a, h, v.a, v.h))

if __name__ == '__main__':
    unittest.main()

