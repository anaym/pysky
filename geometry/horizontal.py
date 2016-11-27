import math
from geometry.angle_helpers import to_0_360, to_m180_180
from geometry.nvector import NVector
from geometry.sky_math import sin, cos
from geometry.vector import Vector


class Horizontal(NVector):
    def __init__(self, a, h):
        h = to_m180_180(h)
        if h > 90:
            h = 90 -(h - 90)
            a = to_0_360(180 + a)
        elif h < -90:
            h = -90 -(h - -90)
            a = to_0_360(180 + a)
        else:
            a = to_0_360(a)
        super().__init__((a, h))

    def to_point(self, radius=1) -> Vector:
        a = math.radians(-self.a)
        h = math.radians(self.h)
        z = radius*sin(h)
        r = radius*cos(h)
        x = r*cos(a)
        y = r*sin(a)
        return Vector(x, y, z)

    def cos_to(self, other):
        other = other.to_point()
        self = self.to_point()
        d = other - self
        if self.length == 0 or other.length == 0:
            return 0
        return 1 - d.length**2/2

    @property
    def a(self):
        return self[0]

    @property
    def h(self):
        return self[1]

    def __add__(self, other):
        return Horizontal(*self._add_(other))

    def __sub__(self, other):
        return Horizontal(*self._sub_(other))

    def __mul__(self, other):
        return Horizontal(*self._mul_(other))

    def __str__(self):
        return "({:.2f}, {:.2f})".format(self.a, self.h)
