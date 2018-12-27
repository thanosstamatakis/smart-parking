""" This module contains helper functions for webmap app """
import os

import folium
from config import CONFIGURATION
from fastkml.kml import KML

from . import models

LOGGER = CONFIGURATION.get_logger(__name__)


def create_map():
    """ Create a folium map object and save it as html in templates """
    if not os.path.exists('webmaps/templates/map.html'):
        LOGGER.debug('CREATED NEW PATH')
        center = read_kml()
        start_coords = tuple(center)
        folium_map = folium.Map(location=start_coords, zoom_start=17)
        folium_map.save('webmaps/templates/map.html')


def read_kml(fname='webmaps/kml/population.kml'):
    """
    Parse kml file to create Placemark objects, 
    store to db and return the center of the map
    """
    kml = KML()
    kml.from_string(open(fname).read().encode('utf-8'))
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
        center[1] += placemark.geometry._geoms[0]._coordinates[0]
        center[0] += placemark.geometry._geoms[0]._coordinates[1]
        mark = models.Placemark(placemark.name, population, placemark.geometry)
        mark.save_to_db()
    for index, _ in enumerate(center):
        center[index] /= len(placemarks)
    return center
