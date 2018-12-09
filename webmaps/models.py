""" Module containing the base classes """
import logging
from config import CONFIGURATION

LOGGER = CONFIGURATION.get_logger(__name__)


class Placemark():
    """ Class representing a placemark retrieved from KML file """

    def __init__(self, name, coordinates):
        """ Class constructor """
        self.name = name
        self.coordinates = self.get_coordinates(coordinates)

    def get_coordinates(self, coordinates):
        """ Sanitize Placemark coordinates and return the corrected dict """
        return {coordinates}

    def save_to_db(self):
        """ Save placemark to database """
        LOGGER.debug("SAVED TO DB")
