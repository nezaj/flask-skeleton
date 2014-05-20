"""
Generic test class for testing endpoints
"""
from unittest import TestCase

from web import app as flask_app

class ViewTest(TestCase):

    def setUp(self):
        self.app = flask_app.test_client()
