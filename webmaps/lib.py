""" This module contains helper functions for webmap app """
import folium
from fastkml.kml import KML
from . import models


def create_map():
    """ Create a folium map object and save it as html in templates """
    start_coords = (38.246269, 21.7339247)
    folium_map = folium.Map(location=start_coords, zoom_start=17)
    folium_map.save('webmaps/templates/map.html')


def read_kml(fname='webmaps/kml/population.kml'):
    kml = KML()
    kml.from_string(open(fname).read().encode('utf-8'))
    points = dict()
    features = list(kml.features())
    folder_object = list(features[0].features())
    placemarks = list(folder_object[0].features())
    for placemark in placemarks:
        mark = models.Placemark(placemark.name, placemark._geometry.geometry)
        mark.save_to_db()
    return points
