from flask_restplus import Resource, Namespace, reqparse
from flask import request
from . import lib
from webmaps.models import User as User_Class

NAMESPACE = Namespace(
    'user', description='Api namespace representing an app user.')


@NAMESPACE.route('/')
class User(Resource):
    """
    Api class placemark representing an app user.
    """
    @NAMESPACE.param('type', 'Type of user.')
    @NAMESPACE.param('username', 'Username of user to be stored.')
    @NAMESPACE.param('password', 'Password of user to be stored.')
    def post(self):
        """ Post function for storing user credentials to db """
        args = request.args
        try:
            user_type = str(args['type'])
            user_name = str(args['username'])
            user_pass = str(args['password'])
        except AttributeError:
            return 'User was unsuccessfuly stored. Check users credentials again.'
        new_user = User_Class(user_type, user_name, user_pass)
        new_user.save_to_db()

        # Response
        return 'User was successfuly stored'
