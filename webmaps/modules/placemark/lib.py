""" This module contains helper function for placemark api """
import redis
from config import CONFIGURATION

redis_conn = redis.Redis(CONFIGURATION.db_conn)
redis_pipe = redis_conn.pipeline()


def get_placemark_objects():
    """
    Return as dictionary all the placemark objects from db.
    """
    response = []
    redis_key = 'placemark'
    placemark_objects = redis_conn.smembers(redis_key)
    for obj in placemark_objects:
        placemark_num = str(obj).split('.')[1]
        placemark_attr = redis_pipe.hgetall(
            ":".join((redis_key, placemark_num)))
        response.append({'name': str(obj), 'population': str(placemark_attr['population']),
                         'coordinates': str(placemark_attr['coordinates'])})
    redis_pipe.execute()

    return response
