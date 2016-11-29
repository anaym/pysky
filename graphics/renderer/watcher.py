import datetime

from geometry.equatorial import Equatorial
from geometry.horizontal import Horizontal
from graphics.renderer.camera import Camera
from stars.star_time import StarTime


class Watcher(Camera):
    def __init__(self, position: Horizontal, local_time: datetime, camera: Camera):
        super().__init__(camera.see, camera.radius)
        self._position = position
        self._local_time = local_time
        self._star_time = StarTime.from_local(position.a, local_time)
        #self.position = position

    @property
    def local_time(self):
        return self._local_time

    @local_time.setter
    def local_time(self, value: datetime):
        self._local_time = value
        self._star_time = StarTime.from_local(self.position.a, self.local_time)

    @property
    def star_time(self) -> StarTime:
        return self._star_time

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Horizontal):
        self._position = value
        self.see = value
        self._star_time = StarTime.from_local(self.position.a, self.local_time)

    def to_horizontal(self, equ: Equatorial):
        return equ.to_horizontal_with_time(self.star_time.total_degree % 360, self.position.h)

