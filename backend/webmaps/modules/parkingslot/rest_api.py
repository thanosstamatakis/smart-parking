from flask_restplus import Resource, Namespace
from . import lib
import flask

NAMESPACE = Namespace(
    'parking-slot', description='Api namespace representing a parking slot.')


@NAMESPACE.route('/')
class ParkingSlot(Resource):
    """
    Api class placemark representing a parking-slot.
    """
    @NAMESPACE.param('longitude ', 'Longitude of parking slot')
    @NAMESPACE.param('latitude', 'Latitude of parking slot')
    def get(self):
        """ Return all available parking slots """
        response = []

        # Response
        response = flask.jsonify(response)

        return response
