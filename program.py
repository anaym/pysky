import datetime
import os
import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QSound

from geometry.horizontal import Horizontal
from graphics.renderer.camera import Camera
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.key_controllable_sky import KeyControllableSky
from graphics.sky_viewers.mouse_controllable_sky import MouseControllableSky
from graphics.sky_viewers.named_sky import NamedSky
from stars.parser import TxtDataBaseParser
#import vlc
import sys

def get_all_files_in_dir(path: str, ext: str):
    for fn in os.listdir(path):
        if fn.endswith(ext):
            yield (os.path.join(path, fn), fn.split('.')[0])


def get_all_lines_in_dir(path: str, ext: str):
    for p, fn in get_all_files_in_dir(path, ext):
        with open(p, 'r') as file:
            for line in file:
                yield (line, fn)


class City(Horizontal):
    def __init__(self, широта, долгота):
        super().__init__(долгота, широта)


MAGNITOGORSK = City(53, 59)
YEKATERINBURG = City(56, 60)


# TODO: renderer --> 2D plane (points) --> image raenderer --> image


def main():
    sky_base = TxtDataBaseParser().parse(get_all_lines_in_dir(r'stars\stars\txt', '.txt'))
    camera = Camera(Horizontal(0, 90), 60)
    watcher = Watcher(MAGNITOGORSK, datetime.datetime.now(), camera)

    app = QtWidgets.QApplication([])
    NamedSky(watcher, sky_base)
    #p = subprocess.Popen([sys.executable, "music.py"])
    app.exec()
    #p.kill()

if __name__ == '__main__':
    main()
