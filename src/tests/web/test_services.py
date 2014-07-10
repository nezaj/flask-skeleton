# from . import RoutesTest
import pytest

class TestServices:

    def test_health(self, testapp):
        res = testapp.get('/services/health')
        assert res.status_code == 200
