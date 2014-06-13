#!/usr/bin/env python

from flask_script import Manager

from web import create_app
from config import app_config

app = create_app(app_config)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
