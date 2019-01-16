""" This is the main application module. """
from config import CONFIGURATION
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from webmaps import APP
from webmaps.modules import API

BCRYPT = Bcrypt(APP)
LOGGIN_MANAGER = LoginManager(APP)
CORS(APP)

APP.secret_key = CONFIGURATION.secret_key
APP.config['SERVER_NAME'] = CONFIGURATION.get_server_name()
API.init_app(APP)

if __name__ == '__main__':
    APP.run(debug=CONFIGURATION.debug_mode,
            host=CONFIGURATION.backend_ip, port=CONFIGURATION.port)
