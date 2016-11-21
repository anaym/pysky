from geometry.avector import Equatorial


class Star:
    POGSON_RATIO = 100**0.2

    def __init__(self, pos: Equatorial, mass, constellation, spectral_class='O'):
        self.position = pos
        self.mass = mass
        self.constellation = constellation
        self.spectral_class = spectral_class

    def __str__(self):
        return "\{{}, mass={}, constellation={}, class={}\}".format(
            self.position, self.mass, self.constellation, self.spectral_class
        )

    def __eq__(self, other):
        return self.position == other.position and self.mass == other.m and self.constellation == other.constellation
