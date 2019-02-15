""" This module represents a Parking Slots Cluster model. """
# Python libs.
import logging
import math
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint
# Project files.
from config import CONFIGURATION
from webmaps.utils.general_sanitizations import point_sanitization

LOGGER = CONFIGURATION.get_logger(__name__)


class ParkingSlotsCluster():
    """ Parking Slots Cluster Class. """

    def __init__(self, parking_slots, user_location):
        """ Constructor method. """
        self.parking_slots = parking_slots
        self.user_location = user_location
        self.clustering = self.get_clustering()

    def get_clustering(self):
        """
        Use DBSCAN to group points into clusters and
        return clustering.
        """
        # Get DBSCAN model.
        model = DBSCAN(eps=0.0002, min_samples=2)
        # Get clustering from DB scan model.
        clustering = model.fit(self.parking_slots)

        return clustering

    def get_clusters(self):
        """
        Get all maximum parking slot clusters with their
        attributes.
        """
        correct_clusters = list()
        # Find number of clusters.
        number_of_clusters = len(set(self.clustering.labels_)) - \
            (1 if -1 in self.clustering.labels_ else 0)
        # Get cluster arrays.
        clusters = [self.parking_slots[self.clustering.labels_ == i]
                    for i in range(number_of_clusters)]
        # Get max points clusters.
        clusters = self._find_max_point_cluster(clusters)

        for cluster in clusters:
            # LOGGER.debug(f"CLUSTERS: {clusters} CLUSTER: {type(cluster)}")
            if len(cluster) > 0:
                cluster_cent = self._get_clusters_centroid(cluster)
                cluster_dist = self._get_clusters_distance(cluster_cent)
                correct_clusters.append(
                    {'centroid': cluster_cent, 'distance': cluster_dist})

        return correct_clusters

    def _find_max_point_cluster(self, clusters):
        """
        Find the cluster or clusters with maximum parking slots.
        """
        max_points_clusters = list()
        max_len = 0
        # Get max lenth of clusters.
        for cluster in clusters:
            if len(cluster) > max_len:
                max_len = len(cluster)
        # Find clusters with max lengths.
        max_points_clusters.append(
            [cluster for cluster in clusters if len(cluster) == max_len])
        max_points_clusters = max_points_clusters[0]

        return max_points_clusters

    def _get_clusters_centroid(self, cluster):
        """ Get specific cluster's coordinates. """
        # Use Multipoint to get cluster
        centroid = MultiPoint(cluster).centroid
        # LOGGER.debug(f"CENTROID PASSED: {centroid}")
        # Sanitize format of centroid
        centroid = point_sanitization(centroid)
        # Further formating.
        # LOGGER.debug(f"CENTROID PASSED: {centroid}")
        centroid = self._sanitize_lists_numbers(centroid)

        return centroid

    def _get_clusters_distance(self, clusters_center):
        """ Get specific cluster's distance from user point. """
        distance = math.sqrt(
            (clusters_center[0] - float(self.user_location[0]))**2 +
            (clusters_center[1] - float(self.user_location[1]))**2)

        return distance

    @staticmethod
    def _sanitize_lists_numbers(list_to_sanitize):
        """ Limit lists floats to 2 decimals and return. """
        for index, number in enumerate(list_to_sanitize):
            # list_to_sanitize[index] = float("%.2f" % round(float(number), 2))
            list_to_sanitize[index] = float(number)

        return list_to_sanitize
