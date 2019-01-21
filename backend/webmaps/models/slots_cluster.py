""" This module represents a Parking Slots Cluster model. """
from sklearn.cluster import DBSCAN


class ParkingSlotsCluster():
    """ Parking Slots Cluster Class. """

    def __init__(self, parking_slots):
        """ Constructor method. """
        self.parking_slots = parking_slots
