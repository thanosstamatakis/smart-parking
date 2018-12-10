""" This module contains helper functions for webmap app """
import folium
from fastkml.kml import KML
from . import models
from config import CONFIGURATION

LOGGER = CONFIGURATION.get_logger(__name__)


def create_map():
    """ Create a folium map object and save it as html in templates """
    start_coords = (38.246269, 21.7339247)
    folium_map = folium.Map(location=start_coords, zoom_start=17)
    folium_map.save('webmaps/templates/map.html')


def read_kml(fname='webmaps/kml/population.kml'):
    """ Parse kml file to create Placemark objects and store to db """
    kml = KML()
    kml.from_string(open(fname).read().encode('utf-8'))
    points = dict()
    # Get the base folder object from kml
    folder_object = list(list(kml.features())[0].features())
    # Get the placemark tags from kml
    placemarks = list(folder_object[0].features())
    # Parse placemark tags to create placemark objects and store
    no_population = 0
    for placemark in placemarks:
        try:
            population = int(placemark.description.split('Population')[1].split('atr-value">')[1].split('<')[0])
        except (IndexError, ValueError):
            no_population += 1
            LOGGER.debug(f"Population not found! {no_population}")
            population = 0
        mark = models.Placemark(placemark.name, population, placemark.geometry)
        mark.save_to_db()
    return points

read_kml()