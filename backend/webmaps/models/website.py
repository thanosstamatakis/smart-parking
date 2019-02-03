""" Module containing webiste classes. """
# Python libs.
import logging
import redis
# Project files.
from webmaps import BCRYPT
from config import CONFIGURATION

LOGGER = CONFIGURATION.get_logger(__name__)
redis_con = redis.Redis(host=CONFIGURATION.db_conn, decode_responses=True)


class User():
    """ Class representing an App User. """

    def __init__(self, user_type, username, password):
        """ Class constructor """
        self.user_type = user_type
        self.username = username
        self.password = password

    def check_if_user_exists(self):
        """ Check if user is stored already in db and return according message. """
        user_valid = {'user_name': False, 'password': False}
        user_numbers = redis_con.smembers('users')
        if not user_numbers:
            return "User does not exist"
        for user_number in user_numbers:
            temp_username = str(redis_con.hget(
                ":".join(('users', str(user_number))), 'username'))
            if temp_username == self.username:
                user_valid['user_name'] = True
            usr_pass = redis_con.hget(
                ":".join(('users', str(user_number))), 'password')
            if usr_pass and BCRYPT.check_password_hash(usr_pass, self.password):
                user_valid['password'] = True
        if list(user_valid.values()) == [True, True]:
            return 'User exists in DB'
        elif list(user_valid.values()) == [True, False]:
            return 'Wrong Password'
        else:
            return 'User does not exist'

    def _encrypt_password(self, password):
        """ Returns user encrypted password"""
        pass_hash = BCRYPT.generate_password_hash(password, 10)
        return pass_hash

    def save_to_db(self):
        """ Store user credentials to db """
        # Save users number
        enc_password = self._encrypt_password(self.password)
        redis_key = 'users'
        users = redis_con.smembers(redis_key)
        users = list(users)
        if users:
            users_number = 1 + len(users)
        else:
            users_number = 1

        redis_con.sadd(redis_key, str(users_number))
        LOGGER.debug(f'Save to key: {redis_key} : {users_number}')
        # Save users credentials
        redis_key = ":".join((redis_key, str(users_number)))
        user_dict = {'usertype': self.user_type,
                     'username': self.username, 'password': enc_password}
        redis_con.hmset(
            redis_key, user_dict)
        LOGGER.debug(f'Save to key: {redis_key} : {user_dict}')
