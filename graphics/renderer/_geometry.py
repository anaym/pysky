import math

import numpy

from geometry.equatorial import SecondEquatorial
from geometry.point import Point


def rescale_angle_distance(sight_radius, visible_radius, dist):
    return dist / sight_radius * visible_radius


def translate_coordinates(sight_radius, visible_radius, r, sight_vector, diametr, ox, oy, point: SecondEquatorial):
    r = rescale_angle_distance(sight_radius, visible_radius, r)

    cos_da = sight_vector.get_relative_angle_cos(point)
    sin_da = sight_vector.get_relative_angle_sin(point)
    cx, cy = ox - r * sin_da, oy - r * cos_da

    x, y = cx - diametr//2, cy - diametr//2
    return x, y



def get_angle(x1, y1, x2, y2):
    return math.atan2(x1 * x2 + y1 * y2, x1 * y2 - x2 * y1)


def get_see_distance(width, height, angle):
    angle = math.radians(angle)/2
    radius = min(width, height)/2
    return radius / math.tan(angle)


def project(point: SecondEquatorial, see: SecondEquatorial, see_distance: float):
    da = point.alpha - see.alpha
    dd = point.delta - see.delta
    dx = math.tan(da)*see_distance
    dy = math.tan(dd)*see_distance
    return dx, dy


def solve(a00, a01, a10, a11, b0, b1):
    a = numpy.array([[a00, a01], [a10, a11]])
    b = numpy.array([b0, b1])
    try:
        return numpy.linalg.solve(a, b)
    except:
        return None


def extract_2d(point: Point, see: Point, up: Point):
    a = solve(see.x, up.x, see.y, up.y, point.x, point.y)
    b = solve(see.x, up.x, see.z, up.z, point.x, point.z)
    c = solve(see.y, up.y, see.z, up.z, point.y, point.z)
    return a if not a is None else (b if not b is None else c)
