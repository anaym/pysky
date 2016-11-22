from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.field_item import FloatItem, DateTimeItem
from graphics.autogui.gui import GUI
from graphics.autogui.set_item import CheckBoxSet
from graphics.horizontal_item import HorizontalItem
from graphics.renderer.watcher import Watcher


class Configurator(GUI):
    def __init__(self, watcher: Watcher, settings, render_settings, constellations):
        super().__init__("CONFIGURATOR")
        self.constellationsChangedHandler = lambda s: s
        self.imageSaveRequestedHandler = lambda: 0
        self.switchPauseRequestedHandler = lambda: 0

        camera = self.add(GUI("CAMERA"))

        camera.add(HorizontalItem(watcher, "position"))
        camera.add(HorizontalItem(watcher, "see"))
        camera.add(FloatItem(watcher, "up_rotation"))

        time = self.add(GUI("DATE & TIME"))
        time.add(DateTimeItem(watcher, "local_time"))
        time.add(FloatItem(settings, "speed"))
        time.add(FloatItem(settings, "speed_rank"))

        other = self.add(GUI("OTHER"))
        other.add(BoolItem(render_settings, "fisheye"))
        self.constellation_filter = other.add(CheckBoxSet(sorted(constellations), lambda s: self.constellationsChangedHandler(s)))

        self.add(ActionItem("Save image", lambda: self.imageSaveRequestedHandler()))
        self.add(ActionItem("Pause", lambda: self.switchPauseRequestedHandler()))
