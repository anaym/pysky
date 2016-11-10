import unittest

from math import sqrt

from vectors.vector import Vector


class VectorTest(unittest.TestCase):
    def setUp(self):
        self.a = Vector(100500, 100, 4)
        self.b = Vector(2, 100, 4)

    def test_sum(self):
        expected = Vector(self.a.x + self.b.x, self.a.y + self.b.y, self.a.z + self.b.z)
        self.assertEqual(self.a + self.b, expected)

    def test_mul_to_int(self):
        m = 7
        expected = Vector(self.a.x*m, self.a.y*m, self.a.z*m)
        self.assertEqual(self.a*m, expected)

    def test_mul_to_float(self):
        m = 0.5
        expected = Vector(self.a.x*m, self.a.y*m, self.a.z*m)
        self.assertEqual(self.a*m, expected)

    def test_throws_when_incorrect_mul(self):
        m = 'stuff'
        with self.assertRaises(TypeError):
            self.a*m

    def test_sub(self):
        expected = Vector(self.a.x - self.b.x, self.a.y - self.b.y, self.a.z - self.b.z)
        self.assertEqual(self.a - self.b, expected)

if __name__ == '__main__':
    unittest.main()

