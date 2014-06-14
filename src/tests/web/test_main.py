"""
Tests dashboard endpoints
"""
from . import RoutesTest

class MainRoutesTest(RoutesTest):

    def test_hello(self):
        response = self.client.get('/')
        assert response.status_code == 200
