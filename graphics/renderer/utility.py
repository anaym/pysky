from PyQt5.QtGui import QColor


def hexstr_to_color(s: str):
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:], 16)
    return QColor(r, g, b)