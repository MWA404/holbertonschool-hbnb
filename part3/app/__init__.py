from flask import Flask
from config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    """Application factory for Flask app configuration."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints and extensions here as needed

    return app