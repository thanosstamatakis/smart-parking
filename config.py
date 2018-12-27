""" This module contains the Config class. """
import os.path
import yaml
import logging


class Config(object):
    """Configuration class for ci dashboard backend."""

    def __init__(self):
        """ Class constructor """
        if os.path.isfile('config/config.yaml'):
            config_dict = yaml.safe_load(open('config/config.yaml', 'r'))
            self.app_name = config_dict['backend']['app_name']
            self.secret_key = config_dict['backend']['secret_key']
            self.server_ip = config_dict['backend']['server_ip']
            self.backend_ip = config_dict['backend']['backend_ip']
            self.db_conn = config_dict['backend']['db_conn']
            self.port = config_dict['backend']['port']
            self.debug_mode = config_dict['backend']['debug_mode']
            self.logging_level = config_dict['logging']['level']
            self.logging_format = config_dict['logging']['format']
            self.logging_datefmt = config_dict['logging']['datefmt']

        else:
            print('No config yaml file found.')
            exit(1)

    def get_logger(self, module_name):
        """ Set up logging and return logger name """
        LOGGER = logging.getLogger(f'app:{module_name}')
        logging.basicConfig(format=self.logging_format, level=self.logging_level,
                            datefmt=self.logging_datefmt)

        return LOGGER

    def get_server_name(self):
        "Return the server name of the API server."
        return ':'.join([self.server_ip, str(self.port)])

    def get_server_url(self):
        "Return the url of the API server."
        return 'http://' + self.server_ip


CONFIGURATION = Config()
