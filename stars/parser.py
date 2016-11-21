import re
import os

from geometry.avector import Equatorial
from stars.star import Star

# TODO: change regexpes!!!
# TODO: rename static methods!!!
# TODO: make refactoring


class TxtDataBaseParser:
    def __init__(self):
        regex_str_beginning = r" *?\w+ *?"
        regex_str_alpha = r"(?P<a_hours>\d+): ?(?P<a_minutes>\d+): ?(?P<a_seconds>\d+\.\d+)"
        regex_str_alpha_to_delta = r" "
        regex_str_delta = r"(?P<d_degrees>[\+-] ?\d+): ?(?P<d_minutes>\d+): ?(?P<d_seconds>\d+)"
        regex_str_delta_to_m = r" *?\d+\.\d+ *?-? ?\d+\.\d+.*?"
        regex_str_m = r"(?P<mass>\d+\.\d+)"
        regex_str_class=r".*?(?P<class>[OBAFGKM])"

        regex_str = regex_str_beginning + regex_str_alpha + regex_str_alpha_to_delta + regex_str_delta + regex_str_delta_to_m + regex_str_m + regex_str_class
        self._regex = re.compile(regex_str)

    def parse_dir(self, dirname: str):
        stars = []
        for filename in os.listdir(dirname):
            if filename.endswith('.txt'):
                stars += self.parse_file(os.path.join(dirname, filename), filename.split('.')[0])
        return stars

    def parse_file(self, filename: str, constellation: str) -> list:
        with open(filename, 'r') as file:
            stars = []
            for line in file.readlines():
                star = self.parse_star(line, constellation)
                if star is not None:
                    stars.append(star)
            return stars

    def parse_star(self, line: str, constellation: str) -> Star:
        match = self._regex.match(line)
        if match is None:
            return None
        alpha = self._parse_alpha(match)
        delta = self._parse_delta(match)
        m = self._parse_m(match)
        spectral_class = self._parse_class(match)
        return Star(Equatorial(alpha, delta), m, constellation, spectral_class)

    @staticmethod
    def _parse_alpha(match):
        hours = match.group('a_hours')
        minutes = match.group('a_minutes')
        seconds = match.group('a_seconds')
        return (float(hours) + float(minutes) / 60 + float(seconds) / 3600) * 15

    @staticmethod
    def _parse_delta(match):
        degrees = match.group('d_degrees')
        degrees = degrees.replace(' ', '')
        minutes = match.group('d_minutes')
        seconds = match.group('d_seconds')
        return float(degrees) + float(minutes) / 60 + float(seconds) / 3600

    @staticmethod
    def _parse_m(match):
        m = match.group('mass')
        return float(m)

    @staticmethod
    def _parse_class(match):
        spectral_class = match.group('class')
        return spectral_class
