from flask_wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Email, InputRequired

from data.db import db
from data.models import User
from web.forms import Predicate

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
    email = TextField('Email Address', validators=[
        Email(message="Please enter a valid email address"),
        Predicate(email_is_available, message="Sorry, an account has already been made with this email!")
    ])
    username = TextField('Email Address', validators=[
        InputRequired(),
        Predicate(email_is_available, message="Sorry, an account has already been made with this email!")
    ])
    password = PasswordField('Password', validators=[InputRequired()])
    password_confirm = PasswordField('Password Confirmation', validators=[InputRequired()])
