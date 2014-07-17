"""
Tests auth endpoints
"""
import pytest

from src.data.models import User, UserPasswordToken
from flask import url_for
from .generate import generate_user
from .util import fill_register_form, login_el, logout_el

@pytest.fixture(scope='function')
def user(db):
    return generate_user(email="mock@example.com", password="mock").save()

class TestAuth:

    def test_login(self, user, client):
        # Go to login page
        res = client.get(url_for('auth.login'), status=200)

        # Login form successfully submits and redirects
        login_form = res.forms['login-form']
        login_form['email'] = user.email
        login_form['password'] = "mock"
        res = login_form.submit().follow()

        # Login-form is no longer displayed
        assert not res.forms.get('login-form')

        # Login link is no longer displayed. Logout link is displayed
        assert not login_el(res)
        assert logout_el(res)

    def test_logout(self, user, client):
        # Login
        res = client.post('/login', dict(
            email=user.email,
            password="mock")).follow()

        # After logout, login should be present and logout not present
        res = client.get('/logout').follow()
        assert login_el(res)
        assert not logout_el(res)

    def test_register(self, client, db):
        # Go to register page
        res = client.get(url_for('auth.register'), status=200)

        # Register form successfully submits and redirects
        user = User(email="joejoe@example.com", username='joejoe')
        form = fill_register_form(res.forms['register-form'], user)
        res = form.submit().follow()

        # Register-form is no longer displayed
        assert not res.forms.get('register-form')

        # Registered user persists in the database
        assert User.find_by_email(user.email)

        # Cannot register same user twice. Register-form should still be displayed
        res = client.get(url_for('auth.register'), status=200)
        res = fill_register_form(res.forms['register-form'], user).submit()
        assert res.forms['register-form']

    def test_user_activate(self, client, db):
        # Registers a user
        res = client.get(url_for('auth.register'), status=200)
        user = User(email="joejoe@example.com", username='joejoe')
        form = fill_register_form(res.forms['register-form'], user)
        res = form.submit().follow()

        # Registered user is not verified
        user = User.find_by_email(user.email)
        assert not user.verified

        # Activate token is created for registered user
        assert user.activate_token

        # An invalid user/token combination does not verify the user
        res = client.get(url_for('auth.activate', userid=user.id, activate_token="moop"))
        assert not user.verified

        # A valid user/token combination verifies the user
        res = client.get(url_for('auth.activate', userid=user.id, activate_token=user.activate_token))
        assert user.verified

    def test_forgot_password(self, client, db, user):
        # User has no valid reset tokens initially
        assert not UserPasswordToken.valid_token(user.id)

        # Go to forgot password page
        res = client.get(url_for('auth.forgot_password'), status=200)

        # Submits bad email, forgot-form is still displayed
        res.forms['forgot-form']['email'] = 'moop'
        res = res.forms['forgot-form'].submit()
        assert res.forms.get('forgot-form')

        # Submits good email, forgot-form is no longer displayed
        res.forms['forgot-form']['email'] = user.email
        res = res.forms['forgot-form'].submit()
        assert not res.forms.get('forgot-form')

        # User now has a valid UserPasswordToken
        assert UserPasswordToken.valid_token(user.id)

    def test_reset_password(self, client, db, user):
        # Requests password reset
        client.post(url_for('auth.forgot_password'),
                          dict(email=user.email)).follow()

        # User has valid UserPasswordToken
        valid_token = UserPasswordToken.valid_token(user.id)
        assert valid_token

        # Invalid user/token combo does not display reset form
        res = client.get(url_for('auth.reset_password', userid=user.id, reset="moop"))
        assert not res.forms.get('reset-form')

        # Valid user/token combo displays reset form
        res = client.get(url_for('auth.reset_password', userid=user.id, value=valid_token.value))
        assert res.forms.get('reset-form')

        # Password is changed on form submit
        reset_form = res.forms.get('reset-form')
        reset_form['password'] = 'joejoe'
        reset_form['confirm'] = 'joejoe'
        reset_form.submit()
        assert user.verify_password('joejoe')

        # User has no more valid UserPasswordToken
        assert not UserPasswordToken.valid_token(user.id)

        # Previous valid token no longer works. Does not display reset form
        res = client.get(url_for('auth.reset_password', userid=user.id, value=valid_token.value))
        assert not res.forms.get('reset-form')
