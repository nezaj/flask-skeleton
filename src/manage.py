#!/usr/bin/env python

from flask_script import Manager, Shell

from web import create_app
from data import models
from data.db import db_connect
from config import app_config

app = create_app(app_config)
manager = Manager(app)
db = db_connect()

@manager.shell
def make_context_shell():
    return dict(app=app, db=db, models=models)

if __name__ == '__main__':
    manager.run()
