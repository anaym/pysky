from multiprocessing.pool import Pool

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter

from geometry.equatorial import Equatorial
from geometry.horizontal import Horizontal
from graphics.renderer.projector import Projector, ProjectedStar
from graphics.renderer.utility import try_or_print
from graphics.renderer.watcher import Watcher
from stars.star import Star


class Renderer(Projector):
    def __init__(self, watcher: Watcher):
        super().__init__(watcher)
        self._buffer = QImage(QSize(0, 0), QImage.Format_RGB32)
        self._painter = QPainter()
        self._width = 0
        self._height = 0

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
            self.centre = (self._width//2, self._height//2)
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    @height.setter
    def height(self, value):
        if value != self.height:
            self._height = value
            self.centre = (self._width//2, self._height//2)
            self._buffer = QImage(QSize(self.width, self.height), QImage.Format_RGB32)

    def render(self, stars: list, forecast: bool):
        self._painter.begin(self._buffer)
        self._draw_background()
        for o in self.project(stars, forecast):
            self._draw_object(o)
        if self.settings.up_direction:
            self._draw_up()
        if self.settings.see_direction:
            self._draw_see()
        if self.settings.compass:
            self._draw_compass()
        self._painter.end()
        return self._buffer

    def _draw_object(self, pstar: ProjectedStar, with_color=True):
        if with_color:
            if self.settings.spectral:
                self.settings.apply_color(pstar.star.spectral_class, self._painter)
            else:
                self.settings.apply_color('star', self._painter)

        x, y = pstar.cx - pstar.diameter//2, pstar.cy - pstar.diameter//2
        self._painter.drawEllipse(x, y, pstar.diameter, pstar.diameter)

    def _draw_background(self):
        self.settings.apply_color("sky", self._painter)
        self._painter.drawRect(0, 0, self.width, self.height)

    def _draw_compass(self):
        n = self._draw_latidude_depencing_point(Equatorial(0, 90), 'north', -3)
        s = self._draw_latidude_depencing_point(Equatorial(0, -90), 'south', -3)
        try:
            self.settings.apply_color('north', self._painter)
            self._painter.drawLine(n.cx, n.cy, self.centre[0], self.centre[1])
            self.settings.apply_color('south', self._painter)
            self._painter.drawLine(self.centre[0], self.centre[1], s.cx, s.cy)
        except Exception as e:
            print(e)

    def _draw_latidude_depencing_point(self, pos: Equatorial, color, size):
        self.settings.apply_color(color, self._painter)
        lat = pos.to_horizontal_with_latitude(self.watcher.position.h)
        p_lat = self.project_star(lat, Star(pos, '', size, '', ''), True)
        if p_lat is not None and p_lat.in_eye:
            self._draw_object(p_lat, False)
        return p_lat

    def _draw_up(self):
        self.settings.apply_color('up', self._painter)
        if self.watcher.position is not None:
            prjctd = self.project_star(self.watcher.position, Star(Equatorial(0, 90), '', -1, '', ''), True)
            if prjctd is not None:
                if prjctd.in_eye:
                    self._draw_object(prjctd, False)
                self._painter.drawLine(self.centre[0], self.centre[1], prjctd.cx, prjctd.cy)

    def _draw_see(self):
        self.settings.apply_color('see', self._painter)
        diameter = self._get_size(-2)
        diameter, _ = self._distortion(diameter, 0, self.watcher.radius, 0)
        x, y = self.centre[0] - diameter // 2, self.centre[1] - diameter // 2
        self._painter.drawEllipse(x, y, diameter, diameter)



