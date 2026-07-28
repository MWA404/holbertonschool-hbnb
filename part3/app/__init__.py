from flask import Flask
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig

bcrypt = Bcrypt()


def create_app(config_class=DevelopmentConfig):
    """Application factory for Flask app configuration."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)

    # Register blueprints here as needed

    return app
