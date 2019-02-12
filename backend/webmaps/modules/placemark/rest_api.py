""" Rest Api module for Placemarks. """
# Python libs.
import flask
import werkzeug
import logging
from flask_restplus import Resource, Namespace, reqparse
# Project files.
from . import lib
from config import CONFIGURATION
from webmaps.models.file_parser import KmlParser
from constans import PLACEMARK_NAMESPACE

NAMESPACE = Namespace(
    'placemark', description='Api namespace representing a placemark.')
LOGGER = CONFIGURATION.get_logger(__name__)
# Models
kml_model = NAMESPACE.parser()
kml_model.add_argument('kml-file', type=werkzeug.datastructures.FileStorage,
                       help='Kml file to be parsed', location='files', required=True)
demand_model = NAMESPACE.parser()
demand_model.add_argument('demand', help='The updated demand.', type=dict, location='json',
                          required=True)


@NAMESPACE.route('/all')
class Placemarks(Resource):
    """
    Api class placemark representing placemarks.
    """

    def get(self):
        """ Return all placemark objects """
        response = dict()
        response = lib.get_placemark_objects()
        # Response
        response = flask.jsonify(response)

        return response

    def delete(self):
        """ Delete all placemark objects. """
        response = lib.delete_placemarks()
        # Response
        response = PLACEMARK_NAMESPACE.get_database_deletion_message(
            len(response))

        return response


@NAMESPACE.route('/file')
class Placemark(Resource):
    """
    Api class placemark representing one placemark.
    """
    @NAMESPACE.expect(kml_model)
    def post(self):
        """
        Input a new kml file and store information to db.
        """

        kml_file = kml_model.parse_args()['kml-file']

        # Response
        response = PLACEMARK_NAMESPACE.FILE_ERROR
        if kml_file:
            kml_parser = KmlParser(kml_file)
            kml_parser.parse()
            file_name = werkzeug.utils.secure_filename(kml_file.filename)
            response = PLACEMARK_NAMESPACE.get_correct_file_parsing_message(
                file_name)

        return response


@NAMESPACE.route('/demand/<int:placemark_id>')
class PlacemarkDemand(Resource):
    """
    Api class placemark representing placemark's demand.
    """
    @NAMESPACE.expect(demand_model)
    def patch(self, placemark_id):
        """ Patch method to update a placemark's demand. """
        # Parse arguments.
        args = demand_model.parse_args()
        demand = args['demand']
        # Call lib function to update demand.
        response = lib.update_demand(placemark_id, demand)
        if response == [True]:
            response = PLACEMARK_NAMESPACE.get_correct_demand_update_message(
                placemark_id)
        else:
            response = PLACEMARK_NAMESPACE.DEMAND_ERROR

        return response

    def get(self, placemark_id):
        """ Get spesific's block real and fixed demand. """
        response = lib.get_demands(placemark_id)

        return response
