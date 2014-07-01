from flask_wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Email, InputRequired, Length

from data.db import db
from data.models import User
from .util import Predicate

def email_is_available(email_address):
    if not email_address:
        return True
    return not User.find_by_email(db.session, email_address)

def username_is_available(username):
    if not username:
        return True
    return not User.find_by_username(db.session, username)

class LoginForm(Form):
    email = TextField('Email Address', validators=[Email(message="Please enter a valid email address")])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(Form):
    username = TextField('Username', validators=[
        InputRequired(),
        Length(min=4, max=25, message="Username must be between 4 and 25 characters"),
        Predicate(username_is_available, message="Sorry, this username has already been taken")
    ])
    email = TextField('Email Address', validators=[
        Email(message="Please enter a valid email address"),
        Predicate(email_is_available, message="Sorry, this email has already been taken")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password can't be blank")
    ])
