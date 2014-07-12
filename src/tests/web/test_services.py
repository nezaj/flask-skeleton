import pytest

class TestServices:

    def test_health(self, client):
        res = client.get('/services/health', status=200)
