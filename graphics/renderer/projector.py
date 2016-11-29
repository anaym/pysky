from collections import namedtuple
from math import e
from geometry.horizontal import Horizontal
from graphics.renderer.settings import Settings
from utility import try_or_print
from graphics.renderer.watcher import Watcher
from stars.star import Star


def fisheye_distortion(x, y, radius, z):
    r = radius * 10 / (1 - abs(z)) ** 2
    return x*r, y*r


def scale_distortion(x, y, radius, z):
    return x * radius * 10, y * radius * 10


ProjectedStar = namedtuple('ProjectedStar', ['cx', 'cy', 'horizontal', 'diameter', 'star', 'in_eye'])


class Projector:
    def __init__(self, watcher: Watcher):
        super().__init__()
        self.settings = Settings()
        self.watcher = watcher
        self.distortion = fisheye_distortion
        self._objects = []
        self.centre = (0, 0)
        self._constellations = {}

    @try_or_print
    def project(self, stars: list, forecast: bool) -> list:
        self.distortion = fisheye_distortion if self.settings.fisheye else scale_distortion

        good = self._objects
        self._objects = []
        all = not forecast or len(good) == 0
        src = stars if all else (s.star for s in good)
        if all:
            self._constellations = {}
        actual = map(self._apply_time_rotation, src)
        for o in actual:
            if o[1].constellation in self._constellations:
                current = self._constellations[o[1].constellation]
                self._constellations[o[1].constellation] = min(current, o, key=lambda s: s[1].magnitude)
            else:
                self._constellations[o[1].constellation] = o
            p = self.project_star(*o)
            if p is not None:
                self._objects.append(p)

        return self._objects

    def find_star(self, screenX, screenY, delta):
        good = (i for i in self._objects if (abs(i.cx - screenX) + abs(i.cy - screenY)) < (delta + i.diameter))
        return min(good, key=lambda i: abs(i.cx - screenX) + abs(i.cy - screenY) - i.diameter, default=None)

    def find_constellation(self, name):
        if name in self._constellations:
            return self._constellations[name][0]

    def _get_size(self, mag):
        mag = e**(self.settings.exp_const + mag * self.settings.exp_factor)
        mag = max(1, mag / self.watcher.radius)
        mag = 0.005 if not self.settings.magnitude else mag/500
        mag *= self.settings.pull
        return mag

    def _apply_time_rotation(self, star: Star):
        return self.watcher.to_horizontal(star.position), star

    def project_star(self, pos: Horizontal, star: Star, always_project: bool=False):
        diameter = self._get_size(star.magnitude if star is not None else -1)
        in_eye = self.watcher.radius_low_bound < self.watcher.see.cos_to(pos) <= 1
        if in_eye or always_project:
            delta = pos.to_point() - self.watcher.see.to_point()
            prj_delta = delta.rmul_to_matrix(self.watcher.transformation_matrix)
            dx, dy = self.distortion(prj_delta.x, prj_delta.y, self.watcher.radius, prj_delta.z)
            diameter, _ = self.distortion(diameter, 0, self.watcher.radius, prj_delta.z)
            cx, cy = self.centre[0] + dx, self.centre[1] + dy
            return ProjectedStar(cx, cy, pos, diameter, star, in_eye)
