from requirements import Requirements
Requirements((3, 5, 1)).add("PyQt5", "PyQt5>=5.7").add("jdcal", "jdcal>=1.3").critical_check()


import os
import subprocess
from argparse import ArgumentParser
from os.path import join
import datetime
import sys
from PyQt5 import QtWidgets
from geometry.horizontal import Horizontal
from graphics.renderer.camera import Camera
from graphics.renderer.renderer import Renderer
from graphics.renderer.settings import Settings
from graphics.renderer.watcher import Watcher
from graphics.sky_viewers.named_sky import NamedSky
from stars.filter import Filter, Range
from stars.parser import TxtDataBaseParser
from stars.skydatabase import SkyDataBase


class City(Horizontal):
    def __init__(self, широта, долгота):
        super().__init__(долгота, широта)


BUILTIN_CITIES = {"MGN": City(53, 59), "EKB": City(56, 60)}

parser = ArgumentParser(
    description="Sky visualizer",
    epilog="Developed by Anton Tolstov (aka Anaym): atolstov.com"
)

parser.add_argument('-c', '--console', action='store_true', help="don`t use gui for visualization")
parser.add_argument('-m', '--music', action='store_true', help="enable music")
parser.add_argument('-b', '--base', type=str, metavar='PATH', default=join('stars', 'stars', 'txt'),
                    help="path to star date base")
parser.add_argument('-o', '--out', type=str, metavar='PATH', default='stars when %d.%m.%Y %H_%M_%S.jpg',
                    help="name of resulted image (you can use datetime mask)")

parser.add_argument('-d', type=str, metavar='DATETIME', default=None, help="datetime for rendering (use d.m.Y H:M:S)")
parser.add_argument('-p', type=float, nargs=2, metavar=('LONG', 'LAT'), default=(53, 59), help="position of watcher")
parser.add_argument('-s', type=float, nargs=2, metavar=('A', 'H'), default=(59, 53),
                    help="see direction (in horizontal)")

parser.add_argument('--see-up', action='store_true', help="see always up")
parser.add_argument('--city', choices=BUILTIN_CITIES.keys(), default=None, help="builtins cities")

parser.add_argument('--fisheye', type=bool, metavar="", default=True, help="enable fisheye distortion?")
parser.add_argument('--spectral', type=bool, metavar="", default=True, help="enable spectral depended star color?")
parser.add_argument('--magnitude', type=bool, metavar="", default=True,
                    help="enable magnitude depended star size transformation?")
parser.add_argument('--disable-effects', action='store_true', help="disable all visual effects")

parser.add_argument('--see-points', type=bool, metavar="", default=True, help="show see critical points(0, +-90)?")
parser.add_argument('--centre-direction', type=bool, metavar="", default=True, help="show centre direction?")
parser.add_argument('--compass', type=bool, metavar="", default=True, help="show compass?")
parser.add_argument('--disable-points', action='store_true', help="disable all points")

parser.add_argument('--magnitude-range', type=float, nargs=2, metavar=('MIN', 'MAX'), default=(-1, 10),
                    help='Magnitude filter for stars')
parser.add_argument('--constellations', type=str, nargs='*', metavar='NAME', default=None,
                    help='Constellations filter for stars')


def get_all_files_in_dir(path: str, ext: str):
    for fn in os.listdir(path):
        if fn.endswith(ext):
            yield (os.path.join(path, fn), fn.split('.')[0])


def get_all_lines_in_dir(path: str, ext: str):
    for p, fn in get_all_files_in_dir(path, ext):
        with open(p, 'r') as file:
            for line in file:
                yield (line, fn)


def gui_mode(database, filter, render_settings, watcher: Watcher, out_file_name, music_mode: bool):
    app = QtWidgets.QApplication([])
    sky = NamedSky(watcher, database, filter)
    sky.renderer.settings = render_settings
    sky.viewer.out_file_name = out_file_name
    if music_mode:
        p = subprocess.Popen([sys.executable, "sound.py", join("resources", "Still Alive.mp3")])
        app.exec()
        p.kill()
    else:
        app.exec()


def console_mode(database: SkyDataBase, filter, render_settings, watcher: Watcher, out_file_name):
    renderer = Renderer(watcher)
    renderer.settings = render_settings
    image = renderer.render(database.get_stars(filter), False)
    fname = watcher.local_time.strftime(out_file_name)
    image.save(fname)
    print("Image has been successful saved to {}".format(fname))


def extract_time(string):
    full_year = ["%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M", "%d.%m.%Y %H", "%d.%m.%Y"]
    short_year = ["%d.%m.%y %H:%M:%S", "%d.%m.%y %H:%M", "%d.%m.%y %H", "%d.%m.%y"]
    time = ["%H:%M:%S", "%H:%M", "%H"]
    for f in full_year + short_year + time:
        try:
            dt = datetime.datetime.strptime(string, f)
            if f in time:
                n = datetime.datetime.now()
                dt = datetime.datetime(n.year, n.month, n.day, dt.hour, dt.minute, dt.second)
            return dt
        except:
            pass
    return None

if __name__ == '__main__':
    task = parser.parse_args()
    dt = extract_time(task.d)
    if dt is None:
        if task.d is not None:
            print('Bad datetime!')
            sys.exit(1)
        else:
            dt = datetime.datetime.now()
    database = TxtDataBaseParser().parse(get_all_lines_in_dir(task.base, '.txt'))

    r = rset = Settings()
    if not task.disable_effects:
        r.fisheye, r.spectral, r.magnitude, = task.fisheye, task.spectral, task.magnitude
    else:
        r.fisheye, r.spectral, r.magnitude = False, False, False

    if not task.disable_points:
        r.see_points, r.screen_centre, r.compass = task.see_points, task.centre_direction, task.compass
    else:
        r.see_points, r.screen_centre, r.compass = False, False, False

    pos = BUILTIN_CITIES[task.city] if task.city else Horizontal(task.p[1], task.p[0])
    see = pos if task.see_up else Horizontal(*task.s)
    camera = Camera(see, 60)
    watcher = Watcher(pos, dt, camera)

    consts = task.constellations if task.constellations else database.constellations
    range = Range(min(*task.magnitude_range), max(*task.magnitude_range))
    filter = Filter(consts, range)

    if task.console:
        console_mode(database, filter, rset, watcher, task.out)
    else:
        gui_mode(database, filter, rset, watcher, task.out, task.music)
