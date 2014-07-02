import os
import logging

from sqlalchemy.engine.url import URL

class Config(object):
    # controls whether web interfance users are in Flask debug mode
    # (e.g. Werkzeug stack trace console, unminified assets)
    DEBUG = False

    # Encryption key used to sign Flask session cookies
    # Generate a random one using os.urandom(24)
    SECRET_KEY = os.environ.get('APP_KEY')

    # Loggging
    APP_LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_LOG_LEVEL = logging.WARN
    STDERR_LOG_FORMAT = ('%(asctime)s %(levelname)s %(message)s', '%m/%d/%Y %I:%M:%S %p')

    # Location of db connection. Use in-memory db by default
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=None)

    # Useful directories
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    WEB_DIR = os.path.join(SRC_DIR, 'web')
    STATIC_DIR = os.path.join(WEB_DIR, 'static')

    # Location of alembic config file
    ALEMBIC_INI_PATH = os.path.join(SRC_DIR, 'alembic.ini')

    # Number of rounds for bcrypt hashing
    # timeit Bcrypt().generate_password_hash('some12uihr3', 3) ~ 1.49ms per loop
    BCRYPT_LOG_ROUNDS = 4

    # Mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD')

    INFO_ACCOUNT = 'info@flask-skeleton.herokuapp.com'
    TEST_RECIPIENT = os.environ.get('APP_TEST_RECIPIENT')  # Test account for recieving messages
    MAIL_DEFAULT_SENDER = INFO_ACCOUNT

class DevelopmentConfig(Config):
    ENV = 'dev'

    # Enable the flask debugger
    DEBUG = True

    # DB is located in web directory
    db_path = os.path.join(Config.WEB_DIR, 'dev.db')
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=db_path)

class TestConfig(Config):
    ENV = 'test'

    # Dummy secret key for running tests
    SECRET_KEY = 'test'

    # Don't want to see info messages about managing posts
    APP_LOG_LEVEL = logging.WARN

    # Use in-memory test database
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=None)

class ProductionConfig(Config):
    ENV = 'prod'

    # Don't need to see debug messages in production
    APP_LOG_LEVEL = logging.INFO

    # This must be defined in Heroku or locally
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Increase rounds for production instances
    # timeit Bcrypt().generate_password_hash('some12uihr3', 7) ~ 11.4ms per loop
    BCRYPT_LOG_ROUNDS = 7

config_dict = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestConfig,

    'default': DevelopmentConfig
}

app_config = config_dict[os.getenv('APP_ENV') or 'default']
