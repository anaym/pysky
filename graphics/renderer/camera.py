import datetime

import numpy

from geometry.avector import Horizontal
from geometry.sky_math import StarTimeHelper

#TODO: Watcher [+latitude, longitude, datetime, star_datetime]--> Camera
#TODO: rename sight_vector to see
#TODO: sight radius - wtf?

class Camera:
    def __init__(self, sight_radius, sight_vector: Horizontal):
        self._sight_radius = sight_radius
        self._sight_vector = Horizontal(sight_vector.alpha, sight_vector.delta)
        if sight_vector.delta == 90 or sight_vector.delta == -90:
            sight_vector.delta += 1e-9
        self._up_rotation = 0
        self._oy_vector = Horizontal(0, 0)
        self._update()

    def _update(self):
        self._oy_vector = (self._sight_vector + Horizontal(self.up_rotation, -90)).to_point()
        self._ox_vector = self._sight_vector.to_point().vector_mul(self._oy_vector)
        self._transformation_matrix = numpy.array([list(self._ox_vector), list(self._oy_vector), list(self._sight_vector.to_point())])

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
