from flask_restplus import Resource, Api
from flask import Blueprint
from webmaps import APP
from .placemark.rest_api import NAMESPACE as placemark_ns
from .parkingslot.rest_api import NAMESPACE as parkingslot_ns


API = Api(doc='/doc/', prefix='/api')
API.add_namespace(placemark_ns)
API.add_namespace(parkingslot_ns)
