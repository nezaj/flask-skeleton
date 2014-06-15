"""
Database manager for performing database operations
"""
from flask_script import Manager, prompt_bool

from data.db import db_connect
from data.models import Base

db = db_connect()
manager = Manager(usage="Perform database operations")

@manager.command
def drop():
    "Drops database tables"
    print 'Connected to {}'.format(repr(db.engine.url))
    if prompt_bool("Are you sure you want to lose all your data"):
        Base.metadata.drop_all(db.engine)
        return 'Tables dropped'


@manager.command
def create():
    "Creates database tables from sqlalchemy models"
    print 'Connected to {}'.format(repr(db.engine.url))
    if prompt_bool("Are you sure you want to create the tables?"):
        Base.metadata.create_all(db.engine)
        return 'Tables created'

@manager.command
def recreate():
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    print 'Connected to {}'.format(repr(db.engine.url))
    if prompt_bool("Are you sure you want to recreate the database?"):
        Base.metadata.drop_all(db.engine)
        Base.metadata.create_all(db.engine)
        return 'Database re-created'
