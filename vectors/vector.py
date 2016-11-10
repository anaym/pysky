from math import cos, sin, pi, atan2, sqrt, acos, asin
from collections import namedtuple
from vectors._base import VectorBase
from vectors.math_conversion import to_radian, to_degree


Horizontal = namedtuple("Horizontal", ["h", "a", "r"])
FirstEquatorial = namedtuple("FirstEquatorial", ["d", "t", "r"])
SecondEquatorial = namedtuple("FirstEquatorial", ["d", "a", "r"])

class Vector(VectorBase):
    # TODO: implement
    @staticmethod
    def from_first_equatorial(d, t, radius=1): #time rotation
        cosh = sin()

    @staticmethod
    def from_second_equatorial(d, a, radius=1):
        raise NotImplementedError("TODO")

    @staticmethod
    def from_horizontal(h, a, radius=1):
        a = -to_radian(a)
        h = to_radian(h)
        z = sin(h)*radius
        pr = sqrt(radius**2 - z**2)
        x = cos(a)*pr
        y = sin(a)*pr
        v = Vector(x, y, z)
        v._pdir = (cos(a), sin(a))
        return v

    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self._pdir = (x, y)

    def to_first_equatorial(self):
        raise NotImplementedError("TODO")

    def to_second_equatorial(self):
        raise NotImplementedError("TODO")

    def to_horizontal(self):
        h = asin(self.z/self.length) if self.length != 0 else 0
        x, y = self._pdir
        a = atan2(y, x)
        return Horizontal(to_degree(h), -to_degree(a), self.length)

    def __add__(self, other):
        return Vector(other.x + self.x, other.y + self.y, other.z + self.z)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector(self.x*other, self.y*other, self.z*other)
        else:
            raise TypeError("Not supported type")

    def __sub__(self, other):
        return self + other*(-1)
