""" This module contains helper function for placemark api """
# Python libs.
import redis
import logging
import numpy as np
import random
from math import sin, cos, sqrt, atan2, radians
# Project files.
from config import CONFIGURATION
from webmaps.utils import demand
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
    close_centroids = get_close_centroids(user_location, radius)
    LOGGER.debug(f'CLOSE CLUSTERS: {len(close_centroids)}')
    parking_slots = get_parking_slots(close_centroids, time)
    try:
        slots = list(parking_slots.values())[0]
    except IndexError:
        slots = None
    if not slots:
        return []
    slots = np.array(slots)
    parking_slot_cluster = ParkingSlotsCluster(slots, user_location)
    clusters = parking_slot_cluster.get_clusters()

    return clusters


def get_parking_slots(clusters, time):
    """ Return the parking slots of the cluster in long and lat format """
    blocks_parking_slots = dict()

    for placemark_id, cluster in clusters.items():
        redis_key = ":".join(('placemark', placemark_id, 'polygon', 'slots'))
        parking_slots = redis_conn.get(redis_key)
        parking_slots = _get_available_parking_slots(parking_slots, time,
                                                     redis_key)
        parking_slots_in_cluster = list()
        for parking_slot in range(parking_slots):
            distance_from_centroid = get_distance_from_centroid()

            parking_slots_in_cluster.append([float(cluster[0]) + distance_from_centroid,
                                             float(cluster[1]) + distance_from_centroid])

        blocks_parking_slots[placemark_id] = parking_slots_in_cluster
        LOGGER.debug(
            f'BLOCK: {placemark_id}, num of slots: {len(parking_slots_in_cluster)}\n\n\n')
    # LOGGER.debug(f'CLUSTERS PS: {blocks_parking_slots}')
    return blocks_parking_slots


def get_distance_from_centroid():
    """ Return the distance from centroid. """
    distance_from_centroid = random.randint(1, 50) * 0.00000089
    # If random number >= 0.5 then true.
    if random.random() >= 0.5:
        return -distance_from_centroid

    return distance_from_centroid


def get_close_centroids(user_location, radius):
    """ Return centroids of polygons in database inside area. """
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
    R = 6373.0
    # Python fucntion use radians, not degrees.
    lat1 = radians(float(centroid[0]))
    lon1 = radians(float(centroid[1]))
    lat2 = radians(float(user_location[1]))
    lon2 = radians(float(user_location[0]))
    # Get distance in radias in longiture and latitude
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # Distance in km transofrmed to meters.
    distance = R * c * 1000
    # LOGGER.debug(f'LAT-LON: {centroid[0]}{lat1}|{lon1} USER: {lat2}|{lon2} dist:{distance}')
    # distance = sqrt(lang_diff ** 2 + long_diff ** 2)
    if (distance < float(radius)):
        LOGGER.debug(
            f'Distance: {distance}, radius: {radius}, Cluster: {centroid}')
        return True

    return False


def _get_available_parking_slots(parking_slots, time, redis_key):
    """ Get available parking slots for specific block. """
    parking_slots = int(parking_slots)
    time = float(time)
    # Get from db Population, fixed and normal demand.
    # Remove redis_key slots ending.
    redis_key = ":".join((redis_key.split(':')[:-2]))
    population = int(redis_conn.hget(redis_key, 'population'))
    redis_key = ":".join((redis_key, 'polygon'))
    # Get fixed demand.
    fixed_demand = float(redis_conn.lrange(
        f'{redis_key}:fixed_demand', 0, 0)[0])
    # Get real demand.
    real_demand = demand.get_simulation_demand(time, redis_key)

    # Available parking slots are parking slots -
    # fixed demand * population + remaining * normal demand
    # and are computed bellow.
    LOGGER.debug(f'PARKING SLOTS: {parking_slots}')
    # Number of Parking slots occupied by civilians with parking slot cards.
    fixed_demand_parking_slots = fixed_demand * population
    LOGGER.debug(f'FIXED DEMAND PS: {fixed_demand_parking_slots}')
    # Number of Parking slots remaining without fixed.
    remaining_parking_slots = parking_slots - fixed_demand_parking_slots
    LOGGER.debug(f'REMAINING PS: {remaining_parking_slots}')
    # Number of Parking slots occupied by people based on demand at the time.
    real_demand_parking_slots = remaining_parking_slots * real_demand
    LOGGER.debug(f'REAL DEMAND PS: {real_demand_parking_slots}')
    # Available parking slots = All - Real demand - Fixed.
    available_parking_slots = int(round(parking_slots -
                                        real_demand_parking_slots - fixed_demand_parking_slots))
    LOGGER.debug(f'AVAILABLE PS: {available_parking_slots}')
    # Check if parking slots are bellow 0 or more than the parking slots.
    available_parking_slots = 0 if available_parking_slots < 0 else available_parking_slots
    available_parking_slots = parking_slots if int(
        available_parking_slots) > int(parking_slots) else available_parking_slots

    return available_parking_slots
