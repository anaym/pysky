import math

import datetime
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor, QImage
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QWidget

from geometry.equatorial import SecondEquatorial, Horizontal
from geometry.point import Point
from graphics.renderer._geometry import translate_coordinates, rescale_angle_distance, project, get_see_distance, \
    extract_2d
from graphics.renderer.camera import Camera
from graphics.renderer.settings import RenderSettings
from stars.skybase import SkySphere
from stars.star import Star

#TODO: выпилить для презентации: землю, надир

class Canvas(QWidget):
    def __init__(self, camera: Camera, dt: datetime):
        super().__init__()
        self._canvas = QImage(self.size(), QImage.Format_RGB32) #TODO: rename: _buffer
        self.settings = RenderSettings()
        self.camera = camera
        self.datetime = dt

    def get_visible_radius(self):
        return math.sqrt(self._canvas.width()**2 + self._canvas.height()**2) // 2

    def get_observer_x(self):
        return self._canvas.width() // 2

    def get_observer_y(self):
        return self._canvas.height() // 2

    def get_star_diameter(self, star: Star, sight_radius):
        return max(
            1,
            (400 // sight_radius) //
            (Star.POGSON_RATIO**((star.m - 1) / 4))
        )

    def redraw(self, stars, sky_sphere: SkySphere):
        sight_radius = self.camera.sight_radius
        sight_vector = self.camera.get_sight_vector()
        painter = QPainter()
        painter.begin(self._canvas)
        self._draw_background(painter)
        self._draw_stars(stars, sight_vector, sight_radius, painter)
        #self._draw_earth(sight_vector, sight_radius, painter)
        self._draw_landmarks(sky_sphere, sight_vector, sight_radius, painter)
        painter.end()
        self.repaint()

    def _draw_stars(self, stars, sight_vector, sight_radius, p):
        self.settings.apply_color("star", p)
        for star in stars:
            self._draw_star(star, sight_vector, sight_radius, p)

    def _draw_star(self, star: Star, sight_vector, sight_radius, p, translate=True):
        pos = star.position.to_horizontal_system(
                self.camera.latitude,
                self.camera.get_lst(self.datetime) * 15
            )
        if not translate:
            pos = Horizontal(star.position.alpha, star.position.delta)

        diametr = self.get_star_diameter(star, sight_radius)

        ps = pos.to_point()
        s = sight_vector.to_point()
        delta = ps - s
        up = self.camera.up_vector.to_point()
        projected = delta.change_basis(s.vector_mul(up), up, s)
        r = sight_vector.angle_to(pos)
        if r <= sight_radius:
            dx, dy = projected.x, projected.y
            r = sight_radius *10 / (1 - abs(projected.z)) # z преобразование для эффект рыюъего глаза
            dx, dy = dx*r, dy*r
            cx, cy = self.get_observer_x() + dx, self.get_observer_y() + dy
            x, y = cx - diametr//2, cy - diametr//2
            p.drawEllipse(x, y, diametr, diametr)


    def _draw_landmarks(self, sky_sphere: SkySphere, sight_vector, sight_radius, p):
        self.settings.apply_color("point", p)
        self._draw_star(sky_sphere.get_zenith(), sight_vector, sight_radius, p, False)
        self._draw_star(sky_sphere.get_nadir(), sight_vector, sight_radius, p, False)

    def _draw_background(self, p):
        self.settings.apply_color("sky", p)
        p.drawRect(0, 0, self.width(), self.height())

    def _draw_earth(self, sight_vector: SecondEquatorial, sight_radius, p):
        if sight_vector.delta < sight_radius:
            dist_to_ground = rescale_angle_distance(sight_radius, self.get_visible_radius(), sight_vector.delta)
            ground_y = self.get_observer_y() + dist_to_ground
            self.settings.apply_color("earth", p)
            p.drawRect(0, max(0, ground_y), self._canvas.width(), self._canvas.height())

    def resizeEvent(self, event):
        self._canvas = self._canvas.scaled(self.size())

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self._canvas)
        painter.end()
