from math import cos, sin

import datetime


class FirstEquatorialToHorizontal:
    '''https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%B8%D0%B7%D0%BE%D0%BD%D1%82%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D0%BA%D0%BE%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B0%D1%82'''

    @staticmethod
    def cosz(f, d, t):
        return sin(f)*sin(d) + cos(d)*cos(f)*cos(t)

    @staticmethod
    def siza_sinz(d, t):
        return cos(d)*sin(t)

    @staticmethod
    def cosa_sinz(f, d, t):
        return -cos(f)*sin(d) + sin(f)*cos(d)*cos(t)


class StarTimeHelper:
    @staticmethod
    def get_star_hour(longitude, date_time: datetime.datetime):
        d = StarTimeHelper.get_julian_day(date_time)
        t = d / 36525
        hours = (280.46061837 + 360.98564736629 * d + 0.000388 * (t**2) + longitude) / 15
        return hours

    @staticmethod
    def get_julian_day(date_time: datetime.datetime):
        dwhole = (
            367 * date_time.year -
            int(7 * (date_time.year + int((date_time.month + 9) / 12)) / 4) +
            int(275 * date_time.month / 9) +
            date_time.day - 730531.5
        )
        dfrac = (date_time.hour + date_time.minute/60 + date_time.second / 3600) / 24
        return dwhole + dfrac


class StarTime:
    @staticmethod
    def from_local(longitude: float, local: datetime):
        return StarTime(StarTimeHelper.get_star_hour(longitude, local))

    def __init__(self, hours: int):
        self._hours = hours

    @property
    def total_hours(self):
        return self._hours

    @property
    def total_minutes(self):
        return self.total_hours * 60

    @property
    def total_seconds(self):
        return self.total_minutes * 60

    @property
    def total_degree(self):
        return self.total_hours * 15
