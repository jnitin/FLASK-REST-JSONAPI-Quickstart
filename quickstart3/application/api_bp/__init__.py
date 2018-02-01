from flask import Blueprint

api_bp = Blueprint('api_bp', __name__)

from application.api_bp import endpoints, schemas, resource_managers
