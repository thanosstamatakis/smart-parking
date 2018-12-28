from flask_restplus import Resource, Namespace

NAMESPACE = Namespace(
    'placemark', description='Api namespace representing a placemark')


@NAMESPACE.route('/')
class Placemark(Resource):
    """
    Api class placemark representing a placemark.
    """
    def get(self):
        """ Return all placemark objects """
        return "HELLo"
