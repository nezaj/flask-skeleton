#!/usr/bin/env python

"""
Usage: ./manage.py [submanager] <command>
Manage script for development. Type ./manage.py for more info
"""
import os

from flask_script import Manager
from flask_script.commands import ShowUrls
from flask_migrate import MigrateCommand as db_manager

from src.app import create_app
from src.settings import app_config
from src.data.base import Base
from src.data.database import db
from src.data import models
from src.util import invoke_process, parse_sqlalchemy_url

def import_env():
    if os.path.exists('.env'):
        print 'Importing environment from .env...'
        for line in open('.env'):
            var = line.strip().split('=', 1)
            if len(var) == 2:
                os.environ[var[0]] = var[1]

import_env()

app = create_app(app_config)
manager = Manager(app)
test_manager = Manager(usage='Performs test related operations')

manager.add_command('db', db_manager)
manager.add_command('test', test_manager)
manager.add_command("routes", ShowUrls())

@manager.shell
def make_context_shell():
    """
    Usage: ./manage.py shell
    Starts a python shell with with app, db and models loaded
    """
    # Loads all the models which inherit from Base
    models_map = {name: cls for name, cls in models.__dict__.items() if isinstance(cls, type(Base))}
    return dict(app=app, db=db, **models_map)

@db_manager.option('--url', dest='url', type=parse_sqlalchemy_url,
                   default=app.config['SQLALCHEMY_DATABASE_URI'],
                   help="A RFC1738 URL to a PostgreSQL or SQLite database to use.")
def repl(url):
    """
    Usage: ./manage.py db repl
    Launch a psql or sqlite3 repl connected to the database
    """
    def build_named_arglist(arg_dict):
        for name, value in arg_dict.iteritems():
            yield "--{}".format(name)
            yield str(value)

    dialect = url.get_dialect()
    if dialect.name == "postgresql":
        env = os.environ.copy()
        env["PGPASSWORD"] = url.password
        proc_args = list(build_named_arglist({
            'host': url.host,
            'port': url.port,
            'username': url.username,
            'dbname': url.database
        }))
        return invoke_process("psql", proc_args, env=env)
    elif dialect.name == "sqlite":
        proc_args = [url.database] if url.database else []
        return invoke_process("sqlite3", proc_args)
    else:
        raise argparse.ArgumentTypeError("Dialect {} is not supported.".format(dialect.name))

@test_manager.command
def test_email():
    """
    Usage: ./manage.py test email
    Send a test email -- useful for ensuring flask-mail is set up correctly
    """
    from flask_mail import Mail, Message
    mail = Mail(app)
    msg = Message(subject='test subject', recipients=[app.config['TEST_RECIPIENT']])
    msg.body = 'text body'
    msg.html = '<b>HTML</b> body'
    with app.app_context():
        mail.send(msg)

@test_manager.command
def scratch():
    """
    Usage: ./manage.py test scratch
    Run some snipper of code -- useful for quickly testing things
    """
    print 'Moop'

if __name__ == '__main__':
    manager.run()
