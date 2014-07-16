from flask import Flask

from .data.db import db
from .extensions import bcrypt, login_manager, mail
from .loggers import get_app_stderr_handler, configure_sqlalchemy_logger
from . import assets
from . import auth, public, services

def create_app(config_obj):
    " Factory for creating app "
    app = Flask(__name__)
    app.config.from_object(config_obj)
    register_loggers(app)
    initialize_app(app)
    register_extensions(app)
    register_blueprints(app)
    return app

def register_loggers(app):
    " Sets up app and sqlalchemy loggers "
    app.logger.handlers = []
    app.logger.setLevel(app.config["APP_LOG_LEVEL"])
    app.logger.addHandler(get_app_stderr_handler())
    configure_sqlalchemy_logger(app.config["STDERR_LOG_FORMAT"], level=app.config["SQLALCHEMY_LOG_LEVEL"])

def initialize_app(app):
    " Do any one-time initialization of the app prior to serving "
    app.static_folder = app.config['STATIC_DIR']

    @app.teardown_appcontext
    def remove_session(response):  # pylint: disable=W0612
        db.session.remove()
        return response

def register_extensions(app):
    " Configures flask extensions to be used with app"
    assets.register_assets(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    " Registers blueprint routes on app "
    app.register_blueprint(auth.views.bp)
    app.register_blueprint(public.views.bp)
    app.register_blueprint(services.views.bp, url_prefix="/services")
