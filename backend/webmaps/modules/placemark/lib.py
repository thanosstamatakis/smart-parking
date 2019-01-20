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
    response = []
    redis_key = 'placemark'
    placemark_objects = redis_conn.smembers(redis_key)
    for obj in placemark_objects:
        placemark_num = obj.split('.')[1]
        temp_key = ":".join((redis_key, placemark_num))
        placemark_attr = redis_conn.hgetall(temp_key)
        response.append({'name': obj, **placemark_attr})

    return response

def delete_placemarks():
    """
    Delete all placemarks from redis database.
    """
    redis_pipe = redis_conn.pipeline()
    for key in redis_conn.scan_iter(match='placemark*'):
       redis_pipe.delete(key)
    response = redis_pipe.execute()

    return response