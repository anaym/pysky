from PyQt5 import QtWidgets

from graphics.crenderer import ControllableRenderer
from graphics.renderer.watcher import Watcher
from stars.skybase import SkyBase


class StarsWindow(QtWidgets.QMainWindow):
    """Главное окно приложения"""
    def __init__(self, watcher: Watcher, sky_sphere: SkyBase):
        super().__init__()

        self.resize(700, 700)
        self._sky_watch = ControllableRenderer(watcher, sky_sphere)
        self._init_ui()
        self._sky_watch.setFocus()

    def _init_ui(self):
        panel = QtWidgets.QWidget()
        self.setCentralWidget(panel)

        layout = QtWidgets.QGridLayout()
        panel.setLayout(layout)
        layout.addWidget(self._sky_watch, 0, 0)

        self.setWindowTitle("Sky")
        self.show()
