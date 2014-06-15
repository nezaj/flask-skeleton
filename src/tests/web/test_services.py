from . import RoutesTest

class ServicesRoutesTest(RoutesTest):

    def test_health(self):
        response = self.client.get('/health')
        assert response.status_code == 200
