class Horizontal:
    def __init__(self, a, d):
        self._a = a
        self._d = d

    @property
    def a(self):
        return self._a

    @property
    def d(self):
        return self._d

    def __str__(self):
        return "({}, {})".format(self.a, self.d)

    def __eq__(self, other):
        return self.a == other.a and self.d == other.d
