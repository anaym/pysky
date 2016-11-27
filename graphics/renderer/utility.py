from PyQt5.QtGui import QColor


def hexstr_to_color(s: str):
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:], 16)
    return QColor(r, g, b)


def try_or_print(foo):
    def decorated(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except Exception as e:
            print("Exception in {}({}; {}): {}".format(foo.__name__, e, args, kwargs))
            return None
    return decorated
