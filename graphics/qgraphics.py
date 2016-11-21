import datetime

from PyQt5 import QtWidgets

from graphics.renderer.camera import Camera
from graphics.renderer.crenderer import ControllableRenderer
from stars.skybase import SkySphere


class StarsWindow(QtWidgets.QMainWindow):
    """Главное окно приложения"""
    def __init__(self, observer: Camera, sky_sphere: SkySphere, start_time: datetime.datetime):
        super().__init__()

        self.resize(700, 700)
        self._sky_watch = ControllableRenderer(observer, sky_sphere, start_time)
        self._init_ui()
        self._sky_watch.setFocus()


    def _init_ui(self):
        panel = QtWidgets.QWidget()
        self.setCentralWidget(panel)

        layout = QtWidgets.QGridLayout()
        panel.setLayout(layout)
        layout.addWidget(self._sky_watch, 0, 0)

        self.setWindowTitle("Stars")
        self.show()
