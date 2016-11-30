from requirements import Requirements

Requirements((3, 5, 1)).add("PyQt5", "PyQt5>=5.7").critical_check()

import os
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication
from graphics.autogui.action_item import ActionItem
from graphics.autogui.bool_item import BoolItem
from graphics.autogui.gui import GUI
from graphics.autogui.slide_item import SlideItem


class SoundPlayer(GUI):
    def __init__(self, name):
        mname = os.path.splitext(os.path.basename(name))[0]
        super().__init__("Sound player ({})".format(mname))
        self.player = player = QMediaPlayer()
        self.setGeometry(300, 300, 300, 220)
        self.show()
        self.setWindowTitle("Sound player")

        c = QMediaContent(QUrl.fromLocalFile(name))
        player.setMedia(c)
        player.setVolume(50)
        player.play()
        self.infinity = True
        self.add(ActionItem("pause", lambda: player.pause()))
        self.add(ActionItem("play", lambda: player.play()))
        self.add(SlideItem(self, "volume", 0, 100))
        self.add(SlideItem(self, "progress", 0, 1000))
        self.add(BoolItem(self, "infinity"))
        self.timer = QTimer()
        self.timer.timeout.connect(self.handle)
        self.timer.start(100)
        self.showMinimized()

    @property
    def volume(self):
        return self.player.volume()

    @volume.setter
    def volume(self, value):
        self.player.setVolume(value)

    @property
    def progress(self):
        if self.player.position() == self.player.duration() and self.infinity:
            self.player.setPosition(0)
            self.player.play()
        return 1000 * self.player.position() // self.player.duration()

    @progress.setter
    def progress(self, value):
        return self.player.setPosition(value * self.player.duration() / 1000)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError("File <> is not founded!")
    app = QApplication([])
    ex = SoundPlayer(sys.argv[1])
    app.exec()
