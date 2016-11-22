import sys
import datetime
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from geometry.horizontal import Horizontal
from graphics.autogui.cast_tools import to_widget
from graphics.configurator import Configurator
from graphics.image_viewer import ImageViewer
from graphics.utility import KeyProcessor, profile
from graphics.renderer.renderer import Renderer
from graphics.renderer.settings import ControllableRenderSettings
from graphics.renderer.watcher import Watcher
from stars.skydatabase import SkyDataBase


def star_window_key_processor(self):
    return KeyProcessor() \
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
        .register("image", self.viewer.save_to_file) \
        .bind(Qt.Key_I, "image", ("stars.jpg",)) \
        .register("full_screen", self._switch_full_screen) \
        .bind(Qt.Key_F, "full_screen") \
        .register("exit", lambda: sys.exit(0))\
        .bind(Qt.Key_Escape, "exit")


class QtStars(QMainWindow):
    def __init__(self, watcher: Watcher, sky_sphere: SkyDataBase):
        super().__init__()

        self._renderer = Renderer(watcher)
        self.settings = ControllableRenderSettings()

        self._available_constellations = sky_sphere.constellations
        self._objects = []
        self._sky_sphere = sky_sphere

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(33)
        self._timer.timeout.connect(self._rerender)

        self._create_ui()
        self.setFocus()

        self._rerender()
        self._timer.start()

        self._configurator_widget.setVisible(False)
        self._key_processor = star_window_key_processor(self)

    def _switch_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _switch_pause(self):
        if self._timer.isActive():
            self._timer.stop()
        else:
            self._timer.start()

    def _switch_menu(self):
        self._configurator_widget.setVisible(not self._configurator_widget.isVisible())

    def _create_ui(self):
        main = QtWidgets.QGridLayout()
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)
        self.viewer = ImageViewer()
        main.addWidget(self.viewer, 0, 0)
        main.setColumnStretch(0, 1)

        self.setWindowTitle("Sky")
        self.resize(1000, 700)
        self.setCentralWidget(to_widget(main))
        self.show()

        self._configurator = Configurator(self._renderer.watcher, self.settings, self._renderer.settings, self._available_constellations)
        self._configurator.constellationsChangedHandler = self._apply_constellation_filter
        self._configurator.imageSaveRequestedHandler = lambda: self.viewer.image.save("sky.jpg")
        self._configurator.switchPauseRequestedHandler = self._switch_pause
        self._configurator_widget = self._configurator.to_widget()
        main.addWidget(self._configurator_widget, 0, 1)

    def _look_around(self, *delta):
        da, dd, dr = delta[0], delta[1], delta[2]
        self._renderer.watcher.see += Horizontal(da, dd)
        self._renderer.watcher.up_rotation += dr
        self.setFocus()

    def _update_image(self):
        self._renderer.width = self.viewer.width()
        self._renderer.height = self.viewer.height()
        image = self._renderer.render(self._objects)
        self.viewer.image = image

    @profile
    def _rerender(self, exec_delta: datetime.timedelta):
        if exec_delta is None:
            selected = self._configurator.constellation_filter.selected
            self._apply_constellation_filter(selected)
            return
        datetime.timedelta(0, 0, )
        self._renderer.watcher.local_time = self._renderer.watcher.local_time + datetime.timedelta(0, 0, exec_delta.microseconds * self.settings.speed)
        self._update_image()
        self._configurator.handle()

    def _apply_constellation_filter(self, slctd):
        stars = self._sky_sphere.get_stars(slctd)
        self._objects = stars
        self._update_image()

    def keyPressEvent(self, e):
        self._key_processor.execute(e.key())

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()
