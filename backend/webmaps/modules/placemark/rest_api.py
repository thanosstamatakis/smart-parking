from flask_restplus import Resource, Namespace, reqparse
from . import lib
from webmaps.parse_kml import read_kml
import flask
import werkzeug

NAMESPACE = Namespace(
    'placemark', description='Api namespace representing a placemark.')

kml_model = NAMESPACE.parser()
kml_model.add_argument('kml-file', type=werkzeug.datastructures.FileStorage,
                       help='Kml file to be parsed', location='files', required=True)


@NAMESPACE.route('/all')
class Placemarks(Resource):
    """
    Api class placemark representing placemarks.
    """

    def get(self):
        """ Return all placemark objects """
        response = []
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
            read_kml(kml_file)
            file_name = werkzeug.utils.secure_filename(kml_file.filename)
            response = f'File {file_name} was successfuly parsed.'

        return response
