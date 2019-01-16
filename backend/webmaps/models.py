""" Module containing the base classes """
import logging
import redis
import re
from webmaps import BCRYPT
from config import CONFIGURATION
from shapely.geometry import MultiPoint

LOGGER = CONFIGURATION.get_logger(__name__)
redis_con = redis.Redis(host=CONFIGURATION.db_conn, decode_responses=True)
COORDS_REGEX = re.compile(r'POINT\ (\([0-9. ]*\)),\ POLYGON([()0-9. ,]*)\)')


class Placemark():
    """ Class representing a placemark retrieved from KML file """

    def __init__(self, name, population, coordinates):
        """ Class constructor """
        self.name = str(name)
        self.coordinates = self.get_coordinates(coordinates)
        self.population = str(population)

    def get_coordinates(self, coordinates):
        """ Sanitize Placemark coordinates and return the corrected dict """
        try:
            point = re.search(COORDS_REGEX, str(coordinates)).group(1)
        except AttributeError:
            point = 0
        try:
            polygon = re.search(COORDS_REGEX, str(coordinates)).group(2)
        except AttributeError:
            polygon = 0

        coordinates = {
            'point': point, 'polygon': polygon}

        return coordinates

    def get_centroid(self):
        """ Extract centroid from coordinates """
        new_list = []
        list1 = []
        try:
            polygon_points = self.coordinates['polygon'].strip('()').split(',')
        except AttributeError:
            return '0'
        polygon_points_sanitized = []
        for point in polygon_points:
            polygon_points_sanitized.append(point.split(' '))
        for p in polygon_points_sanitized:
            for pi in p:
                if pi:
                    new_list.append(float(pi))
            tuple1 = tuple(new_list)
            list1.append(tuple1)
            new_list = []

        return " ".join((str(MultiPoint(list1).centroid).split(' ')[1:]))

    def save_to_db(self):
        """ Save placemark to database """
        redis_key = 'placemark'
        redis_con.sadd(redis_key, self.name)
        LOGGER.debug(f'Add to key {redis_key}, set {self.name}')
        redis_key = ":".join((redis_key, self.name.split('.')[1]))
        hash_to_store = {'point': self.coordinates['point'],
                         'polygon': self.coordinates['polygon'],
                         'population': self.population,
                         'centroid': self.get_centroid()}
        redis_con.hmset(
            redis_key, hash_to_store)
        LOGGER.debug(f'Add to key {redis_key}, hash {hash_to_store}')


class User():
    """ Class representing an App User. """

    def __init__(self, user_type, username, password):
        """ Class constructor """
        self.user_type = user_type
        self.username = username
        self.password = self._encrypt_password(password)

    def save_to_db(self):
        """ Store user credentials to db """
        # Save users number
        redis_key = 'users'
        users = redis_con.smembers(redis_key)
        if users:
            users_number = 1 + int(users[-1])

        else:
            users_number = 1
        redis_con.sadd(redis_key, str(users_number))
        LOGGER.debug(f'Save to key: {redis_key} : {users_number}')
        # Save users credentials
        redis_key = ":".join((redis_key, str(users_number)))
        user_dict = {'usertype': self.user_type,
                     'username': self.username, 'password': self.password}
        redis_con.hmset(
            redis_key, user_dict)
        LOGGER.debug(f'Save to key: {redis_key} : {user_dict}')

    def _encrypt_password(self, password):
        """ Returns user encrypted password"""
        pass_hash = BCRYPT.generate_password_hash(password, 10)
        return pass_hash
