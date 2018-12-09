""" This module contains helper functions for webmap app """
import folium


def create_map():
    """ Create a folium map object and save it as html in templates """
    start_coords = (38.246269, 21.7339247)
    folium_map = folium.Map(location=start_coords, zoom_start=17)
    folium_map.save('webmaps/templates/map.html')
