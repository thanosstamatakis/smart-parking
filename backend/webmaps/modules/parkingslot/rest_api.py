""" Parkingslots api module. """
# Python mail libs.
import numpy as np
# Python libs.
import flask
import logging
from flask_restplus import Resource, Namespace
# Project files.
from . import lib
from config import CONFIGURATION
from webmaps.models.slots_cluster import ParkingSlotsCluster
from constans import VALIDATION_NAMESPACE

NAMESPACE = Namespace(
    'parking-slot', description='Api namespace representing a parking slot.')
LOGGER = CONFIGURATION.get_logger(__name__)
# Model for parsing arguments.
user_location_model = NAMESPACE.parser()
user_location_model.add_argument(
    'longitude', type=float, help='Longitude of parking slot.')
user_location_model.add_argument(
    'latitude', type=float, help='Latitude of parking slot.')
user_location_model.add_argument(
    'radius', type=float, help= 'Radius of circle to look for parking.'
)


@NAMESPACE.route('/')
class ParkingSlot(Resource):
    """
    Api class placemark representing a parking-slot.
    """
    @NAMESPACE.expect(user_location_model)
    def get(self):
        """ Return all available parking slots """
        args = flask.request.args
        try:
            user_location = [args['latitude'], args['longitude']]
        except KeyError as e:
            LOGGER.debug(e)
            return VALIDATION_NAMESPACE.USER_LOCATION_INPUT_ERROR
        # Response
        response = lib.get_clusters(user_location, args['radius'])
        response = flask.jsonify(response)

        return response
