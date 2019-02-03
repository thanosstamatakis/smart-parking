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
        response = f'{len(response)} keys deleted from database.'

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
        response = "File parsing was unsuccessful."
        if kml_file:
            kml_parser = KmlParser(kml_file)
            kml_parser.parse()
            file_name = werkzeug.utils.secure_filename(kml_file.filename)
            response = f'File {file_name} was successfuly parsed.'

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
            response = f'Demand of Placemark:{placemark_id} is updated!'
        else:
            response = 'An error occured. Demand is not updated!'

        return response
