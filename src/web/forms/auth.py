import re

from flask_wtf import Form
from wtforms.fields import BooleanField, TextField, PasswordField
from wtforms.validators import Email, InputRequired, Length

from data.db import db
from data.models import User
from .util import Predicate

def email_is_available(email):
    if not email:
        return True
    return not User.find_by_email(db.session, email)

def username_is_available(username):
    if not username:
        return True
    return not User.find_by_username(db.session, username)

def username_is_safe(username):
    """
    Only letters (a-z), numbers, and periods are allowed in usernames.
    Based off Google username validator
    """
    if not username:
        return True
    return re.match(r'^[\w]+$', username) is not None

class LoginForm(Form):
    email = TextField('Email Address', validators=[
        Email(message="Please enter a valid email address"),
        InputRequired(message="You can't leave this empty")
    ])

    password = PasswordField('Password', validators=[
        InputRequired(message="You can't leave this empty")
    ])

    remember_me = BooleanField('Keep me logged in')

class RegistrationForm(Form):
    username = TextField('Choose your username', validators=[
        Predicate(username_is_safe, message="Please use only letters (a-z) and/or, numbers"),
        Predicate(username_is_available,
                  message="An account has already been registered with that username. Try another?"),
        Length(min=6, max=30, message="Please use between 6 and 30 characters"),
        InputRequired(message="You can't leave this empty")
    ])

    email = TextField('Your email address', validators=[
        Predicate(email_is_available, message="An account has already been reigstered with that email. Try another?"),
        Email(message="Please enter a valid email address"),
        InputRequired(message="You can't leave this empty")
    ])

    password = PasswordField('Create a password', validators=[
        Length(min=6, max=30, message="Please use between 6 and 30 characters"),
        InputRequired(message="You can't leave this empty")
    ])
