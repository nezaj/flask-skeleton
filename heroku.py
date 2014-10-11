#!/usr/bin/env python
"""
Used for serving the application via gunicorn in heroku.
See Procfile for commands
"""
from src.app import create_app
from src.settings import app_config

flask_app = create_app(app_config)
