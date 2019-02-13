""" Module containing unit tests for slot cluster module module. """
# Python libs.
import pytest
from unittest import mock
# Project Files.
from webmaps.models.slots_cluster import ParkingSlotsCluster


@pytest.fixture
def slot_cluster_mock():
    """ Return mock Placemark object. """
    with mock.patch.object(ParkingSlotsCluster, "__init__", lambda x: None):
        mock_obj = ParkingSlotsCluster()

        return mock_obj


@pytest.mark.parametrize("clusters, result", [
    [
        [[(1, 1), (2, 2), (3, 3)], [(1, 1), (2, 2)]],
        [[(1, 1), (2, 2), (3, 3)]]
    ],
    [
        [], []
    ],
    [
        [[]], [[]]
    ],
    [
        [[(1, 1), (2, 2), (3, 3)], [(1, 1), (2, 2), (3, 3)]],
        [[(1, 1), (2, 2), (3, 3)], [(1, 1), (2, 2), (3, 3)]]
    ]
])
def test_find_max_point_cluster(clusters, result, slot_cluster_mock):
    """ Test if max point clusters are returned correctly. """
    max_point_clusters = slot_cluster_mock._find_max_point_cluster(
        clusters)
    assert result == max_point_clusters
