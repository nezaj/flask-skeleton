"""
Services endpoints
"""
from flask import Blueprint

services = Blueprint('services', __name__)

@services.route('/health')
def health():
    return "All is well :)"
