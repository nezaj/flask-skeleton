"""Defines fixtures available to all tests."""
import pytest
# from webtest import TestApp

from config import TestConfig
from web import create_app
from data.db import DatabaseConnection

@pytest.yield_fixture(scope='function')
def db():
    """Session-wide test database."""
    _db = DatabaseConnection(TestConfig.SQLALCHEMY_DATABASE_URI)
    _db.create_all()

    yield _db

    _db.session.remove()
    _db.drop_all()
