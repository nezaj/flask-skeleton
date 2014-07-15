"""
Tests public endpoints
"""
from flask import url_for

class TestPublic:

    def test_index(self, client):
        res = client.get(url_for('public.index'), status=200)
