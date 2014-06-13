"""
Logic for dashboard related routes
"""
from . import main

@main.route('/')
def index():
    return "Hello World!"
