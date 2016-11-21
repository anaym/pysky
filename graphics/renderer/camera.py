import datetime

import numpy

from geometry.avector import Horizontal


class Camera:
    def __init__(self, longitude, latitude, sight_radius, sight_vector: Horizontal):
        if latitude == 90 or latitude == -90:
            latitude += 1e-9
        self._sight_radius = sight_radius
        self._sight_vector = Horizontal(sight_vector.alpha, sight_vector.delta)
        if sight_vector.delta == 90 or sight_vector.delta == -90:
            sight_vector.delta += 1e-9
        self._longitude = longitude
        self._latitude = latitude
        self._up_rotation = 0
        self._oy_vector = Horizontal(0, 0)
        self._update()

    def _update(self):
        self._oy_vector = (self._sight_vector + Horizontal(self.up_rotation, -90)).to_point()
        self._ox_vector = self._sight_vector.to_point().vector_mul(self._oy_vector)
        self._transformation_matrix = numpy.array([list(self._ox_vector), list(self._oy_vector), list(self._sight_vector.to_point())])

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = min(90, max(-90, latitude))

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude % 360

    @property
    def sight_radius(self):
        return self._sight_radius

    @sight_radius.setter
    def sight_radius(self, radius):
        self._sight_radius = radius

    @property
    def up_vector(self) -> Horizontal:
        return self._oy_vector

    @property
    def sight_vector(self):
        return self._sight_vector

    @sight_vector.setter
    def sight_vector(self, value: Horizontal):
        #TODO: подозрительно
        self._sight_vector = Horizontal(value.alpha%360, min(max(value.delta, -90 + 1e-9), 90 - 1e-9))
        self._update()

    @property
    def up_rotation(self):
        return self._up_rotation

    @up_rotation.setter
    def up_rotation(self, value):
        self._up_rotation = value
        self._update()

    @property
    def transformation_matrix(self):
        return self._transformation_matrix

    def get_lst(self, date_time: datetime.datetime):
        d = self.get_julian_day(date_time)
        t = d / 36525
        hours = (280.46061837 + 360.98564736629 * d + 0.000388 * (t**2) + self._longitude) % 360 / 15
        return hours

    @staticmethod
    def get_julian_day(date_time: datetime.datetime):
        dwhole = (
            367 * date_time.year -
            int(7 * (date_time.year + int((date_time.month + 9) / 12)) / 4) +
            int(275 * date_time.month / 9) +
            date_time.day - 730531.5
        )
        dfrac = (date_time.hour + date_time.minute/60 + date_time.second / 3600) / 24
        return dwhole + dfrac
