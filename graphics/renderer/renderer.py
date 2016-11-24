from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from math import sqrt, e, log, pi

from geometry.horizontal import Horizontal
from graphics.renderer.settings import RenderSettings
from graphics.renderer.watcher import Watcher
from stars.star import Star


def fisheye_distortion(x, y, radius, z):
    r = radius * 10 / (1 - abs(z)) ** 2
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
        self._draw_background()
        self.settings.apply_color("star", self._painter)
        for o in (self._apply_time_rotation(s) for s in stars):
            self._draw_object(*o)
        if self.settings.up_direction:
            self._draw_up()
        if self.settings.see_direction:
            self._draw_see()
        self._painter.end()
        return self._buffer

    def _get_size(self, mag):
        mag = e**(self.settings.exp_const + mag * self.settings.exp_factor)
        mag = max(1, mag / self.watcher.radius)
        mag = 0.005 if not self.settings.magnitude else mag/500
        mag *= self.settings.pull
        return mag

    def _apply_time_rotation(self, star: Star):
        return star.position.to_horizontal_system(self.watcher.star_time.total_degree % 360, self.watcher.position.h), star

    def _draw_object(self, pos: Horizontal, star: Star):
        if not star is None:
            if self.settings.spectral:
                self.settings.apply_color(star.spectral_class, self._painter)
            diameter = self._get_size(star.magnitude)
        else:
            self.settings.apply_color('up', self._painter)
            diameter = self._get_size(-1)
        if self.watcher.see.angle_to(pos) <= self.watcher.radius:
            delta = pos.to_point() - self.watcher.see.to_point()
            prj_delta = delta.rmul_to_matrix(self.watcher.transformation_matrix)
            dx, dy = self._distortion(prj_delta.x, prj_delta.y, self.watcher.radius, prj_delta.z)
            diameter, _ = self._distortion(diameter, 0, self.watcher.radius, prj_delta.z)
            cx, cy = self._width//2 + dx, self._height//2 + dy
            x, y = cx - diameter//2, cy - diameter//2
            self._painter.drawEllipse(x, y, diameter, diameter)

    def _draw_background(self):
        self.settings.apply_color("sky", self._painter)
        self._painter.drawRect(0, 0, self.width, self.height)

    def _draw_up(self):
        self._draw_object(Horizontal(0, 90), None)
        self._draw_object(Horizontal(0, -90), None)

    def _draw_see(self):
        self.settings.apply_color('see', self._painter)
        diameter = self._get_size(-2)
        diameter, _ = self._distortion(diameter, 0, self.watcher.radius, 0)
        cx, cy = self._width // 2, self._height // 2
        x, y = cx - diameter // 2, cy - diameter // 2
        self._painter.drawEllipse(x, y, diameter, diameter)



