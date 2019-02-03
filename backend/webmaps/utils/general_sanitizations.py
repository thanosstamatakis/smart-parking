""" Utility module containing functions for sanitization """

def point_sanitization(point):
    """ Sanitize point from MultiGeo format to list """
    point = str(point).translate(
            str.maketrans({'(': '', ')': ''})).split(' ')[1:]
    point[0], point[1] = point[1], point[0]

    return point