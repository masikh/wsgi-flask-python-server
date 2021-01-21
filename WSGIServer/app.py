import threading
import time
import yaml
from flask import Flask, session
from routes import *
from wsgiserver import WSGIServer
from flasgger import Swagger

template = {
    "swagger": "2.0",
    "info": {
        "title": "FLASK WSGI VUE TEMPLATE SERVER",
        "description": "Template server",
        "contact": {
            "responsibleOrganization": "masikh.org",
            "responsibleDeveloper": "Robert Nagtegaal",
            "email": "info@masikh.org",
            "url": "https://github.com/masikh",
        },
        "version": "version-3.0"
    },
    "host": "{HOSTIP}:8888".format(HOSTIP=Configuration.environment['flask']['ip_address']),
    "basePath": "",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "APIKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    },
    "security": [
        {
            "APIKeyAuth": []
        }
    ],
    "static_url_path": "/flasgger",
    "description": "FLASK WSGI TEMPLATE (vue app)",
    "operationId": "getmyData"
}


class ConfigClass(object):
    """ Flask application config
    """
    JSON_SORT_KEYS = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = 'QwErTy0192837465-{timestamp}'.format(timestamp=time.time())
    SWAGGER = {
        'title': 'Example WSI-Flask-server',
        'uiversion': 3
    }


class APIServer:
    def __init__(self, ip, port, cwd, debug=False):
        self.ip = ip
        self.port = port
        self.cwd = cwd
        self.debug = debug
        Configuration.global_parameters = self.__dict__
        self.app = Flask('WSGI-Flask Server on port: {port}'.format(port=self.port),
                         template_folder='{}/vue_web_code/dist'.format(self.cwd),
                         static_folder='{}/vue_web_code/dist'.format(self.cwd))
        self.http_server = None

        # Setup database and trigger Database.__enter__()
        self.database = Database()
        with self.database:
            pass

        # Start the API documentation services
        try:
            yaml.warnings({'YAMLLoadWarning': False})
        except Exception as error:
            print(error)
        Swagger(self.app, template=template)

        threading.Thread(target=self.run).start()

    def run(self):
        print('Starting WSGI-Flask Server on port: {port}'.format(port=self.port))
        print('API: http://{}:{}'.format(self.ip, self.port))
        self.app.config['JSON_SORT_KEYS'] = True
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        self.app.config['SECRET_KEY'] = str(time.time())

        self.app.config['DEBUG'] = True
        self.app.config['SESSION_COOKIE_HTTPONLY'] = True
        self.app.config['REMEMBER_COOKIE_HTTPONLY'] = True
        self.app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
        self.app.debug = True
        self.app.register_blueprint(routes)

        self.http_server = WSGIServer(self.app, host='0.0.0.0', port=self.port)
        self.http_server.start()

    def stop(self):
        self.http_server.stop()
