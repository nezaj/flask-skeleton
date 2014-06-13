"""
Generic test class for testing endpoints
"""
from unittest import TestCase

from web import create_app
from config import app_config

class RoutesTest(TestCase):

    def setUp(self):
        self.app = create_app(app_config)
        self.client = self.app.test_client()
