#!/usr/bin/env python
"""
Launch script for heroku
"""
import os
from src.app import create_app
from src.settings import app_config

def import_env():
    if os.path.exists('.env'):
        print 'Importing environment from .env...'
        for line in open('.env'):
            var = line.strip().split('=', 1)
            if len(var) == 2:
                os.environ[var[0]] = var[1]

import_env()

flask_app = create_app(app_config)
