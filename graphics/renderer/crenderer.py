import datetime
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton

from geometry.avector import Horizontal
from graphics.renderer.camera import Camera
from graphics.renderer.renderer import Canvas
from graphics.renderer.settings import ControllableRenderSettings
from graphics.renderer.ui import create_float_widget, create_datetime_widget, create_bool_widget
from stars.skybase import SkyBase


class ControllableRenderer(QtWidgets.QWidget):
    def __init__(self, camera: Camera, sky_sphere: SkyBase, start_time: datetime.datetime):
        super().__init__()

        self._canvas = Canvas(camera, start_time)
        self._sky_sphere = sky_sphere
        self.settings = ControllableRenderSettings()
        self._magnitude_lower_th = 6
        self._magnitude_upper_th = 0
        self._datetime_format = "%d.%m.%Y %H:%M:%S"
        self._key_commands = {
            QtCore.Qt.Key_A: lambda: self._change_sight_vector(1, 0),
            QtCore.Qt.Key_D: lambda: self._change_sight_vector(-1, 0),
            QtCore.Qt.Key_W: lambda: self._change_sight_vector(0, 1),
            QtCore.Qt.Key_S: lambda: self._change_sight_vector(0, -1),

            QtCore.Qt.Key_Q: lambda: self._change_sight_vector(0, 0, 10),
            QtCore.Qt.Key_E: lambda: self._change_sight_vector(0, 0, -10),

            QtCore.Qt.Key_Equal: lambda: self._change_zoom(1.5),
            QtCore.Qt.Key_Minus: lambda: self._change_zoom(2 / 3)
        }

        self._timer = QtCore.QTimer(self)
        self._timer.setInterval(1000 / self.settings.fps)
        self._timer.timeout.connect(self._on_timer_tick)

        self._constellations = sky_sphere.constellations

        self._cmodel = QStandardItemModel()
        self._init_ui()
        self.setFocus()

        self._last_tick_time = datetime.datetime.now()
        self._apply_constellation_filter()
        self._on_timer_tick()
        self._timer.start()

    def _create_constellations(self):
        model = QStandardItemModel()
        for const in sorted(self._constellations):
            item = QStandardItem(const)
            item.setCheckState(False)
            item.setCheckable(True)
            model.appendRow(item)

        view = QListView()
        view.setModel(model)
        self._cmodel = model
        view.clicked.connect(lambda: self._apply_constellation_filter())
        return view

    def _init_ui(self):
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self._canvas, 0, 0)
        layout.setColumnStretch(0, 1)

        tools_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(tools_layout, 0, 1)

        time_zone = QtWidgets.QGridLayout()
        tools_layout.addLayout(time_zone)

        consw = create_bool_widget("fisheye", self._canvas.settings, "fisheye")
        time_zone.addWidget(consw)
        self._datetime_widget = create_datetime_widget(self._canvas, "datetime", self._datetime_format)
        time_zone.addWidget(self._datetime_widget)

        self._speed_widget = create_float_widget(self.settings, "speed")
        time_zone.addWidget(self._speed_widget)

        constellation_zone = QtWidgets.QHBoxLayout()
        tools_layout.addLayout(constellation_zone)

        self._constellation_widget = self._create_constellations()
        tools_layout.addWidget(self._constellation_widget)
        bclear = QPushButton("none")
        bclear.clicked.connect(lambda: self._set_all_cmodel(0))
        tools_layout.addWidget(bclear)
        ball = QPushButton("all")
        ball.clicked.connect(lambda: self._set_all_cmodel(2))
        tools_layout.addWidget(ball)

        camera_layout = QtWidgets.QGridLayout()
        tools_layout.addLayout(camera_layout)

        camera_layout.addWidget(QtWidgets.QLabel('long:'), 0, 0)
        self._longitude_widget = create_float_widget(self._canvas.camera, "longitude")
        camera_layout.addWidget(self._longitude_widget, 0, 1)

        camera_layout.addWidget(QtWidgets.QLabel('lat:'), 1, 0)
        self._latitude_widget = create_float_widget(self._canvas.camera, "latitude")
        camera_layout.addWidget(self._latitude_widget, 1, 1)

        camera_layout.addWidget(QtWidgets.QLabel('radius:'), 2, 0)
        self._zoom_widget = QtWidgets.QLineEdit(str(self._canvas.camera.sight_radius))
        self._zoom_widget.editingFinished.connect(
            lambda: self._change_zoom(
                self._canvas.camera.sight_radius / float(self._zoom_widget.text())
            )
        )

        camera_layout.addWidget(self._zoom_widget, 2, 1)
        camera_layout.addWidget(QtWidgets.QLabel('angle:'), 3, 0)
        self._sight_vector_azimuth = QtWidgets.QLineEdit(str(self._canvas.camera.sight_vector.alpha))
        self._sight_vector_azimuth.editingFinished.connect(
            lambda: self._set_sight_vector(
                float(self._sight_vector_azimuth.text()),
                self._canvas.camera.sight_vector.delta
            )
        )
        camera_layout.addWidget(self._sight_vector_azimuth, 3, 1)

        camera_layout.addWidget(QtWidgets.QLabel('delta:'), 4, 0)
        self._sight_vector_altitude = QtWidgets.QLineEdit(str(self._canvas.camera.sight_vector.delta))
        self._sight_vector_altitude.editingFinished.connect(
            lambda: self._set_sight_vector(
                self._canvas.camera.sight_vector.alpha,
                float(self._sight_vector_altitude.text())
            )
        )
        camera_layout.addWidget(self._sight_vector_altitude, 4, 1)

        camera_layout.addWidget(QtWidgets.QLabel('up_rotation:'), 5, 0)
        self._rot_wid = create_float_widget(self._canvas.camera, "up_rotation")
        camera_layout.addWidget(self._rot_wid, 5, 1)

        tools_layout.addWidget(QtWidgets.QWidget())
        tools_layout.setStretch(7, 1)

    def _set_all_cmodel(self, value):
        for i in range(0, self._cmodel.rowCount()):
            self._cmodel.item(i, 0).setCheckState(value)
        self._apply_constellation_filter()

    def _change_zoom(self, d_zoom):
        d_zoom = max(d_zoom, self._canvas.camera.sight_radius / 90)
        self.settings.zoom = self.settings.zoom* d_zoom
        self._canvas.camera.sight_radius = self._canvas.camera.sight_radius / d_zoom
        self._zoom_widget.setText(str(self._canvas.camera.sight_radius))
        self.setFocus()

    def _change_sight_vector(self, da=0, dd=0, dr=0):
        self._canvas.camera.sight_vector += Horizontal(da, dd)
        self._canvas.camera.up_rotation += dr
        self.setFocus()
        self._rot_wid.setText(str(self._canvas.camera.up_rotation))

    def _on_timer_tick(self):
        if self.settings.speed != 0:
            self._update_current_time()
        self._canvas.repaint()

    def _update_current_time(self):
        now = datetime.datetime.now()
        seconds_passed = (now - self._last_tick_time).total_seconds()
        self._canvas.datetime += datetime.timedelta(0, seconds_passed * self.settings.speed)
        self._last_tick_time = now
        self._datetime_widget.setText(self._canvas.datetime.strftime(self._datetime_format))

    def _apply_constellation_filter(self):
        selected = set()
        for i in range(0, self._cmodel.rowCount()):
            if self._cmodel.item(i, 0).checkState() != 0:
                selected.add(self._cmodel.item(i, 0).text())
        stars = self._sky_sphere.get_stars(selected)
        self._canvas.objects = stars
        self._canvas.repaint()

    def keyPressEvent(self, e):
        if e.key() in self._key_commands:
            self._key_commands[e.key()]()

    def mousePressEvent(self, QMouseEvent):
        self.setFocus()




