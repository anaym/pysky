import math
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen

from graphics.renderer.utility import hexstr_to_color
from stars.sky_math import sign
from stars.star import SPECTRAL_MAP


class RenderSettings:
    def __init__(self):
        self.fisheye = True
        self.spectral = True
        self.magnitude = True
        self._earth_color = QColor(0, 100, 100)
        self._star_color = QColor(255, 255, 255)
        self._sky_color = QColor(0, 0, 0)
        self._up_color = QColor(255, 0, 255)
        self._down_color = QColor(0, 255, 255)
        self._earth_drawer = (QBrush(self._earth_color), QPen(self._earth_color))
        self._star_drawer = (QBrush(self._star_color), QPen(self._star_color))
        self._sky_drawer = (QBrush(self._sky_color), QPen(self._sky_color))
        self._up_drawer = (QBrush(self._up_color), QPen(self._up_color))
        self._down_drawer = (QBrush(self._down_color), QPen(self._down_color))
        self._spectrals = {}
        for i in SPECTRAL_MAP.keys():
            clr = hexstr_to_color(SPECTRAL_MAP[i])
            self._spectrals[i] = (QBrush(clr), QPen(clr))

    def get_drawer(self, color_name: str):
        if color_name in self._spectrals:
            return self._spectrals[color_name]
        fullname = "_" + color_name + "_drawer"
        return self.__getattribute__(fullname)

    def apply_color(self, name: str, painter: QPainter):
        b, p = self.get_drawer(name)
        painter.setBrush(b)
        painter.setPen(p)


class ControllableRenderSettings:
    def __init__(self):
        self.second_per_second = 1
        self.zoom = 1

    @property
    def speed_rank(self):
        if self.second_per_second == 0:
            return 0
        return (math.log10(abs(self.second_per_second)) + 1) * sign(self.second_per_second)

    @speed_rank.setter
    def speed_rank(self, value):
        if value > 10:
            raise ValueError()
        self.second_per_second = 10 ** (abs(value) - 1) * sign(value)
