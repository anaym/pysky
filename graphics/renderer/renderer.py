from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter

from geometry.horizontal import Horizontal
from geometry.equatorial import Equatorial
from graphics.renderer.settings import RenderSettings
from graphics.renderer.watcher import Watcher
from stars.star import Star


def fisheye_distortion(x, y, radius, z):
    r = radius * 10 / (1 - abs(z)) ** 2 # z преобразование для эффект рыбъего глаза
    return x*r, y*r


def scale_distortion(x, y, radius, z):
    return x * radius * 10, y * radius * 10


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

    def render(self, stars: list) -> QImage:
        self._distortion = fisheye_distortion if self.settings.fisheye else scale_distortion

        self._painter.begin(self._buffer)
        self._draw_background(self._painter)
        self.settings.apply_color("star", self._painter)
        for o in (self._apply_time_rotation(s) for s in stars):
            self._draw_object(o, self._painter)
        self.settings.apply_color("up", self._painter)
        self._draw_object(Horizontal(0, 90), self._painter)
        self.settings.apply_color("down", self._painter) #TODO: what is it? Повторить отображения координат
        self._draw_object(Horizontal(0, -90), self._painter)
        self._painter.end()
        return self._buffer

    def _apply_time_rotation(self, star: Star):
        return star.position.to_horizontal_system(self.watcher.position.h, self.watcher.star_time.total_degree % 360)

    def _draw_object(self, pos: Horizontal, p):
        diameter = 0.01
        delta = pos.to_point() - self.watcher.see.to_point()
        prj_delta = delta.rmul_to_matrix(self.watcher.transformation_matrix)
        if self.watcher.see.angle_to(pos) <= self.watcher.eye_radius:
            dx, dy = self._distortion(prj_delta.x, prj_delta.y, self.watcher.eye_radius, prj_delta.z)
            diameter, _ = self._distortion(diameter, 0, self.watcher.eye_radius, prj_delta.z)
            cx, cy = self._width//2 + dx, self._height//2 + dy
            x, y = cx - diameter//2, cy - diameter//2
            p.drawEllipse(x, y, diameter, diameter)

    def _draw_background(self, p):
        self.settings.apply_color("sky", p)
        p.drawRect(0, 0, self.width, self.height)

