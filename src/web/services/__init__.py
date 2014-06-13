from flask import Blueprint

services = Blueprint('services', __name__)

from . import routes
