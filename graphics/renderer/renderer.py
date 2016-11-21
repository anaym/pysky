import math
import datetime
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
from geometry.avector import Horizontal, Equatorial
from graphics.renderer.camera import Camera
from graphics.renderer.settings import RenderSettings
from stars.skybase import SkyBase
from stars.star import Star


def fisheye_distortion(dx, dy, sight_radius, z):
    r = sight_radius * 10 / (1 - abs(z)) # z преобразование для эффект рыюъего глаза
    return dx*r, dy*r


class Canvas(QWidget):
    def __init__(self, camera: Camera, dt: datetime):
        super().__init__()
        self._buffer = QImage(self.size(), QImage.Format_RGB32)
        self._painter = QPainter()
        self.settings = RenderSettings()
        self.camera = camera
        self.datetime = dt
        self._width = 0
        self._height = 0
        self.objects = []

    def repaint(self):
        self._width, self._height = self.width(), self.height()
        self._painter.begin(self._buffer)
        self._draw_background(self._painter)
        self.settings.apply_color("star", self._painter)
        for o in self.objects:
            self._draw_objects(o, self._painter)
        self.settings.apply_color("point", self._painter)
        self._draw_objects(Star(Equatorial(0, 90), 3, ''), self._painter, False)
        self._draw_objects(Star(Equatorial(0, -90), 3, ''), self._painter, False)
        self._painter.end()
        super().repaint()

    def _draw_objects(self, star: Star, p, translate=True):
        pos = star.position.to_horizontal_system(
                self.camera.latitude,
                self.camera.get_lst(self.datetime) * 15 #TODO: WTF???
            )
        if not translate:
            pos = Horizontal(star.position.alpha, star.position.delta)

        diameter = 2
        delta = pos.to_point() - self.camera.sight_vector.to_point()
        prj_delta = delta.rmul_to_matrix(self.camera.transformation_matrix)
        r = self.camera.sight_vector.angle_to(pos)
        if r <= self.camera.sight_radius:
            dx, dy = fisheye_distortion(prj_delta.x, prj_delta.y, self.camera.sight_radius, prj_delta.z)
            cx, cy = self._width//2 + dx, self._height//2 + dy
            x, y = cx - diameter//2, cy - diameter//2
            p.drawEllipse(x, y, diameter, diameter)

    def _draw_background(self, p):
        self.settings.apply_color("sky", p)
        p.drawRect(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        self._buffer = self._buffer.scaled(self.size())

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self._buffer)
        painter.end()
