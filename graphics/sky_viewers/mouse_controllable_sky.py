from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from math import atan2, degrees

from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.key_controllable_sky import KeyControllableSky
from stars.skydatabase import SkyDataBase


class MouseControllableSky(KeyControllableSky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):
        super().__init__(watcher, sky_base)
        self.setMouseTracking(True)
        self._move_mode = False
        self._mouse_pos = (0, 0)
        self._mouse_gpos = (0, 0)
        self._mouse_delta = (0, 0)

    def _apply_mouse_move(self):
        d = self._mouse_delta
        k = degrees(atan2(abs(d[1]), abs(d[0])))
        if k > 45:
            self._look_around(0, d[1]//10, 0)
        elif k < 45:
            self._look_around(d[0]//10, 0, 0)
        else:
            self._look_around(d[0]//20, d[1]//20, 0)

    def mouseMoveEvent(self, e: QMouseEvent):
        self._mouse_delta = (e.x() - self._mouse_pos[0], e.y() - self._mouse_pos[1])
        self._mouse_pos = (e.x(), e.y())
        self._mouse_gpos = (e.globalX(), e.globalY())
        if self._move_mode:
            self._apply_mouse_move()

    def mousePressEvent(self, e: QMouseEvent):
        if e.buttons() == Qt.LeftButton:
            self._move_mode = True
        self._mouse_pos = (e.x(), e.y())
        self._mouse_gpos = (e.globalX(), e.globalY())
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.buttons() == Qt.LeftButton:
            self._move_mode = False
        self._mouse_pos = (e.x(), e.y())
        self._mouse_gpos = (e.globalX(), e.globalY())
        super().mouseReleaseEvent(e)

