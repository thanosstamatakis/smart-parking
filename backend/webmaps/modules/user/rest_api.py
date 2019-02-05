""" Users rest api module. """
# Python Libs
import logging
from flask_restplus import Resource, Namespace, reqparse
from flask import request
# Project Files
from . import lib
from config import CONFIGURATION
from webmaps.models.website import User as User_Class
from constans import (VALIDATION_NAMESPACE, REGISTRATION_NAMESPACE)

NAMESPACE = Namespace(
    'user', description='Api namespace representing an app user.')
LOGGER = CONFIGURATION.get_logger(__name__)
user_model = NAMESPACE.parser()
user_model.add_argument('type', type=str, default='normal',
                        help='Type of user.', choices=['normal', 'admin'])
user_model.add_argument('username', type=str, help='Username of user.')
user_model.add_argument('password', type=str, help='Password of user.')


@NAMESPACE.route('/validation')
class Validation(Resource):
    """
    Api class for user validation.
    """
    @NAMESPACE.expect(user_model)
    def get(self):
        """ Get function for checking user credentials. """
        args = request.args
        try:
            user_type = str(args['type'])
            user_name = str(args['username'])
            user_pass = str(args['password'])
        except AttributeError:
            return VALIDATION_NAMESPACE.VALIDATION_ERROR
        user = User_Class(user_type, user_name, user_pass)
        # Response
        response = user.check_if_user_exists()

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
            return REGISTRATION_NAMESPACE.REGISTRATION_ERROR
        new_user = User_Class(user_type, user_name, user_pass)
        # Response
        response = new_user.check_if_user_exists()
        if response == VALIDATION_NAMESPACE.UNKNOWN_USER:
            new_user.save_to_db()
            response = REGISTRATION_NAMESPACE.get_correct_registration_message(new_user.username)
        else:
            response = REGISTRATION_NAMESPACE.USERNAME_EXISTS

        return response
