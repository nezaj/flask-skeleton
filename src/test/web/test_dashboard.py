"""
Tests dashboard endpoints
"""
from test.web import ViewTest

class DashboardTest(ViewTest):

    def test_hello(self):
        response = self.app.get('/')
        assert response.status_code == 200
