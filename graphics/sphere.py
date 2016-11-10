from PyQt5.QtGui import QColor

from vectors.vector import Vector


class Sphere:
    def __init__(self, radius: int):
        self.radius = radius
        self.centre = Vector(0, 0, 0)
        self.color = (128, 0, 0)
