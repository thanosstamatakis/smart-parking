""" Utility module to generate demand. """
# Python libs.
import random as rand
import numpy as np
import redis
import logging
# Project files.
from config import CONFIGURATION

LOGGER = CONFIGURATION.get_logger(__name__)
redis_conn = redis.Redis(host=CONFIGURATION.db_conn, decode_responses=True)


def generate_demand():
    """ Retrun a list of demands per hour """
    rand_demands = list()
    for i in range(24):
        rand_demands.append(round(rand.random(), 2))

    return rand_demands


def get_simulation_demand(simulation_time, redis_key):
    """
    Return demand for specific hour based on previous and 
    next hour demand.
    """
    demands = list()
    # Get previous and next hour demand from db.
    simulation_period = [simulation_time//1, 1 + simulation_time//1]
    for time in simulation_period:
        demands.append(float(redis_conn.lrange(
            f'{redis_key}:demand', int(time)-1, int(time)-1)[0]))
    coefficients = np.polyfit(simulation_period, demands, 1)
    polynomial = np.poly1d(coefficients)

    return polynomial(simulation_time)
