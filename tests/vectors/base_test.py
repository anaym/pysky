import unittest

from math import sqrt

from vectors.vector import Vector


class VectorTest(unittest.TestCase):
    def setUp(self):
        self.x = 2
        self.y = 3
        self.z = 4
        self.v = Vector(self.x, self.y, self.z)

        self.a = Vector(2, 100, 4)
        self.b = Vector(2, 100, 4)

    def test_creation(self):
        self.assertEqual(self.v.x, self.x)
        self.assertEqual(self.v.y, self.y)
        self.assertEqual(self.z, self.z)

    def test_equal(self):
        self.assertEquals(self.a, self.b)

    def test_unequal(self):
        self.assertNotEquals(self.a, self.v)

    def test_unequal_with_another_type_object(self):
        self.assertNotEquals(self.a, 'another type object')

    def test_length(self):
        self.assertEquals(self.a.length, sqrt(self.a.x**2 + self.a.y**2 + self.a.z**2))

    def test_str(self):
        self.assertEquals(str(self.a), "(2, 100, 4)")

if __name__ == '__main__':
    unittest.main()

