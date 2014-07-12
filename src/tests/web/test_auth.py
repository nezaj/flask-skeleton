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

        # Login link is no longer displayed. Logout link is displayed
        assert not res.html.find('a', href=url_for('auth.login'))
        assert res.html.find('a', href=url_for('auth.logout'))

    def test_logout(self, user, client):
        # Login
        res = client.post('/login', dict(
            email=user.email,
            password="mock")).follow()

        # After login, logout should be present and login is not
        assert not res.html.find('a', href=url_for('auth.login'))
        assert res.html.find('a', href=url_for('auth.logout'))

        # After logout, login should be present and logout not present
        res = client.get('/logout').follow(status=200)
        assert res.html.find('a', href=url_for('auth.login'))
        assert not res.html.find('a', href=url_for('auth.logout'))

    def test_register(self):
        # Goes to register page
        # Register form successfully submits and redirects
        # Registered user persists in the database
        # Registered user is not verified
        # activate token is created for registered user
        pass

    def test_user_activate(self):
        # Registers a user
        # Going to a bad user activation page redirects to index and shows a warning alert
        # Going to valid activation page redirects and shows info message
        # Registered user is now verified
        pass

    def test_forgot_password(self):
        # Goes to forgot password page
        # Submits bad email, renders warning alert and does not redirect
        # Submits good email, renders info alert and redirects to index
        # Generates a new UserPasswordToken associated with this user
        # Newly generated token is valid
        pass

    def test_reset_password(self):
        # Registers a user
        # Requests password reset
        # Goes to password reset page
        # Submits reset form
        # Old password is no longer valid
        # New password is valid
        # No more UserPasswordTokens exist for this user
        pass
