""" Users rest api module. """
# System Libs
import logging
from flask_restplus import Resource, Namespace, reqparse
from flask import request
# Project Files
from . import lib
from config import CONFIGURATION
from webmaps.models import User as User_Class

NAMESPACE = Namespace(
    'user', description='Api namespace representing an app user.')
LOGGER = CONFIGURATION.get_logger(__name__)
user_model = NAMESPACE.parser()
user_model.add_argument('type', type=str, default='normal',
                        help='Type of user.')
user_model.add_argument('username', type=str, help='Username of user.')
user_model.add_argument('password', type=str, help='Password of user.')


@NAMESPACE.route('/validation')
class Validation(Resource):
    """
    Api class for user validation.
    """
    @NAMESPACE.expect(user_model)
    def post(self):
        """ Post function for storing user credentials to db. """
        args = request.args
        try:
            user_type = str(args['type'])
            user_name = str(args['username'])
            user_pass = str(args['password'])
        except AttributeError:
            return 'User was unsuccessfuly stored. Check users credentials again.'
        user = User_Class(user_type, user_name, user_pass)
        response = user.check_if_user_exists()

        # Response
        return response


@NAMESPACE.route('/adduser')
class AddUser(Resource):
    """
    Api class for adding new user.
    """
    @NAMESPACE.expect(user_model)
    def post(self):
        """ Post function for storing user credentials to db. """
        args = request.args
        try:
            user_type = str(args['type'])
            user_name = str(args['username'])
            user_pass = str(args['password'])
        except AttributeError:
            return 'User was unsuccessfuly stored. Check users credentials again.'
        new_user = User_Class(user_type, user_name, user_pass)
        response = new_user.check_if_user_exists()
        if response == 'User does not exist':
            new_user.save_to_db()
            response = f'User {new_user.username} is saved to db.'
        else:
            response = 'Username exists, try a different one.'
        # Response
        return response
