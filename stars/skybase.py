import datetime

from geometry.avector import Equatorial
from stars.star import Star


class SkyBase:
    def __init__(self, stars):
        self._stars = stars
        self._constellations = {star.constellation: [] for star in stars}
        for star in stars:
            self._constellations[star.constellation].append(star)

    @property
    def constellations(self):
        return self._constellations.keys()

    def get_stars(self, avaible_constellations: set):
        stars = []
        for constellation in avaible_constellations:
            if not constellation in self._constellations:
                continue
            for star in self._constellations[constellation]:
                stars.append(star)
        return stars
