from math import pi
from vectors.vector import Vector


class Camera:
    def __init__(self):
        self.position = Vector(0, 0, 0)
        self.view = Vector(1, 0, 0)
        self.up = Vector(0, 0, 1)
        self.angle = 60

    @property
    def look_params(self):
        eye = self.position
        centre = self.position + self.view
        up = self.up
        return eye.x, eye.y, eye.z, centre.x, centre.y, centre.z, up.x, up.y, up.z

    @property
    def perspective_params(self):
        return self.angle, 1.33, 0.1, 100.0
