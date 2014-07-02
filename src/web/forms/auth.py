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
    " Only alphanumeric characters and dashes are allowed in usernames "
    if not username:
        return True
    return re.match(r'^[\w-]+$', username) is not None

class LoginForm(Form):
    email = TextField('Email Address', validators=[
        Email(message="Please enter a valid email address"),
        InputRequired(message="Email can't be blank")
    ])

    password = PasswordField('Password', validators=[
        InputRequired(message="Password can't be blank")
    ])

    remember_me = BooleanField('Keep me logged in')

class RegistrationForm(Form):
    username = TextField('Username', validators=[
        Predicate(username_is_safe, message="Usernames may only contain letters, numbers, and dashes."),
        Predicate(username_is_available, message="Sorry, this username has already been taken"),
        Length(min=4, max=25, message="Username must be between 4 and 25 characters"),
        InputRequired(message="Username can't be blank")
    ])

    email = TextField('Email Address', validators=[
        Predicate(email_is_available, message="Sorry, this email has already been taken"),
        Email(message="Please enter a valid email address"),
        InputRequired(message="Email can't be blank")
    ])

    password = PasswordField('Password', validators=[
        Length(max=25, message="Password can't be more than 25 characters"),
        Length(min=4, message="Password must be at least 4 characters"),
        InputRequired(message="Password can't be blank")
    ])
