from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_rest_jsonapi import Api

# Create the Flask application
app = Flask(__name__, instance_relative_config=True)

# Load the configuration from ./config.py
app.config.from_object('config')

# Load the configuration from ./instance/config.py (secret information)
app.config.from_pyfile('config.py')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Flask-REST-JSONAPI: register the api with the app
api = Api(app)

# Flask-REST-JSONAPI: Create endpoints
from .endpoints import create_api_endpoints
create_api_endpoints()
