from geometry.equatorial import almost_equal, SecondEquatorial


class Star:
    POGSON_RATIO = 100**0.2

    def __init__(self, pos: SecondEquatorial, m, constellation, spectral_class='O'):
        self.position = pos
        self.m = m
        self.constellation = constellation
        self.spectral_class = spectral_class

    def __str__(self):
        return "alpha: {}, delta: {}, m: {}, constellation: {}, class: {}".format(
            self.alpha, self.delta, self.m, self.constellation, self.spectral_class
        )

    def __eq__(self, other):
        return self.position == other.position and self.m == other.m and self.constellation == other.constellation
