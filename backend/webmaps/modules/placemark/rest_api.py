from flask_restplus import Resource, Namespace, reqparse
from . import lib
from webmaps.parse_kml import read_kml
import flask
import werkzeug

NAMESPACE = Namespace(
    'placemark', description='Api namespace representing a placemark.')

parser = NAMESPACE.parser()
parser.add_argument('kml-file', type=werkzeug.datastructures.FileStorage,
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


@NAMESPACE.route('/')
class Placemark(Resource):
    """
    Api class placemark representing one placemark.
    """
    @NAMESPACE.expect(parser)
    def post(self):
        """
        Input a new kml file and store information to db.
        """

        kml_file = parser.parse_args()['kml-file']

        # Response
        response = "File parsing was unsuccessful."
        if kml_file:
            read_kml(kml_file)
            file_name = werkzeug.utils.secure_filename(kml_file.filename)
            response = f'File {file_name} was successfuly parsed.'

        return response
