""" This module contains File Parser models. """
# Python libs.
import os
from fastkml.kml import KML
from abc import ABC, abstractclassmethod
# Project files.
from config import CONFIGURATION
from webmaps.models.webmap import Polygon
# Python libs.
import werkzeug

LOGGER = CONFIGURATION.get_logger(__name__)
PROJECT_PATH = os.path.dirname(os.path.abspath('smart-parking'))


class FileParser(ABC):
    """ Abstruct Class for File Parsing. """

    def __init__(self, file_obj):
        """ Class constructor """
        self.file_obj = file_obj

    @abstractclassmethod
    def parse(self):
        """ Method responsible for parsing some kind of file. """
        pass

    def save_file(self):
        """ Method responsible for saving the file object. """
        file_name = werkzeug.utils.secure_filename(self.file_obj.filename)
        try:
            file_type = file_name.split('.')[1]
        except (IndexError, AttributeError):
            LOGGER.debug(f'{file_name} has no .')
            exit()
        file_path = f'webmaps/{file_type}/{file_name}'
        try:
            if not os.path.exists(os.path.realpath(file_path)):
                self.file_obj.save(file_path)
            self.file_obj = file_path
        except AttributeError:
            self.file_obj = f'webmaps/{file_type}/{file_type}_file.{file_type}'
            LOGGER.debug(f"File is not correct! Trying with {self.file_obj}")


class KmlParser(FileParser):
    """
    Class responsible for parsing kml file to create Placemark objects
    and store to db.
    """

    def __init__(self, kml_file):
        """ Class constructor """
        super().__init__(kml_file)

    def parse(self):
        """ Parse kml file and return the center of all polygons. """
        kml = KML()
        super().save_file()
        kml.from_string(open(self.file_obj).read().encode('utf-8'))
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

    def save_file(self):
        """ Method responsible for saving the kml file. """
        super().save_file()


class CsvParser(ABC):
    """ Class representing csv parser objects. """

    def __init__(self, csv_file):
        """ Class constructor. """
        super().__init__(csv_file)
