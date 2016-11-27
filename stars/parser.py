import re
from geometry.angle_helpers import dtime_to_degree, time_to_degree
from geometry.equatorial import Equatorial
from stars.latin import EN2LAT_MAP
from stars.skydatabase import SkyDataBase
from stars.star import Star, SPECTRAL_CLASSES


def num_regexp(name: str):
    return r"(?P<{}>[\+-]? *?[\d\.]+)".format(name)


def any_num_regexp(separator: str, name: str, count: int):
    tmp = ""
    for i in range(0, count - 1):
        tmp += num_regexp(name + '_' + str(i)) + "{} *?".format(separator)
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


SPECTRAL_CLASSES_SET = str.join('', SPECTRAL_CLASSES)


# Alf: [0; 23] : [0; 59] : [0; 59] - time : hours : minutes : seconds
# Del: [-90; 90] : [0; 59] : [0; 59] - degree : degree minutes : degree seconds


class TxtDataBaseParser:
    def __init__(self):
        map_re = r"^ *?{} *?".format(num_regexp("map"))
        pos_re = any_num_regexp(':', 'alf', 3) + ' ' + any_num_regexp(':', 'del', 3)
        sp0_re = " +?" + any_num_regexp(' ', 'trash0', 2) + r' *?\w*? *?'
        mag_re = num_regexp("mag")
        cls_re = ' +?[a-z:]*?' + '(?P<cls>[A-Z]).*? +?'
        sp1_re = any_num_regexp(' ', 'trash1', 2) + '...' + any_num_regexp(' ', 'trash2', 3)
        nam_re = r' +?\d*?(?P<name>[a-zA-Z]*?)? *?\d*? *?(\(.*?\))?$'
        self._regex = re.compile(map_re + pos_re + sp0_re + mag_re + cls_re + sp1_re + nam_re)

    def parse(self, line_const_tuples):
        stars = [s for s in (self.parse_star(t) for t in line_const_tuples) if s is not None]
        return SkyDataBase(stars)

    def parse_star(self, pair) -> Star:
        try:
            parsed = self._regex.match(pair[0].replace('\n', '')).groupdict()
            a_h, a_m, a_s = extract_nums(parsed, 'alf', 3)
            d_d, d_m, d_s = extract_nums(parsed, 'del', 3)
            a = time_to_degree(a_h, a_m, a_s)
            d = dtime_to_degree(d_d, d_m, d_s)
            cls = parsed['cls'] if parsed['cls'] in SPECTRAL_CLASSES else ''
            name = parsed['name']
            if name is None:
                name = ''
            if name[0:3] in EN2LAT_MAP:
                name = EN2LAT_MAP[name]
            return Star(Equatorial(a, d), pair[1], float(parsed['mag']), cls, name)
        except Exception as ex:
            print('Can`t parse line ({}) in {}'.format(*pair))
