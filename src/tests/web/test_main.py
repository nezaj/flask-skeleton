"""
Tests dashboard endpoints
"""
# from . import RoutesTest

import pytest

class TestMain:

    def test_hello(self, testapp):
        res = testapp.get('/')
        assert res.status_code == 200
