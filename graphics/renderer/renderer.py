import datetime

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from geometry.avector import Horizontal, Equatorial
from geometry.sky_math import StarTimeHelper
from graphics.renderer.camera import Camera
from graphics.renderer.settings import RenderSettings
from graphics.renderer.watcher import Watcher
from stars.star import Star


def fisheye_distortion(x, y, sight_radius, z):
    r = sight_radius * 10 / (1 - abs(z))**2 # z преобразование для эффект рыбъего глаза
    return x*r, y*r


def scale_distortion(x, y, sight_radius, z):
    return x*sight_radius*10, y*sight_radius*10


class Renderer:
    def __init__(self, watcher: Watcher):
        super().__init__()
        self._buffer = QImage(QSize(0, 0), QImage.Format_RGB32)
        self._painter = QPainter()
        self.settings = RenderSettings()
        self.watcher = watcher
        self._width = 0
        self._height = 0
        self._distortion = fisheye_distortion

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, value):
        if value != self.width:
            self._width = value
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    @height.setter
    def height(self, value):
        if value != self.height:
            self._height = value
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    def _load_distortion(self):
        self._distortion = fisheye_distortion if self.settings.fisheye else scale_distortion

    def _draw_object(self, star: Star, p, translate=True):
        pos = star.position.to_horizontal_system(self.watcher.position.delta, self.watcher.star_time.total_degree % 360)
        if not translate:
            pos = Horizontal(star.position.alpha, star.position.delta)

        diameter = 0.01
        delta = pos.to_point() - self.watcher.sight_vector.to_point()
        prj_delta = delta.rmul_to_matrix(self.watcher.transformation_matrix)
        if self.watcher.sight_vector.angle_to(pos) <= self.watcher.eye_radius:
            dx, dy = self._distortion(prj_delta.x, prj_delta.y, self.watcher.eye_radius, prj_delta.z)
            diameter, _ = self._distortion(diameter, 0, self.watcher.eye_radius, prj_delta.z)
            cx, cy = self._width//2 + dx, self._height//2 + dy
            x, y = cx - diameter//2, cy - diameter//2
            p.drawEllipse(x, y, diameter, diameter)

    def _draw_background(self, p):
        self.settings.apply_color("sky", p)
        p.drawRect(0, 0, self.width, self.height)

    def render(self, stars: list) -> QImage:
        self._load_distortion()

        self._painter.begin(self._buffer)
        self._draw_background(self._painter)
        self.settings.apply_color("star", self._painter)
        for o in stars:
            self._draw_object(o, self._painter)
        self.settings.apply_color("point", self._painter)
        self._draw_object(Star(Equatorial(0, 90), 3, ''), self._painter, False)
        self._draw_object(Star(Equatorial(0, -90), 3, ''), self._painter, False)
        self._painter.end()
        return self._buffer
