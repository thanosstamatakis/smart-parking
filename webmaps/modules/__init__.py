from flask_restplus import Resource, Api
from webmaps import APP
from .placemark.rest_api import NAMESPACE as placemark_ns

API = Api()
API.add_namespace(placemark_ns)
