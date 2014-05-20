"""
Tests services endpoints
"""
from test.web import ViewTest

class ServicesTest(ViewTest):

    def test_health(self):
        response = self.app.get('/health')
        assert response.status_code == 200

