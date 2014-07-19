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

    # Useful directories
    APP_DIR = os.path.dirname(os.path.abspath(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    STATIC_DIR = os.path.join(APP_DIR, 'static')

    # Number of rounds for bcrypt hashing
    # timeit Bcrypt().generate_password_hash('some12uihr3', 3) ~ 1.49ms per loop
    BCRYPT_LOG_ROUNDS = 4

    # Mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # The account used to authenticate gmail service
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD')

    # Mail accounts
    INFO_ACCOUNT = os.environ.get('APP_MAIL_INFO_ACCOUNT')
    TEST_RECIPIENT = os.environ.get('APP_TEST_RECIPIENT')
    MAIL_DEFAULT_SENDER = INFO_ACCOUNT

class DevelopmentConfig(Config):
    ENV = 'dev'
    DEBUG = True

    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=DB_PATH)

class TestConfig(Config):
    ENV = 'test'
    TESTING = True

    # Dummy secret key for running tests
    SECRET_KEY = 'test'

    # Don't want to see info messages about managing posts
    APP_LOG_LEVEL = logging.WARN

    # Use in-memory test database
    SQLALCHEMY_DATABASE_URI = URL(drivername='sqlite', database=None)

    # For faster testing
    BCRYPT_LOG_ROUNDS = 1

    # Allows form testing
    WTF_CSRF_ENABLED = False

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
