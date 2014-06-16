#!/usr/bin/env python

from flask_script import Manager

from web import create_app
from data import models
from data.db import db_connect
from data.manager import manager as database_manager
from config import app_config

db = db_connect()
app = create_app(app_config)
manager = Manager(app)

manager.add_command("database", database_manager)

@manager.shell
def make_context_shell():
    return dict(app=app, db=db, models=models)

if __name__ == '__main__':
    manager.run()
