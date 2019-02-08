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


def get_clusters(user_location, radius):
    """ Return all clusters """
    close_clusters = get_close_clusters(user_location, radius)
    LOGGER.debug(f'CLOSE CLUSTERS: {len(close_clusters)}')
    parking_slots = get_parking_slots(close_clusters)
    slots = [x for x in parking_slots.values()]
    LOGGER.debug(f'PARKING SLOTS: {slots}')
    slots = np.array(slots)
    parking_slot_cluster = ParkingSlotsCluster(slots, user_location)
    clusters = parking_slot_cluster.get_clusters()

    return clusters


def get_parking_slots(clusters):
    """ Return the parking slots of the cluster in long and lat format """
    def _check_for_pos_neg():
        """ If random number >= 0.5 then true. """
        if random.random() >= 0.5:
            return True

        return False

    cluster_parking_slots = dict()

    for placemark_id, cluster in clusters.items():
        redis_key = ":".join(('placemark', placemark_id, 'polygon', 'slots'))
        parking_slots = redis_conn.get(redis_key)
        distance_from_centroid = 50 * 0.0000089
        if not _check_for_pos_neg():
            distance_from_centroid = -distance_from_centroid
        for parking_slot in parking_slots:
            cluster_parking_slots[placemark_id] = [
                float(cluster[0]) + distance_from_centroid, float(cluster[1]) + distance_from_centroid]

    return cluster_parking_slots


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
    """ Check """
    lang_diff = float(centroid[0]) - float(user_location[0])
    long_diff = float(centroid[1]) - float(user_location[1])
    distance = sqrt(lang_diff ** 2 + long_diff ** 2)
    if (distance < float(radius)):
        return True

    return False
