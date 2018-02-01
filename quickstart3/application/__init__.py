from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_rest_jsonapi import Api


# Initialize SQLAlchemy
db = SQLAlchemy()

# Flask-REST-JSONAPI: initialize api
api = Api()

def create_app(config_class=Config):
    """Factory function to create the application"""

    # Create the Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Load the configuration from ./config.py
    # Note: Potentially overwritten by TestConfig class during unit testing
    app.config.from_object(config_class)

    # Load the configuration from ./instance/config.py (secret information)
    app.config.from_pyfile('config.py')

    # now we have the application, we initialize all the Flask extensions
    db.init_app(app)
    api.init_app(app)

    # Register all blueprints with the application
    from application.api_bp import api_bp
    app.register_blueprint(api_bp)
    #app.register_blueprint(api_bp, url_prefix='/api')


    return app



# Flask-REST-JSONAPI: Create endpoints
from .api_bp.endpoints import create_api_endpoints
create_api_endpoints()
