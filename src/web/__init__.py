import os
import logging

from flask import Flask
from data.db import db
from loggers import get_app_stderr_handler, configure_sqlalchemy_logger
from web import assets

def register_blueprints(app):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .services import services as services_blueprint
    app.register_blueprint(services_blueprint)

def initialize_app(app):
    " Do any one-time initialization of the app prior to serving "
    # big hack: if the Werkzeug reloader is going, then it decides to
    # restart the whole process as a subprocess in order to manage the
    # reloading, so create_app will run twice.

    # We can detect whether this is the "real" serving
    # process (the subprocess) by looking for the WERKZEUG_RUN_MAIN
    # environment variable, so make the execution of heavyweight
    # initialization code contingent on its presence.
    if os.environ.get('WERKZEUG_RUN_MAIN') or app.config['ENV'] == 'prod':
        app.static_folder = app.config['STATIC_DIR']
        assets.register_assets(app)
    @app.teardown_appcontext
    def remove_session(response):  # pylint: disable=W0612
        db.session.remove()
        return response

def configure_loggers(app):
    " Sets up app and sqlalchemy loggers "

    # Set up app.logger to emit messages according to configuration
    app.logger.handlers = []
    app.logger.setLevel(app.config["APP_LOG_LEVEL"])
    app.logger.addHandler(get_app_stderr_handler())

    configure_sqlalchemy_logger(
        app.config["STDERR_LOG_FORMAT"],
        level=app.config["SQLALCHEMY_LOG_LEVEL"])

def create_app(config_obj):
    " Factory for creating app "
    app = Flask(__name__)
    app.config.from_object(config_obj)
    configure_loggers(app)
    initialize_app(app)
    register_blueprints(app)

    return app
