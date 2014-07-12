"""
Tests auth endpoints
"""
import pytest

from flask import url_for
from ..tools import generate_user

@pytest.fixture(scope='function')
def user(db):
    return generate_user(email="mock@example.com", password="mock").save(db.session)

class TestAuth:

    def test_login(self, user, client):
        # Go to login page
        res = client.get('/login', status=200)

        # Login form successfully submits and redirects
        login_form = res.forms['login-form']
        login_form['email'] = user.email
        login_form['password'] = "mock"
        res = login_form.submit().follow(status=200)

        # Login-form is no longer displayed
        with pytest.raises(KeyError):
            form = res.forms['login-form']
