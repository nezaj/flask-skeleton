"""
Generic test class for testing database models
"""
from unittest import TestCase

from config import TestConfig
from data.db import DatabaseConnection
from web import create_app

db = DatabaseConnection(TestConfig.SQLALCHEMY_DATABASE_URI)

class ModelTest(TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
