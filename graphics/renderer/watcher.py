import datetime
from geometry.avector import Horizontal
from graphics.renderer.camera import Camera
from stars.star_time import StarTime


class Watcher(Camera):
    def __init__(self, position: Horizontal, local_time: datetime, camera: Camera):
        super().__init__(camera.eye_radius, camera.sight_vector)
        self._position = position
        self._local_time = local_time
        self._star_time = StarTime.from_local(position.alpha, local_time)

    @property
    def local_time(self):
        return self._local_time

    @local_time.setter
    def local_time(self, value: datetime):
        self._local_time = value
        self._star_time = StarTime.from_local(self.position.alpha, self.local_time)

    @property
    def star_time(self) -> StarTime:
        return self._star_time

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Horizontal):
        self._position = Horizontal(value.alpha % 360, min(90, max(-90, value.delta)))
        self._star_time = StarTime.from_local(self.position.alpha, self.local_time)

