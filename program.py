import datetime
import os
from PyQt5 import QtWidgets
from geometry.horizontal import Horizontal
from graphics.qt_stars import QtStars
from graphics.renderer.camera import Camera
from graphics.renderer.watcher import Watcher
from stars.parser import TxtDataBaseParser


def get_all_files_in_dir(path: str, ext: str):
    for fn in os.listdir(path):
        if fn.endswith(ext):
            yield (os.path.join(path, fn), fn.split('.')[0])


def get_all_lines_in_dir(path: str, ext: str):
    for p, fn in get_all_files_in_dir(path, ext):
        with open(p, 'r') as file:
            for line in file:
                yield (line, fn)


def main():
    sky_base = TxtDataBaseParser().parse(get_all_lines_in_dir(r'stars\stars\txt', '.txt'))
    camera = Camera(Horizontal(0, 89), 60)
    watcher = Watcher(Horizontal(59, 53), datetime.datetime.now(), camera)

    app = QtWidgets.QApplication([])
    QtStars(watcher, sky_base).show()
    app.exec()

if __name__ == '__main__':
    main()
