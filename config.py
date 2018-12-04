"""This module contains the Config class"""
import os.path

import yaml


class Config(object):
    """Configuration class for ci dashboard backend."""

    def __init__(self):
        # To be removed after first deployment in the backend.
        # self.ip = 'http://sdl-ci-reporting.int.net.nokia.com'
        # self.db_conn = 'db0.local'
        if os.path.isfile('config/config.yaml'):
            config_dict = yaml.safe_load(open('config/config.yaml', 'r'))

            self.secret_key = config_dict['backend']['secret_key']
            self.server_ip = config_dict['backend']['server_ip']
            self.backend_ip = config_dict['backend']['backend_ip']
            self.port = config_dict['backend']['port']
            self.debug_mode = config_dict['backend']['debug_mode']

        else:
            print('No config yaml file found.')
            exit(1)

    def get_server_name(self):
        "Return the server name of the API server."
        return ':'.join([self.server_ip, str(self.port)])

    def get_server_url(self):
        "Return the url of the API server."
        return 'http://' + self.server_ip


CONFIGURATION = Config()
