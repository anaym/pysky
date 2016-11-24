from datetime import datetime
from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, DateTimeItem, IntItem
from graphics.autogui.gui import GUI
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.items.horizontal_item import HorizontalItem
from graphics.sky_viewers.sky import Sky
from stars.skydatabase import SkyDataBase


class ControllableSky(Sky):
    def __init__(self, watcher: Watcher, sky_base: SkyDataBase):
        super().__init__(watcher, sky_base)

        gui = GUI("CONFIGURATOR")

        camera = gui.add(GUI("CAMERA"))
        camera.add(HorizontalItem(self._renderer.watcher, "position", label="(долгота, широта)"))
        camera.add(HorizontalItem(self._renderer.watcher, "see"))
        camera.add(FloatItem(self._renderer.watcher, "up_rotation"))

        time = gui.add(GUI("DATE & TIME"))
        time.add(DateTimeItem(self._renderer.watcher, "local_time"))
        time.add(FloatItem(self._renderer.watcher, "star_time", True))
        time.add(FloatItem(self.settings, "second_per_second"))
        time.add(FloatItem(self.settings, "speed_rank"))
        time.add(IntItem(self, "delay"))

        view = gui.add(GUI("VIEW"))
        view.add(BoolItem(self._renderer.settings, "fisheye"))
        view.add(BoolItem(self._renderer.settings, "spectral"))
        view.add(BoolItem(self._renderer.settings, "magnitude"))
        view.add(FloatItem(self._renderer.settings, "exp_factor"))
        view.add(FloatItem(self._renderer.settings, "exp_const"))
        view.add(FloatItem(self._renderer.settings, "pull"))
        view.add(BoolItem(self._renderer.settings, "up_direction"))
        view.add(BoolItem(self._renderer.settings, "see_direction"))

        gui.add(ActionItem("Save image", lambda: self.viewer.image.save("sky.jpg")))
        gui.add(ActionItem("Pause", self._switch_pause))
        gui.add(ActionItem("Current time", self._current_time))

        self._configurator_widget = gui
        self._main.addWidget(self._configurator_widget, 0, 2)
        self._gui = gui
        self._timer.timeout.connect(self._gui_tick)

    def _current_time(self):
        self._renderer.watcher.local_time = datetime.now()

    def _gui_tick(self):
        try:
            self._gui.handle()
        except Exception as e:
            print(e)

    def _apply_constellation_filter(self, selected):
        self.filter.constellations = selected

    def _switch_pause(self):
        if self.settings.speed_rank != 0:
            self._ssr = self.settings.speed_rank
            self.settings.speed_rank = 0
        else:
            self.settings.speed_rank = self._ssr
