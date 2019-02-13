""" Utility module containing functions for sanitization """
# Python libs.
import logging
import re
# Project files.
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
    point[0], point[1] = point[1], point[0]

    return point


def polygon_sanitization(coordinates):
    """ Sanitize polygon string into list of point lists. """
    points_in_polygon_reg = re.compile(r'(\d+\.?\d*\ \d+\.?\d*)')
    polygon = coordinates.strip('()')
    coords = list()
    for coord_group in re.findall(points_in_polygon_reg, polygon):
        point_list = coord_group.split(' ')
        for index, point in enumerate(point_list):
            point_list[index] = float(point)
        coords.append(point_list)

    return coords
