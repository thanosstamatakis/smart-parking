""" This module contains helper function for placemark api """
# Python libs.
import redis
import logging
# Project files.
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
        placemark_num = obj
        temp_key = ":".join((redis_key, placemark_num))
        response[obj] = redis_conn.hgetall(temp_key)

    return response


def get_polygon_attributes():
    """
    Return polygon attributes for each placemark.
    """
    response = dict()
    polygon_elements = dict()
    redis_key = 'placemark'
    placemark_ids = redis_conn.smembers(redis_key)
    for placemark_id in placemark_ids:
        redis_key = ":".join(('placemark', str(placemark_id), 'polygon'))
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

        response[placemark_id] = [polygon_elements]

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


def update_demand(placemark_id, demand_per_hour):
    """ Update a placemark's demand in database. """
    redis_key = ":".join(('placemark', str(placemark_id), 'polygon', 'demand'))
    redis_pipe = redis_conn.pipeline()
    response = 'An error occured!'
    try:
        for time, demand in demand_per_hour.items():
            redis_pipe.lset(redis_key, int(time), demand)
            LOGGER.debug(
                f'Set to key: {redis_key} at list position: {time} value: {demand}')
    except ValueError:
        pass
    try:
        response = redis_pipe.execute()
    except redis.exceptions.ResponseError:
        pass

    return response


def get_demands(placemark_id):
    """ 
    Return spesific placemark's real and fixed demand 
    from database.
    """
    demand_types = ['demand', 'fixed_demand']
    redis_key = ":".join(('placemark', str(placemark_id), 'polygon'))
    demands = dict.fromkeys(demand_types)

    for demand_type in demand_types:
        temp_redis_key = ":".join((redis_key, demand_type))
        demands[demand_type] = redis_conn.lrange(temp_redis_key, 0, -1)

    return demands


def get_availability(time_of_simulation):
    """
    Return the percentage of availability for each block. 
    """
    # Round time
    time_of_simulation = int(round(float(time_of_simulation)))

    availability_per_block = dict()
    placemarks = redis_conn.smembers('placemark')
    for placemark in placemarks:
        redis_key = ":".join(('placemark', str(placemark), 'polygon'))
        #LOGGER.debug(f'redis key: {redis_key}')
        real_demand = float(redis_conn.lrange(
            f'{redis_key}:demand', time_of_simulation - 1, time_of_simulation - 1)[0])
        fixed_demand = float(redis_conn.lrange(
            f'{redis_key}:fixed_demand', time_of_simulation - 1, time_of_simulation - 1)[0])

        if real_demand >= 1 or fixed_demand >= 1:
            availability_per_block[placemark] = 0
            LOGGER.debug(f'Fixed {fixed_demand}, {real_demand}')
        else:
            availability_per_block[placemark] = 1 - \
                real_demand if real_demand > fixed_demand else 1 - fixed_demand

    return availability_per_block


def map_availability_to_color(availability_per_block):
    """ Map availability of each block to the corresponding color. """
    range_to_color = {0.59: 'green', 0.84: 'yellow', 1: 'red'}
    for placemark_id, availability in availability_per_block.items():
        for max_num, color in range_to_color.items():
            if availability <= max_num:
                availability_per_block[placemark_id] = color
                LOGGER.debug(f'{placemark_id} {availability} {color}')
                break

    return availability_per_block
