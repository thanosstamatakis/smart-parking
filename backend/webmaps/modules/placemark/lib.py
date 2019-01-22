""" This module contains helper function for placemark api """
import redis
import logging
from config import CONFIGURATION

redis_conn = redis.Redis(host=CONFIGURATION.db_conn, decode_responses=True)
LOGGER = CONFIGURATION.get_logger(__name__)


def get_placemark_objects():
    """
    Return as dictionary all the placemark objects from db.
    """
    response = dict()
    redis_key = 'placemark'
    placemark_objects = redis_conn.smembers(redis_key)
    for obj in placemark_objects:
        placemark_num = obj.split('.')[1]
        temp_key = ":".join((redis_key, placemark_num))
        placemark_attr = redis_conn.hgetall(temp_key)
        polygon_attrs = get_polygon_attributes(temp_key)
        response[obj] = {**placemark_attr, **polygon_attrs}
    return response


def get_polygon_attributes(redis_key):
    """
    Return polygon attributes for given placemark.
    """
    polygon_elements = dict()
    redis_key = ":".join((redis_key, 'polygon'))
    polygon_attrs = redis_conn.smembers(redis_key)
    try:
        polygon_elements['parking_slots'] = redis_conn.get(
            ":".join((redis_key, 'slots')))
    except KeyError:
        polygon_elements['parking_slots'] = 0
    LOGGER.debug(
        f'Get from key {redis_key}:slots value {polygon_elements["parking_slots"]}')
    for polygon_attr in set(polygon_attrs) - {'slots'}:
        temp_key = ":".join((redis_key, str(polygon_attr)))
        polygon_elements[polygon_attr] = redis_conn.lrange(temp_key, 0, -1)
        LOGGER.debug(
            f'Get from key {temp_key} value {polygon_elements[polygon_attr]}')
    return polygon_elements


def delete_placemarks():
    """
    Delete all placemarks from redis database.
    """
    redis_pipe = redis_conn.pipeline()
    for key in redis_conn.scan_iter(match='placemark*'):
        redis_pipe.delete(key)
    response = redis_pipe.execute()

    return response
