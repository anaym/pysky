import datetime
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QMainWindow

from geometry.avector import Horizontal
from graphics.configurator import Configurator
from graphics.image_viewer import ImageViewer
from graphics.renderer.renderer import Renderer
from graphics.renderer.settings import ControllableRenderSettings
from graphics.renderer.watcher import Watcher
from stars.skybase import SkyBase


class StarsWindow(QMainWindow):
    def __init__(self, watcher: Watcher, sky_sphere: SkyBase):
        super().__init__()

        self._renderer = Renderer(watcher)
        self._objects = []
        self._sky_sphere = sky_sphere
        self.settings = ControllableRenderSettings()
        self._key_commands = {
            QtCore.Qt.Key_A: lambda: self._change_sight_vector(1, 0),
            QtCore.Qt.Key_D: lambda: self._change_sight_vector(-1, 0),
            QtCore.Qt.Key_W: lambda: self._change_sight_vector(0, 1),
            QtCore.Qt.Key_S: lambda: self._change_sight_vector(0, -1),

            QtCore.Qt.Key_Q: lambda: self._change_sight_vector(0, 0, 10),
            QtCore.Qt.Key_E: lambda: self._change_sight_vector(0, 0, -10),
        }

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000 / self.settings.fps)
        self._timer.timeout.connect(self._on_timer_tick)

        self._constellations = sky_sphere.constellations

        self._cmodel = QStandardItemModel()
        self._create_ui()
        self.setFocus()

        self._last_tick_time = datetime.datetime.now()
        self._on_timer_tick()
        self._timer.start()

    def _switch_pause(self):
        if self._timer.isActive():
            self._timer.stop()
        else:
            self._timer.start()

    def _create_ui(self):
        main = QtWidgets.QGridLayout()
        self.viewer = ImageViewer()
        main.addWidget(self.viewer, 0, 0)
        main.setColumnStretch(0, 1)

        self.setWindowTitle("Sky")
        self.resize(1000, 700)
        panel = QtWidgets.QWidget()
        panel.setLayout(main)
        self.setCentralWidget(panel)
        self.show()

        self._configurator = Configurator(self._renderer.watcher, self.settings, self._renderer.settings, self._constellations)
        self._configurator.constellationsChangedHandler = self._apply_constellation_filter
        self._configurator.imageSaveRequestedHandler = lambda: self.viewer.image.save("sky.jpg")
        self._configurator.switchPauseRequestedHandler = self._switch_pause
        main.addLayout(self._configurator, 0, 1)

    def _change_sight_vector(self, da=0, dd=0, dr=0):
        self._renderer.watcher.sight_vector += Horizontal(da, dd)
        self._renderer.watcher.up_rotation += dr
        self.setFocus()

    def _update_image(self):
        self._renderer.width = self.viewer.width()
        self._renderer.height = self.viewer.height()
        image = self._renderer.render(self._objects)
        self.viewer.image = image

    def _on_timer_tick(self):
        if self.settings.speed != 0:
            self._update_current_time()
        self._update_image()
        self._configurator.handle()

    def _update_current_time(self):
        now = datetime.datetime.now()
        seconds_passed = (now - self._last_tick_time).total_seconds()
        self._renderer.watcher.local_time = self._renderer.watcher.local_time + datetime.timedelta(0, seconds_passed * self.settings.speed)
        self._last_tick_time = now

    def _apply_constellation_filter(self, slctd):
        stars = self._sky_sphere.get_stars(slctd)
        self._objects = stars
        self._update_image()

    def keyPressEvent(self, e):
        if e.key() in self._key_commands:
            self._key_commands[e.key()]()

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()
