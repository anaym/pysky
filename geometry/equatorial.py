import math
from geometry.angle_helpers import to_0_360, to_cos_period_cutted, apply
from geometry.horizontal import Horizontal
from geometry.nvector import NVector
from stars.sky_math import FirstEquatorialToHorizontal


class Equatorial(NVector):
    def __init__(self, a, d):
        super().__init__((to_0_360(a), to_cos_period_cutted(d)))

    def apply_time_rotation(self, star_time_degree):
        return Equatorial(self.a + star_time_degree, self.d)

    def to_horizontal_with_latitude(self, h) -> Horizontal:
        f, t, d = apply(math.radians, h, *self)

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
        return Horizontal(*apply(math.degrees, a, math.pi/2 - d))

    def to_horizontal_with_time(self, star_time_degree, h) -> Horizontal:
        return self.apply_time_rotation(star_time_degree).to_horizontal_with_latitude(h)


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

