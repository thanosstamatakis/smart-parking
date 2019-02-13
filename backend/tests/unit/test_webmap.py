""" Module containing unit tests for webmap module. """
# Python libs.
import pytest
from unittest import mock
# Project Files.
from webmaps.models.webmap import Placemark


@pytest.fixture
def placemark_mock():
    """ Return mock Placemark object. """
    with mock.patch.object(Placemark, "__init__", lambda x: None):
        mock_obj = Placemark()
        return mock_obj


@pytest.mark.parametrize("coordinates, result", [
    ["GEOMETRYCOLLECTION (POINT (22.976145453676704 40.62219146058562), POLYGON((22.976357582114737 40.62222364922901, 22.976353346105217 40.622162077013606, 22.97632513171633 40.6220650814579, 22.976324245515375 40.62206512585228, 22.976245357036497 40.62207953299429, 22.97623578314317 40.62208881430964, 22.975974238516564 40.62218144737031, 22.97591321473136 40.62221276047412, 22.975893871647195 40.62224441073188, 22.975882819289783 40.62229962969202, 22.976357582114737 40.62222364922901)))",
     {'point': '(22.976145453676704 40.62219146058562)', 'polygon': '((22.976357582114737 40.62222364922901, 22.976353346105217 40.622162077013606, 22.97632513171633 40.6220650814579, 22.976324245515375 40.62206512585228, 22.976245357036497 40.62207953299429, 22.97623578314317 40.62208881430964, 22.975974238516564 40.62218144737031, 22.97591321473136 40.62221276047412, 22.975893871647195 40.62224441073188, 22.975882819289783 40.62229962969202, 22.976357582114737 40.62222364922901))'}],
    ["", {'point': 0, 'polygon': 0}]
])
def test_get_coordinates(coordinates, result, placemark_mock):
    """ Test coordinates sanitization in  placemark class. """
    # placemark_mock.coordinates = coordinates
    coordinates = placemark_mock._get_coordinates(coordinates)
    assert result == coordinates


@pytest.mark.parametrize("coordinates, result", [
    [{'point': '(22.956069973316676 40.603924767939965)',
      'polygon': '((22.95566481215897 40.604243345008896, 22.95621817837822 40.60427226675251, 22.956466690128675 40.6036162763744, 22.955940220474005 40.60356109847866, 22.95566481215897 40.604243345008896))'},
     "(22.95599094265977 40.60398726632467)"]
])
def test_get_centroid(coordinates, result, placemark_mock):
    """ Test centroid extraction and sanitization from coordinates. """
    placemark_mock.coordinates = coordinates
    centroid = placemark_mock._get_centroid()
    assert result == centroid
