from math import sqrt


class VectorBase:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __len__(self):
        return self.length

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    def __eq__(self, other):
        try:
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
        except:
            return False

