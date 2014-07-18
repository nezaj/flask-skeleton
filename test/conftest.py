"""Defines fixtures available to all tests."""
import pytest
from webtest import TestApp

from src.settings import TestConfig
from src.app import create_app
from src.data.database import db as _db

@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    """A Webtest app."""
    return TestApp(app)

@pytest.yield_fixture(scope='function')
def db():
    _db.create_all()

    yield _db

    _db.session.remove()
    _db.drop_all()
