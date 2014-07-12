"""
Tests home endpoints
"""
class TestHome:

    def test_index(self, client):
        res = client.get('/', status=200)
