import datetime

from geometry.equatorial import Equatorial
from stars.filter import Filter
from stars.star import Star


class SkyDataBase:
    def __init__(self, stars):
        consts = {star.constellation: [] for star in stars}
        for star in stars:
            consts[star.constellation].append(star)
        self._constellations = {}
        for cn in consts.keys():
            self._constellations[cn] = tuple(consts[cn])

    @property
    def constellations(self):
        return self._constellations.keys()

    def get_stars(self, selection: Filter):
        stars = []
        for constellation in selection.constellations:
            if not constellation in self._constellations:
                continue
            for star in self._constellations[constellation]:
                if selection.magnitude.is_include(star.magnitude):
                    stars.append(star)
        return stars
