from unittest import TestCase


class DoubleTestCase(TestCase):
    EPS = 1E-3

    def assertEqual(self, first, second, msg=None, epsilon=None, mod=None):
        if epsilon is None:
            super().assertEqual(first, second, msg)
        elif mod is None:
            super().assertLess(abs(first - second), epsilon, msg)
        else:
            super().assertLess(abs(first - second)%mod, epsilon, msg)
