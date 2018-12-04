""" This is the main application module. """
from config import CONFIGURATION
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

APP = Flask(__name__)
BCRYPT = Bcrypt(APP)
LOGGIN_MANAGER = LoginManager(APP)

APP.secret_key = CONFIGURATION.secret_key
APP.config['SERVER_NAME'] = CONFIGURATION.get_server_name()

if __name__ == '__main__':
    APP.run(debug=CONFIGURATION.debug_mode,
            host=CONFIGURATION.backend_ip, port=CONFIGURATION.port)
