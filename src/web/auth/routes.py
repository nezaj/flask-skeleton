from flask import render_template

from . import auth
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return "Success!"
    return render_template("auth/login.tmpl", form=form)

@auth.route('/logout', methods=['GET'])
def logout():
    return "Logout page"
