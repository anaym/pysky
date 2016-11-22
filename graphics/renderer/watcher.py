import datetime
from geometry.horizontal import Horizontal
from graphics.renderer.camera import Camera
from stars.star_time import StarTime


class Watcher(Camera):
    def __init__(self, position: Horizontal, local_time: datetime, camera: Camera):
        super().__init__(camera.see, camera.eye_radius)
        self._position = position
        self._local_time = local_time
        self._star_time = StarTime.from_local(position.a, local_time)

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
        self._position = Horizontal(value.a % 360, min(90, max(-90, value.h)))
        self._star_time = StarTime.from_local(self.position.a, self.local_time)

