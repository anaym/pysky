import math
from geometry.horizontal import Horizontal
from geometry.nvector import NVector
from stars.sky_math import FirstEquatorialToHorizontal


class Equatorial(NVector):
    def __init__(self, a, d):
        super().__init__((a, d))

    def to_horizontal_system(self, star_time_degree, h):
        timed = Equatorial(self.a + star_time_degree, self.d)
        d = math.radians(timed.d)
        t = math.radians(timed.a)
        f = math.radians(h)

        cosz = FirstEquatorialToHorizontal.cosz(f, d, t)
        sina_sinz = FirstEquatorialToHorizontal.siza_sinz(d, t)
        cosa_sinz = FirstEquatorialToHorizontal.cosa_sinz(f, d, t)

        sinz = math.sqrt(1 - cosz**2)
        if sinz == 0:
            return Horizontal(0, 90)
        sina = sina_sinz/sinz
        cosa = cosa_sinz / sinz
        a = math.atan2(sina, cosa)
        d = math.atan2(sinz, cosz)
        return Horizontal.star_compatible(math.degrees(a), 90 - math.degrees(d))

    @property
    def a(self):
        return self[0]

    @property
    def d(self):
        return self[1]

    def __add__(self, other):
        return Equatorial(*self._add_(other))

    def __sub__(self, other):
        return Equatorial(*self._sub_(other))

    def __mul__(self, other):
        return Equatorial(*self._mul_(other))

