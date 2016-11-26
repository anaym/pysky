import numpy
from geometry.horizontal import Horizontal


class Camera:
    def __init__(self, see: Horizontal, radius):
        self._see = see
        self._radius = radius
        self._up_rotation = 0
        self._oyp = Horizontal(0, 0)
        self._update()

    def _update(self):
        self._oy = (self._see + Horizontal(self.up_rotation, -90))
        self._oyp = self._oy.to_point()
        self._ox_vector = self._see.to_point().vector_mul(self._oyp)
        self._transformation_matrix = [self._ox_vector, self._oyp, self._see.to_point()]

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @property
    def up(self) -> Horizontal:
        return self._oy

    @property
    def see(self):
        return self._see

    @see.setter
    def see(self, value: Horizontal):
        self._see = Horizontal(value.a, value.h)
        self._update()

    @property
    def up_rotation(self):
        return self._up_rotation

    @up_rotation.setter
    def up_rotation(self, value):
        self._up_rotation = value % 360
        self._update()

    @property
    def transformation_matrix(self):
        return self._transformation_matrix
