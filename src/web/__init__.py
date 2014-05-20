import os
import logging

from flask import Flask
from config import app_config
from web import assets
from loggers import get_app_stderr_handler, configure_sqlalchemy_logger
from data.db import DatabaseConnection

class MyApp(Flask):

    db = None  # initialized later

    def __init__(self, config_obj):
        super(MyApp, self).__init__(__name__)
        self.config.from_object(config_obj)

def initialize_db(app):
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    app.db = DatabaseConnection(db_url)
    app.logger.info("Connected to {}".format(repr(app.db.engine.url)))

    @app.teardown_appcontext
    def remove_session(response):  # pylint: disable=W0612
        app.db.session.remove()
        return response

def initialize_app(app):
    " Do any one-time initialization of the app prior to serving "
    app.static_folder = app.config['STATIC_DIR']
    initialize_db(app)
    assets.register_assets(app)

def configure_loggers(app):
    " Sets up app and sqlalchemy loggers "

    # Set up app.logger to emit messages according to configuration
    app.logger.handlers = []
    app.logger.setLevel(app.config["APP_LOG_LEVEL"])
    app.logger.addHandler(get_app_stderr_handler())

    configure_sqlalchemy_logger(
        app.config["STDERR_LOG_FORMAT"],
        level=app.config["SQLALCHEMY_LOG_LEVEL"])

def create_app():
    " Factory for creating app "
    app = MyApp(app_config)
    configure_loggers(app)

    # big hack: if the Werkzeug reloader is going, then it decides to
    # restart the whole process as a subprocess in order to manage the
    # reloading, so create_app will run twice.

    # We can detect whether this is the "real" serving
    # process (the subprocess) by looking for the WERKZEUG_RUN_MAIN
    # environment variable, so make the execution of heavyweight
    # initialization code contingent on its presence.

    if os.environ.get('WERKZEUG_RUN_MAIN') or app.config['ENV'] == 'prod':
        initialize_app(app)

    return app

app = create_app()

# register routes (must happen after app creation since routes use global app binding)
from web import routes
routes.register_endpoints(app)
