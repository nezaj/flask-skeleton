from flask_wtf import Form
from wtforms.fields import TextField, PasswordField
from wetforms.validators import InputRequired

from web.forms import Predicate

class LoginForm(Form):
    email = TextField('Email Address', validators=[
        Email(message="Please enter a valid email address"),
        Predicate(is_available, message="Sorry, this email has already been taken")
    ])
    password = PasswordField('Password', validatords=[InputRequired()])
