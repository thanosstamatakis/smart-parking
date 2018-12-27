""" Module containing the base classes """
import logging
import redis
from config import CONFIGURATION

LOGGER = CONFIGURATION.get_logger(__name__)
redis_con = redis.Redis(host=CONFIGURATION.db_conn)


class Placemark():
    """ Class representing a placemark retrieved from KML file """

    def __init__(self, name, population, coordinates):
        """ Class constructor """
        self.name = str(name)
        self.coordinates = self.get_coordinates(coordinates)
        self.population = str(population)

    def get_coordinates(self, coordinates):
        """ Sanitize Placemark coordinates and return the corrected dict """
        return str(coordinates)

    def save_to_db(self):
        """ Save placemark to database """
        redis_key = 'placemark'
        redis_con.sadd(redis_key, self.name)
        LOGGER.debug(f'Add to key {redis_key}, set {self.name}')
        redis_key = ":".join((redis_key, self.name.split('.')[1]))
        hash_to_store = {'coordinates': self.coordinates, 'population': self.population}
        redis_con.hmset(
            redis_key, hash_to_store)
        LOGGER.debug(f'Add to key {redis_key}, hash {hash_to_store}')
        
