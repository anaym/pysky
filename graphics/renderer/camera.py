import datetime
from geometry.equatorial import Horizontal


class Camera:
    def __init__(self, longitude, latitude, sight_radius, sight_vector: Horizontal):
        if latitude == 90 or latitude == -90:
            latitude += 1e-9
        self.sight_radius = sight_radius
        self._sight_vector = Horizontal(sight_vector.alpha, sight_vector.delta)
        if sight_vector.delta == 90 or sight_vector.delta == -90:
            sight_vector.delta += 1e-9
        self._longitude = longitude
        self._latitude = latitude
        self._up_rotation = 0
        self._up_vector = Horizontal(0, 0)

    def _update(self):
        self._up_vector = None

    # TODO: move to new class Observer
    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = min(90, max(-90, latitude))

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude % 360

    def sight_radius(self):
        return self._sight_radius

    def set_sight_radius(self, radius):
        self._sight_radius = radius

    def get_sight_vector(self):
        return self._sight_vector

    @property
    def up_vector(self) -> Horizontal:
        return Horizontal(self._sight_vector.alpha, self._sight_vector.delta - 90)

    #TODO: make vector immutable
    def change_sight_vector(self, d_alpha, d_delta):
        self.set_sight_vector_azimuth(self._sight_vector.alpha + d_alpha)
        self.set_sight_vector_altitude(self._sight_vector.delta + d_delta)

    def set_sight_vector_azimuth(self, azimuth):
        self._sight_vector.alpha = azimuth % 360

    def set_sight_vector_altitude(self, altitude):
        self._sight_vector.delta = min(max(altitude, -90 + 1e-9), 90 - 1e-9)

    def get_lst(self, date_time: datetime.datetime):
        d = self.get_julian_day(date_time)
        t = d / 36525
        hours = (280.46061837 + 360.98564736629 * d + 0.000388 * (t**2) + self._longitude) % 360 / 15
        return hours

    def get_julian_day(self, date_time: datetime.datetime):
        dwhole = (
            367 * date_time.year -
            int(7 * (date_time.year + int((date_time.month + 9) / 12)) / 4) +
            int(275 * date_time.month / 9) +
            date_time.day - 730531.5
        )
        dfrac = (date_time.hour + date_time.minute/60 + date_time.second / 3600) / 24
        return dwhole + dfrac
