from flask import Flask
from flask_restx import Api
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API Marketplace',
              doc='/api/v1/docs')


    return app
