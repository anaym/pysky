from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, DateTimeItem, IntItem
from graphics.autogui.gui import GUI
from graphics.autogui.set_item import CheckBoxSet
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.items.filter_item import FilterItem
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

        other = gui.add(GUI("OTHER"))
        other.add(BoolItem(self._renderer.settings, "fisheye"))
        other.add(BoolItem(self._renderer.settings, "spectral"))
        other.add(BoolItem(self._renderer.settings, "magnitude"))
        #self._constellation_filter = other.add(CheckBoxSet(sorted(self._available_constellations), self._apply_constellation_filter))
        #other.add(FilterItem(self.filter, self._available_constellations, self._apply_constellation_filter))

        gui.add(ActionItem("Save image", lambda: self.viewer.image.save("sky.jpg")))
        gui.add(ActionItem("Pause", self._switch_pause))

        self._configurator_widget = gui.to_widget()
        self._main.addWidget(self._configurator_widget, 0, 2)
        self._gui = gui
        self._timer.timeout.connect(self._gui_tick)

        #selected = self._constellation_filter.selected
        #self._apply_constellation_filter(selected)

    def _gui_tick(self):
        try:
            self._gui.handle()
        except Exception as e:
            print(e)

    def _apply_constellation_filter(self, selected):
        self.filter.constellations = selected
        #stars = self._sky_sphere.get_stars(selected)
        #self._objects = stars
        #self._update_image()
        pass

    def _switch_pause(self):
        if self.settings.speed_rank != 0:
            self._ssr = self.settings.speed_rank
            self.settings.speed_rank = 0
        else:
            self.settings.speed_rank = self._ssr
