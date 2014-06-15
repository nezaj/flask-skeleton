"""
Generic test class for testing database models
"""
from unittest import TestCase

from config import config_dict
from data.db import db_connect
from web import create_app

test_config = config_dict['test']
db = db_connect(test_config.SQLALCHEMY_DATABASE_URI)

class ModelTest(TestCase):

    def setUp(self):
        self.app = create_app(test_config)
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
