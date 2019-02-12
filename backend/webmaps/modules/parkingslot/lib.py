""" This module contains helper function for placemark api """
# Python libs.
import redis
import logging
import numpy as np
import random
from math import sqrt
# Project files.
from config import CONFIGURATION
from webmaps.models.slots_cluster import ParkingSlotsCluster
from webmaps.utils.general_sanitizations import point_sanitization

redis_conn = redis.Redis(host=CONFIGURATION.db_conn, decode_responses=True)
LOGGER = CONFIGURATION.get_logger(__name__)

# X = np.array([[1, 2], [2, 2], [2, 3],
#                       [8, 7], [8, 8], [25, 80]])
# parking_slot_cluster = ParkingSlotsCluster(X, user_location)
# clusters = parking_slot_cluster.get_clusters()


def get_clusters(user_location, radius, time):
    """ Return all clusters """
    close_clusters = get_close_clusters(user_location, radius)
    LOGGER.debug(f'CLOSE CLUSTERS: {len(close_clusters)}')
    parking_slots = get_parking_slots(close_clusters, time)
    slots = [x for x in parking_slots.values()]
    LOGGER.debug(f'PARKING SLOTS: {slots}')
    if not slots:
        return slots
    slots = np.array(slots)
    parking_slot_cluster = ParkingSlotsCluster(slots, user_location)
    clusters = parking_slot_cluster.get_clusters()

    return clusters


def get_parking_slots(clusters, time):
    """ Return the parking slots of the cluster in long and lat format """
    cluster_parking_slots = dict()

    for placemark_id, cluster in clusters.items():
        redis_key = ":".join(('placemark', placemark_id, 'polygon', 'slots'))
        parking_slots = redis_conn.get(redis_key)
        parking_slots = _get_available_parking_slots(parking_slots, time,
                                                     redis_key)
        distance_from_centroid = get_distance_from_centroid()
        for parking_slot in range(parking_slots):
            cluster_parking_slots[placemark_id] = [
                float(cluster[0]) + distance_from_centroid,
                float(cluster[1]) + distance_from_centroid
            ]

    return cluster_parking_slots


def get_distance_from_centroid():
    """ Return the distance from centroid. """
    distance_from_centroid = random.randint(1, 50) * 0.0000089
    # If random number >= 0.5 then true.
    if random.random() >= 0.5:
        return -distance_from_centroid

    return distance_from_centroid


def get_close_clusters(user_location, radius):
    """ Return centroids of clusters in database  inside area. """
    redis_key = 'placemark'
    clusters = dict()
    placemark_ids = redis_conn.smembers(redis_key)
    for placemark_id in placemark_ids:
        redis_key = ":".join(('placemark', placemark_id))
        centroid = redis_conn.hget(redis_key, 'centroid')
        if not centroid or centroid == '0':
            continue
        centroid = point_sanitization(centroid)
        if check_if_cluster_is_close(centroid, user_location, radius):
            clusters[placemark_id] = centroid

    return clusters


def check_if_cluster_is_close(centroid, user_location, radius):
    """
    Check if cluster's distance and users desired location are
    inside radius.
    """
    lang_diff = float(centroid[0]) - float(user_location[0])
    long_diff = float(centroid[1]) - float(user_location[1])
    distance = sqrt(lang_diff ** 2 + long_diff ** 2)
    if (distance < float(radius)):
        return True

    return False


def _get_available_parking_slots(parking_slots, time, redis_key):
    """ Get available parking slots for specific block. """
    parking_slots = int(parking_slots)
    time = int(round(float(time)))
    # Get from db Population, fixed and normal demand.
    # Remove redis_key slots ending.
    redis_key = ":".join((redis_key.split(':')[:-2]))
    population = int(redis_conn.hget(redis_key, 'population'))
    redis_key = ":".join((redis_key, 'polygon'))
    fixed_demand = float(redis_conn.lrange(
        f'{redis_key}:fixed_demand', 0, 0)[0])
    real_demand = float(redis_conn.lrange(
        f'{redis_key}:demand', time-1, time-1)[0])
    # Available parking slots are parking slots -
    # fixed demand * population + remaining * normal demand.
    fixed_demand_parking_slots = fixed_demand * population
    parking_slots = int(round(parking_slots - fixed_demand_parking_slots + \
        (parking_slots - fixed_demand_parking_slots) * real_demand))
    # Check if parking slots are bellow 0.
    parking_slots = 0 if parking_slots < 0 else parking_slots
    LOGGER.debug(f'Time: {time}, Fixed demand: {fixed_demand}, \
    Norm: {real_demand}, Parking SLOTS: {parking_slots}')

    return parking_slots
