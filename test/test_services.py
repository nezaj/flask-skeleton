from flask import url_for

class TestServices:

    def test_health(self, client):
        res = client.get(url_for('services.health'), status=200)

    def test_forbidden(self, client):
        res = client.get(url_for('services.forbidden'), status=403)
        assert 'Forbidden' in res.html.title.text

    def test_internal_error(self, client):
        res = client.get(url_for('services.internal_error'), status=500)
        assert 'Internal Error' in res.html.title.text

    def test_not_found(self, client):
        res = client.get(url_for('services.not_found'), status=404)
        assert 'Not Found' in res.html.title.text

    def test_unauthorized(self, client):
        res = client.get(url_for('services.unauthorized'), status=401)
        assert 'Unauthorized' in res.html.title.text
