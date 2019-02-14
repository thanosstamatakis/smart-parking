""" Attaches the flask profiler """
from app import APP, CONFIGURATION
from werkzeug.contrib.profiler import ProfilerMiddleware

APP.config['PROFILE'] = True
APP.wsgi_app = ProfilerMiddleware(APP.wsgi_app, restrictions=[30])

if __name__ == '__main__':
    APP.run(debug=CONFIGURATION.debug_mode,
            host=CONFIGURATION.backend_ip, port=CONFIGURATION.port)
