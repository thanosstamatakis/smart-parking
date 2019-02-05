""" Utility module containing functions for sanitization """
import logging
from config import CONFIGURATION

LOGGER = CONFIGURATION.get_logger(__name__)


def point_sanitization(point):
    """ Sanitize point from MultiGeo format to list """
    LOGGER.debug(f'POINT SANI: {point}')
    point = str(point).translate(
        str.maketrans({'(': '', ')': ''})).split(' ')[0:]
    if 'POINT'in point:
        point.remove('POINT')
        return point
    point[0], point[1]=point[1], point[0]

    return point
