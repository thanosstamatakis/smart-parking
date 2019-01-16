""" This module is responsible for parsing kml """
import os

from config import CONFIGURATION
from fastkml.kml import KML

from . import models

LOGGER = CONFIGURATION.get_logger(__name__)
PROJECT_PATH = os.path.dirname(os.path.abspath('smart-parking'))


def read_kml(file):
    """
    Parse kml file to create Placemark objects, 
    store to db and return the center of the map
    """
    kml = KML()
    try:
        file.save('webmaps/kml/kml_file.kml')
        file = 'webmaps/kml/kml_file.kml'
    except AttributeError:
        file = 'webmaps/kml/population.kml'
        LOGGER.debug("File is not correct!")

    kml.from_string(open(file).read().encode('utf-8'))
    center = [0, 0]
    # Get the base folder object from kml
    folder_object = list(list(kml.features())[0].features())
    # Get the placemark tags from kml
    placemarks = list(folder_object[0].features())
    # Parse placemark tags to create placemark objects and store
    no_population = 0
    for placemark in placemarks:
        try:
            population = int(placemark.description.split('Population')[
                             1].split('atr-value">')[1].split('<')[0])
        except (IndexError, ValueError):
            no_population += 1
            LOGGER.debug(f"Population not found! {no_population}")
            population = 0
        try:
            center[1] += placemark.geometry._geoms[0]._coordinates[0]
            center[0] += placemark.geometry._geoms[0]._coordinates[1]
        except AttributeError:
            center[1] += 0
            center[0] += 0
        mark = models.Placemark(placemark.name, population, placemark.geometry)
        mark.save_to_db()
    for index, _ in enumerate(center):
        center[index] /= len(placemarks)
    return center
