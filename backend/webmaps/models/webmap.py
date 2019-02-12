""" Module containing webmap classes. """
# Python libs.
import logging
import redis
import re
import random as rand
from shapely.geometry import MultiPoint
# Project files.
from config import CONFIGURATION

LOGGER = CONFIGURATION.get_logger(__name__)
redis_con = redis.Redis(host=CONFIGURATION.db_conn, decode_responses=True)
COORDS_REGEX = re.compile(r'POINT\ (\([0-9. ]*\)),\ POLYGON([()0-9. ,]*)\)')


class Placemark():
    """ Class representing a placemark retrieved from KML file. """

    def __init__(self, name, population, coordinates):
        """ Class constructor """
        self.name = str(name).split('.')[1]
        self.coordinates = self._get_coordinates(coordinates)
        self.population = str(population)

    def _get_coordinates(self, coordinates):
        """ Sanitize Placemark coordinates and return the corrected dict. """
        try:
            point = re.search(COORDS_REGEX, str(coordinates)).group(1)
        except AttributeError:
            point = 0
        try:
            polygon = re.search(COORDS_REGEX, str(coordinates)).group(2)
        except AttributeError:
            polygon = 0
        # Returned dict.
        coordinates = {
            'point': point, 'polygon': polygon}

        return coordinates

    def _get_centroid(self):
        """ Extract centroid from coordinates. """
        new_list = []
        list1 = []
        # Get polygon points as a string.
        try:
            polygon_points = self.coordinates['polygon'].strip('()').split(',')
        except AttributeError:
            return '0'
        polygon_points_sanitized = []
        # Sanitize polygon points and add in.
        for point in polygon_points:
            polygon_points_sanitized.append(point.split(' '))
        # Add all points to returned list.
        for points in polygon_points_sanitized:
            for point in points:
                if point:
                    new_list.append(float(point))
            tuple1 = tuple(new_list)
            list1.append(tuple1)
            new_list = []

        return " ".join((str(MultiPoint(list1).centroid).split(' ')[1:]))

    def save_to_db(self):
        """ Save placemark to database. """
        # Save to placemark key set of placemark ids.
        redis_key = 'placemark'
        redis_con.sadd(redis_key, self.name)
        LOGGER.debug(f'Add to key {redis_key}, set {self.name}')
        # Save to placemark:<id> the hash of placemark attributes.
        redis_key = ":".join((redis_key, self.name))
        hash_to_store = {'point': self.coordinates['point'],
                         'polygon': self.coordinates['polygon'],
                         'population': self.population,
                         'centroid': self._get_centroid()}
        redis_con.hmset(
            redis_key, hash_to_store)
        LOGGER.debug(f'Add to key {redis_key}, hash {hash_to_store}')
        # Return the redis key placemark<id> to be used by children functions.

        return redis_key


class Polygon(Placemark):
    """ Class representing a polygon in map. """

    def __init__(self, name, population, coordinates, demand):
        """ Class constructor """
        super().__init__(name, population, coordinates)
        self.parking_slots = rand.randint(10, 50)
        self.demand = demand
        self.fixed_demand = self._get_fixed_demand()

    def save_to_db(self):
        """ Save polygon to database. """
        # Call to save to db from the Placemark's save_to_db funciton
        redis_key = ":".join((super().save_to_db(), 'polygon'))
        demands = self._check_for_demand()
        # Add values to key placemark:<id>:polygon
        polygon_values = (*demands.keys(), 'slots')
        redis_con.sadd(redis_key, *set(polygon_values))
        LOGGER.debug(f'Add to key {redis_key} set values {polygon_values}')
        # Add parking slots to key placemark:<id>:polygon:slots
        redis_key = ":".join((redis_key, 'slots'))
        redis_con.append(redis_key, str(self.parking_slots))
        LOGGER.debug(
            f'Add to key {redis_key} string value {self.parking_slots}')
        # Remove slots from key
        redis_key = ':'.join(redis_key.split(':')[:-1])
        # Add demands to keys placemark:<id>:polygon:(fixed_)demand
        for demand_key, demand_value in demands.items():
            temp_demand_key = ":".join((redis_key, demand_key))
            redis_con.lpush(temp_demand_key, *reversed(demand_value))
            LOGGER.debug(
                f'Add to key {temp_demand_key} list values {demand_value}')

    def _check_for_demand(self):
        """
        Check if demand and fixed demand is not None and return
        strigns of those not.
        """
        demands_dict = dict()
        if self.demand and self.fixed_demand:
            demands_dict = {'demand': self.demand,
                            'fixed_demand': self.fixed_demand}
        elif self.demand:
            demands_dict = {'demand': self.demand}
        elif self.fixed_demand:
            demands_dict = {'demand': self.fixed_demand}

        return demands_dict

    def _get_fixed_demand(self):
        """ Return fixed demand for the specific block. """
        fixed_demand = [0.2] * 24

        return fixed_demand
