#!/usr/bin/env python


from flask_script import Manager
from flask_script.commands import ShowUrls

from web import create_app
from data.db import db
from data.manager import manager as database_manager
from data import models
from config import app_config

app = create_app(app_config)
manager = Manager(app)

manager.add_command("db", database_manager)
manager.add_command("routes", ShowUrls())

def import_env():
    import os
    if os.path.exists('.env'):
        print 'Importing environment from .env...'
        for line in open('.env'):
            var = line.strip().split('=', 1)
            if len(var) == 2:
                os.environ[var[0]] = var[1]

@manager.shell
def make_context_shell():
    return dict(app=app, db=db, models=models)

if __name__ == '__main__':
    import_env()
    manager.run()
