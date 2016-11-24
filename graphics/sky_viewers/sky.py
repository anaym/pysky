import datetime
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from graphics.autogui.cast_tools import to_widget
from graphics.renderer.projector import Projector
from graphics.renderer.renderer import Renderer
from graphics.renderer.settings import ControllableSkySettings
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.image_viewer import ImageViewer
from graphics.sky_viewers.utility import profile
from stars.filter import Filter, Range
from stars.skydatabase import SkyDataBase


class Sky(QMainWindow):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):
        super().__init__()
        self._renderer = Renderer(watcher)
        self.settings = ControllableSkySettings()

        self._available_constellations = sky_base.constellations
        self._objects = []
        self._sky_sphere = sky_base
        self.filter = Filter(sky_base.constellations, Range(-1, 10))

        self._create_ui()
        self.setFocus()

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._rerender)
        self._timer.setInterval(33)
        self._rerender()
        self._timer.start()

        self.setMouseTracking(True)

        self.setVisible(True)

    def _create_ui(self):
        main = QtWidgets.QGridLayout()
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        self.viewer = ImageViewer()
        main.addWidget(self.viewer, 0, 0)

        self._filter_widget = QWidget()
        main.addWidget(self._filter_widget, 0, 1)
        self._filter_widget.setVisible(False)

        self._configurator_widget = QWidget()
        main.addWidget(self._configurator_widget, 0, 2)

        main.setColumnStretch(0, 2)
        self._main = main

        self.setWindowTitle("Sky: Powered by Anton Tolstov (aka anaym), atolstov.com, 2016")
        self.resize(1000, 700)
        self.setCentralWidget(to_widget(main))
        self.show()

    def _update_image(self):
        self._renderer.width = self.viewer.width()
        self._renderer.height = self.viewer.height()
        image = self._renderer.render(self._sky_sphere.get_stars(self.filter))
        self.viewer.image = image

    @profile
    def _rerender(self, exec_delta: datetime.timedelta):
        if exec_delta is None:
            return
        self._renderer.watcher.local_time += exec_delta*self.settings.second_per_second
        self._update_image()

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()

    @property
    def delay(self):
        return self._timer.interval()

    @delay.setter
    def delay(self, value):
        self._timer.setInterval(value)
