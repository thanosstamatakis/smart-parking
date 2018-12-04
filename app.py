from webmaps import app
from config import CONFIGURATION
from flask import Flask

APP = Flask(__name__)
# APP.secret_key = CONFIGURATION.secret_key
APP.config['SERVER_NAME'] = CONFIGURATION.get_server_name()

if __name__ == '__main__':
    APP.run(debug=CONFIGURATION.debug_mode,
            host=CONFIGURATION.backend_ip, port=CONFIGURATION.port)
