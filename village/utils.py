import math


def get_distance(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


def find_coordinates(a, b, ac, bc):
    """
    Calculates coordinates of third point given
    two points and two distances to third point
    :param a: tuple, point one, e.g. (0, 0)
    :param b: tuple, point two, e.g. (0, 1)
    :param ac: distance from point a to unknown point
    :param bc: distance from point b to unknown point
    :return: tuple, coordinates of point c, e.g. (0.5, 0.8660254)
    """
    ab = get_distance(a, b)
    cab_cos = (ac*ac + ab*ab - bc*bc) / (2.0*ac*ab)
    cx = a[0] + ac * cab_cos
    cy = a[1] + ac * math.sqrt(1 - cab_cos ** 2)
    return cx, cy


def get_third_point(a, b, c, ad, bd, cd, epsilon=0.001):
    ab = get_distance(a, b)

    if (ad + bd < ab) or (math.fabs(ad - bd) > ab):
        raise ValueError('no such point: lengths are too short')

    bh = (ad ** 2 - bd ** 2 + ab ** 2) / (2.0 * ab)
    ah = ab - bh

    h = math.sqrt(math.fabs(ad ** 2 - ah ** 2))

    px = a[0] + (ah / ab) * (b[0] - a[0])
    py = a[1] + (ah / ab) * (b[1] - a[1])

    d1x = px + h * (b[1] - a[1]) / ab
    d1y = py - h * (b[0] - a[0]) / ab

    d2x = px - h * (b[1] - a[1]) / ab
    d2y = py + h * (b[0] - a[0]) / ab

    cd1 = get_distance((d1x, d1y), c)
    cd2 = get_distance((d2x, d2y), c)

    if math.fabs(cd1 - cd2) < epsilon:
        raise ValueError('no such point: all three points are lying on one line')

    if math.fabs(cd1 - cd) < epsilon:
        return d1x, d1y

    if math.fabs(cd2 - cd) < epsilon:
        return d2x, d2y

    raise ValueError('no such point: neither solution matches with third point and length')
