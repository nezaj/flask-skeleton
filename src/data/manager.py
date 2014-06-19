"""
Database manager for performing database operations
"""
from flask_script import Manager, prompt_bool

from data.db import db

manager = Manager(usage="Perform database operations")

@manager.command
def drop():
    "Drops database tables"
    print 'Connected to {}'.format(repr(db.engine.url))
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print 'Tables dropped'


@manager.command
def create():
    "Creates database tables from sqlalchemy models"
    print 'Connected to {}'.format(repr(db.engine.url))
    if prompt_bool("Are you sure you want to create the tables?"):
        db.create_all()
        print 'Tables created'

@manager.command
def recreate():
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    print 'Connected to {}'.format(repr(db.engine.url))
    if prompt_bool("Are you sure you want to recreate the database?"):
        db.drop_all()
        db.create_all()
        print 'Database re-created'
