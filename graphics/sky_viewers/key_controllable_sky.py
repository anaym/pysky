import sys
from PyQt5.QtCore import Qt
from geometry.horizontal import Horizontal
from graphics.renderer.utility import try_or_print
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.filterable_sky import FilterableSky
from graphics.sky_viewers.utility import KeyProcessor
from stars.filter import Filter
from stars.skydatabase import SkyDataBase


class KeyControllableSky(FilterableSky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase, filter: Filter):
        super().__init__(watcher, sky_base, filter)
        self.setFocus()
        self._configurator_widget.setVisible(False)
        self._key_processor = KeyProcessor() \
            .register("look", self._look_around) \
            .bind(Qt.Key_W, 'look', (0, 2, 0)) \
            .bind(Qt.Key_A, 'look', (2, 0, 0)) \
            .bind(Qt.Key_S, 'look', (0, -2, 0)) \
            .bind(Qt.Key_D, 'look', (-2, 0, 0)) \
            .bind(Qt.Key_Q, 'look', (0, 0, 2)) \
            .bind(Qt.Key_E, 'look', (0, 0, -2)) \
            .register("pause", self._switch_pause) \
            .bind(Qt.Key_Space, 'pause') \
            .register("menu", self._switch_menu) \
            .bind(Qt.Key_M, 'menu') \
            .register("filter", self._switch_filter) \
            .bind(Qt.Key_N, 'filter') \
            .register("image", self.viewer.save_to_file) \
            .bind(Qt.Key_I, "image") \
            .register("full_screen", self._switch_full_screen) \
            .bind(Qt.Key_F, "full_screen") \
            .register("exit", lambda: sys.exit(0))\
            .bind(Qt.Key_Escape, "exit")

    def _switch_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _switch_menu(self):
        self._configurator_widget.setVisible(not self._configurator_widget.isVisible())

    def _switch_filter(self):
        self._filter_widget.setVisible(not self._filter_widget.isVisible())

    @try_or_print
    def _look_around(self, *delta):
        da, dh, dr = delta
        self.renderer.watcher.up_rotation += dr
        if abs(self.renderer.watcher.see.h + dh) > 90:
            return
        self.renderer.watcher.see += Horizontal(da, dh)

    def keyPressEvent(self, e):
        self._key_processor.execute(e.key())
