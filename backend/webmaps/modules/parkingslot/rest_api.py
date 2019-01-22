""" Parkingslots api module. """
# Python mail libs.
import numpy as np
# Python libs.
import flask
from flask_restplus import Resource, Namespace
# Project files.
from . import lib
from webmaps.models.slots_cluster import ParkingSlotsCluster

NAMESPACE = Namespace(
    'parking-slot', description='Api namespace representing a parking slot.')


@NAMESPACE.route('/')
class ParkingSlot(Resource):
    """
    Api class placemark representing a parking-slot.
    """
    # @NAMESPACE.param('longitude ', 'Longitude of parking slot')
    # @NAMESPACE.param('latitude', 'Latitude of parking slot')

    def get(self):
        """ Return all available parking slots """
        X = np.array([[1, 2], [2, 2], [2, 3],
                      [8, 7], [8, 8], [25, 80]])
        parking_slot_cluster = ParkingSlotsCluster(X, [1, 3])
        clusters = parking_slot_cluster.get_clusters()
        response = clusters
        # Response
        response = flask.jsonify(response)

        return response
