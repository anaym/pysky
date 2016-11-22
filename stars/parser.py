import re
from geometry.equatorial import Equatorial
from stars.sky_math import TimeHelper
from stars.skydatabase import SkyDataBase
from stars.star import Star

# TODO: change regexpes!!!
# TODO: rename static methods!!!
# TODO: make refactoring
# TODO: разобраться с еденицами изменрения при парсинге!!!! (ГРАДУСЫ/ЧАСЫ)

# Alf: [0; 23] : [0; 59] : [0; 59]
# Del: [-90; 90] : [0; 59] : [0; 59]
def num_regexp(name: str):
    return r"(?P<{}>[\+-]? *?[\d\.]+)".format(name)


def any_num_regexp(separator: str, name: str, count: int):
    tmp = ""
    for i in range(0, count - 1):
        tmp += num_regexp(name + '_' + str(i)) + "{} ?".format(separator)
    tmp += num_regexp(name + '_' + str(count - 1))
    return tmp


def extract_nums(parsed, name: str, count: int):
    nums = []
    for i in range(0, count):
        nm = name + '_' + str(i)
        if nm in parsed:
            nums.append(float(parsed[nm].replace(' ', '')))
        else:
            raise ValueError()
    return nums


class TxtDataBaseParser:
    def __init__(self):
        map_re = r"^ *?{} *?".format(num_regexp("map"))
        pos_re = any_num_regexp(':', 'alf', 3) + ' ' + any_num_regexp(':', 'del', 3)
        self._regex = re.compile(map_re + pos_re)

    def parse(self, line_const_tuples):
        stars = [i for i in (self.parse_star(t) for t in line_const_tuples) if i is not None]
        return SkyDataBase(stars)

    def parse_star(self, pair) -> Star:
        try:
            parsed = self._regex.match(pair[0]).groupdict()
            a_h, a_m, a_s = extract_nums(parsed, 'alf', 3)
            d_d, d_m, d_s = extract_nums(parsed, 'del', 3)
            a = TimeHelper.time_to_degree(a_h, a_m, a_s)
            d = TimeHelper.time_to_degree(0, d_m, d_s) + d_d #TODO: WTF??? это минуты градуса или ромто минуты?
            return Star(Equatorial(a, d), pair[1])
        except Exception as ex:
            print(ex)
