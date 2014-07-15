from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from .data.db import db
from .loggers import get_app_stderr_handler, configure_sqlalchemy_logger
from . import assets

# Initialize extensions to be used in create_app
login_manager = LoginManager()
mail = Mail()

# TODO: Hacky, import needs to come after extension initialization, fix this.
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

    # Set up app.logger to emit messages according to configuration
    app.logger.handlers = []
    app.logger.setLevel(app.config["APP_LOG_LEVEL"])
    app.logger.addHandler(get_app_stderr_handler())

    configure_sqlalchemy_logger(
        app.config["STDERR_LOG_FORMAT"],
        level=app.config["SQLALCHEMY_LOG_LEVEL"])

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
        from .data.models import User
        @login_manager.user_loader
        def load_user(userid):  # pylint: disable=W0612
            return db.session.query(User).get(int(userid))

    def register_flask_mail(app):
        mail.init_app(app)

    register_flask_login(app)
    register_flask_mail(app)

def register_blueprints(app):
    " Registers blueprint routes on app "
    app.register_blueprint(auth.views.bp)
    app.register_blueprint(public.views.bp)
    app.register_blueprint(services.views.bp, url_prefix="/services")
