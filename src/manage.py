#!/usr/bin/env python

import os
if os.path.exists('.env'):
    print 'Importing environment from .env...'
    for line in open('.env'):
        var = line.strip().split('=', 1)
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from flask_script import Manager

from web import create_app
from data import models
from data.db import db
from data.manager import manager as database_manager
from config import app_config

app = create_app(app_config)
manager = Manager(app)

manager.add_command("db", database_manager)

@manager.shell
def make_context_shell():
    return dict(app=app, db=db, models=models)

if __name__ == '__main__':
    manager.run()
