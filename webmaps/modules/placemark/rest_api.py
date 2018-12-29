from flask_restplus import Resource, Namespace
from . import lib
import flask

NAMESPACE = Namespace(
    'placemark', description='Api namespace representing a placemark.')


@NAMESPACE.route('/')
class Placemark(Resource):
    """
    Api class placemark representing a placemark.
    """

    def get(self):
        """ Return all placemark objects """
        response = []
        response = lib.get_placemark_objects()
        
        # Response
        response = flask.jsonify(response)
        return response
