"""
Configures pytest and fixtures for tests in this package
"""
from flask_webtest import TestApp
import pytest

from src.app import create_app
from src.settings import TestConfig
from src.data.database import db as _db

def pytest_addoption(parser):
    """ Allows us to add --runslow as an argument to py.test so we can run tests marked slow """
    parser.addoption("--runslow", action="store_true", help="run slow tests")

def pytest_runtest_setup(item):
    """ Skip tests marked 'slow' unless we explicility asked to run them """
    if 'slow' in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")

@pytest.yield_fixture(scope='function')
def app():
    """
    Yields a flask app instance with an active request context.

    We need to do this to get access to the request object for making HTTP requests.
    See: http://flask.pocoo.org/docs/0.10/reqcontext/
    """
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    """
    Flask-Webtest TestApp provides convenient methods for writing high-level functional tests

    See:
    http://flask-webtest.readthedocs.org/en/latest/
    http://webtest.readthedocs.org/en/latest/
    """
    return TestApp(app)

@pytest.yield_fixture(scope='function')
def db():
    """
    Database fixture which creates/drop tables on setup/cleanup

    Useful for tests that need an empty database (e.g. testing mongo imports)
    """
    _db.create_all()

    yield _db

    _db.session.remove()
    _db.drop_all()
