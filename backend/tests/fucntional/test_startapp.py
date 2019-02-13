""" Module for testing app initialization. """
# Python libs.
import pytest
import os
import redis
# Prject files.
from config import CONFIGURATION


def test_config_file():
    """ Test if config.yaml file exists in config folder. """
    relevant_path = 'config/config.yaml'
    abs_path = os.path.realpath(relevant_path)

    # Check if file exists.
    assert os.path.exists(abs_path)
    # Check if file is empty.
    assert os.stat(abs_path).st_size


def test_redis_running():
    """ Test if redis server is running. """
    redis_con = redis.Redis(
        host=CONFIGURATION.db_conn, decode_responses=True)

    assert redis_con.ping()
