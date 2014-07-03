import os
import logging

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from config import app_config
from data.db import db
from loggers import get_app_stderr_handler, configure_sqlalchemy_logger
from web import assets

# Initialize extensions to be used in create_app
login_manager = LoginManager()
mail = Mail()

class MyApp(Flask):
    def __init__(self, config_obj):
        super(MyApp, self).__init__(__name__)
        self.config.from_object(config_obj)

def register_blueprints(app):
    " Registers blueprint routes on app "
    from .routes import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import services as services_blueprint
    app.register_blueprint(services_blueprint, url_prefix="/services")

def initialize_app(app):
    " Do any one-time initialization of the app prior to serving "
    app.static_folder = app.config['STATIC_DIR']
    assets.register_assets(app)

    @app.teardown_appcontext
    def remove_session(response):  # pylint: disable=W0612
        db.session.remove()
        return response

def register_extensions(app):
    " Configures flask extensions to be used with app"

    def register_flask_login(app):
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'
        login_manager.login_message = 'Please log-in to continue'
        login_manager.login_message_category = 'warning'

        # Register callback for loading users from session
        from data.models import User
        @login_manager.user_loader
        def load_user(userid):  # pylint: disable=W0612
            return db.session.query(User).get(int(userid))

    def register_flask_mail(app):
        mail.init_app(app)

    register_flask_login(app)
    register_flask_mail(app)

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
    app = MyApp(config_obj)
    configure_loggers(app)
    initialize_app(app)
    register_extensions(app)
    register_blueprints(app)

    return app
