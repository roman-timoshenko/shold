import logging
import math

DEFAULT_EPSILON = 0.001
logger = logging.getLogger(__name__)

def get_distance(a, b):
    """
    Calculates distance between two points
    :param a: tuple, point one, e.g. (0, 0)
    :param b: tuple, point two, e.g. (0, 1)
    :return: distance between two points
    """
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def intersect(x0, y0, r0, x1, y1, r1):
    """
    Checks if two circles intersect.
    A way to avoid throwing ValueError
    :param x0: first circle center X coordinate
    :param y0: first circle center Y coordinate
    :param r0: first circle radius
    :param x1: second circle center X coordinate
    :param y1: second circle center Y coordinate
    :param r1: second circle radius
    :return: true if circles intersect, false otherwise
    """
    d = get_distance((x0, y0), (x1, y1))
    if d > r0 + r1:
        return False
    if d < math.fabs(r0 - r1):
        return False
    return True


def find_circle_intersections(x0, y0, r0, x1, y1, r1):
    """
    Finds two points of intersection for two circles.
    :param x0: first circle center X coordinate
    :param y0: first circle center Y coordinate
    :param r0: first circle radius
    :param x1: second circle center X coordinate
    :param y1: second circle center Y coordinate
    :param r1: second circle radius
    :return: :raise ValueError: when circles do not intersect
    """
    d = get_distance((x0, y0), (x1, y1))
    if d > r0 + r1:
        raise ValueError('circles are not intersecting: too far from each other')
    if d < math.fabs(r0 - r1):
        raise ValueError('circles are not intersecting: one inside another')

    a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(math.fabs(r0 ** 2 - a ** 2))

    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d

    xa3 = x2 + h * (y1 - y0) / d
    ya3 = y2 - h * (x1 - x0) / d

    xb3 = x2 - h * (y1 - y0) / d
    yb3 = y2 + h * (x1 - x0) / d

    return (xa3, ya3), (xb3, yb3)


def get_fourth_point(a, b, c, ad, bd, cd, epsilon=DEFAULT_EPSILON):
    """
    Finds fourth point by three points and distance from those points to fourth point.
    :param a: tuple, point one, e.g. (0, 0)
    :param b: tuple, point two, e.g. (0, 1)
    :param c: tuple, point three, e.g. (1, 1)
    :param ad: distance from point a to unknown point d
    :param bd: distance from point b to unknown point d
    :param cd: distance from point c to unknown point d
    :param epsilon:
    :return:
    """
    try:
        first, second = find_circle_intersections(a[0], a[1], ad, b[0], b[1], bd)
    except ValueError as e:
        logger.info(e)
        raise ValueError('intersection point cannot be found, please, verify data')

    distance_to_first = get_distance(c, first)
    distance_to_second = get_distance(c, second)

    if math.fabs(distance_to_first - distance_to_second) < epsilon:
        raise ValueError('cannot find intersection point correctly, please, verify data')

    if math.fabs(distance_to_first - cd) < epsilon:
        return first
    if math.fabs(distance_to_second - cd) < epsilon:
        return second

    raise ValueError('intersection point cannot be found, please, verify data')

# x1 = 0
# y1 = 0
# r1 = 1
# x2 = 1
# y2 = 0
# r2 = 2
#
# intersections = find_circle_intersections(x1, y1, r1, x2, y2, r2)
#
# print(get_third_point((0, 0), (1, 0), (1, 1), 1, math.sqrt(2), 1))
#
# print(intersections)
#
# for intersection in intersections:
#     print (x1 - intersection[0]) ** 2 + (y1 - intersection[1]) ** 2, r1 ** 2
#     print (x2 - intersection[0]) ** 2 + (y2 - intersection[1]) ** 2, r2 ** 2
# print(get_third_point((0, 0), (1, 0), (0, 0), 1, math.sqrt(2), 1))
