import math
from math import sin, cos
from geometry.vector import Vector


class AngleVectror:
    def __init__(self, alpha, delta):
        self._alpha = alpha
        self._delta = delta

    @property
    def alpha(self):
        return self._alpha

    @property
    def delta(self):
        return self._delta

    def length(self):
        return math.sqrt(self.alpha**2 + self.delta**2)

    def __str__(self):
        return "({}, {})".format(self.alpha, self.delta)

    def __eq__(self, other):
        return AngleVectror(self.alpha - other.alpha, self.delta - other.delta) < 1e-5


class Equatorial(AngleVectror):
    def __init__(self, a, d):
        super().__init__(a, d)

    def apply_time(self, sidereal_time):
        return Equatorial(self.alpha + sidereal_time, self.delta)

    def to_horizontal_system(self, latitude, sidereal_time):
        timed = self.apply_time(sidereal_time)
        delta = math.radians(timed.delta)
        t = math.radians(timed.alpha)
        φ = math.radians(latitude)
        cos_z = sin(φ)*sin(delta) + cos(delta)*cos(φ)*cos(t)
        sin_z = math.sqrt(1 - cos_z**2)
        if sin_z == 0:
            return Horizontal(0, 90)
        sin_A = cos(delta)*sin(t)/sin_z
        cos_A = (-cos(φ)*sin(delta) + sin(φ)*cos(delta)*math.cos(t)) / sin_z
        a = math.atan2(sin_A, cos_A)
        z = math.atan2(sin_z, cos_z)
        #TODO: create method to_first_period
        return Horizontal((math.degrees(a) + 360) % 360, 90 - math.degrees(z))

    def __add__(self, other):
        return Equatorial(self.alpha + other.alpha, self.delta + other.delta)

    def __sub__(self, other):
        return Equatorial(self.alpha - other.alpha, self.delta - other.delta)


class Horizontal(AngleVectror):
    def __init__(self, a, d):
        super().__init__(a, d)

    def to_point(self, radius=1) -> Vector:
        a = math.radians(-self.alpha)
        h = math.radians(self.delta)
        z = radius*math.sin(h)
        r = math.sqrt(radius**2 - z**2)
        x = r*math.cos(a)
        y = r*math.sin(a)
        return Vector(x, y, z)

    def angle_to(self, other_point):
        return math.degrees(self.to_point().angle_to(other_point.to_point()))

    def __add__(self, other):
        return Horizontal(self.alpha + other.alpha, self.delta + other.delta)

    def __sub__(self, other):
        return Horizontal(self.alpha - other.alpha, self.delta - other.delta)
