""" This module is responsible for parsing kml """
# Python libs.
import os
from fastkml.kml import KML
# Project files.
from config import CONFIGURATION
from webmaps.models.webmap import Polygon

LOGGER = CONFIGURATION.get_logger(__name__)
PROJECT_PATH = os.path.dirname(os.path.abspath('smart-parking'))


class KmlParser():
    """
    Class responsible for parsing kml file to create Placemark objects,
    store to db and return the center of the map.
    """

    def __init__(self, kml_file):
        """ Class constructor """
        self.kml_file = kml_file

    def parse(self):
        kml = KML()
        self._save_file()
        kml.from_string(open(self.kml_file).read().encode('utf-8'))
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
            mark = Polygon(placemark.name, population,
                           placemark.geometry, 20, [1, 2, 3], [1, 1, 1])
            mark.save_to_db()
        for index, _ in enumerate(center):
            center[index] /= len(placemarks)

        return center

    def _save_file(self):
        """ Save kml file if it doesn't aleady exist. """
        try:
            if not os.path.exists(os.path.realpath('webmaps/kml/kml_file.kml')):
                self.kml_file.save('webmaps/kml/kml_file.kml')
            self.kml_file = 'webmaps/kml/kml_file.kml'
        except AttributeError:
            self.kml_file = 'webmaps/kml/population.kml'
            LOGGER.debug("File is not correct!")
