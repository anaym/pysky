from math import sqrt, acos

import numpy


class Vector:
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
        return sqrt(self.scalar_mul(self))

    def angle_to(self, other):
        d = other - self
        if self.length == 0 or other.length == 0:
            return 0
        return acos((self.length**2 + other.length**2 - d.length**2)/2/self.length/other.length)

    def scalar_mul(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def vector_mul(self, other):
        x = numpy.linalg.det([[self.y, self.z], [other.y, other.z]])
        y = -numpy.linalg.det([[self.x, self.z], [other.x, other.z]])
        z = numpy.linalg.det([[self.x, self.y], [other.x, other.y]])
        return Vector(x, y, z)

    def mul_to_matrix(self, matrix):
        return Vector(*numpy.matmul(list(self), matrix))

    def rmul_to_matrix(self, matrix):
        return Vector(*numpy.matmul(matrix, list(self)))

    def change_basis(self, x, y, z):
        return self.rmul_to_matrix(numpy.array([list(x), list(y), list(z)]))

    def project_to(self, plane_normal_vector):
        sqr = plane_normal_vector.scalar_mul(plane_normal_vector)
        mul = self.scalar_mul(plane_normal_vector)
        t = -mul/sqr
        return self + t*plane_normal_vector

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self*other

    def __sub__(self, other):
        return self + other*-1

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __next__(self):
        yield self.x
        yield self.y
        yield self.z

    def __str__(self):
        return "({}, {}, {})".format(*self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
