"""
Generic test class for testing endpoints
"""
from unittest import TestCase

from web import create_app
from config import TestConfig

class RoutesTest(TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
