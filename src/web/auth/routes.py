from flask import flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm
from data.db import db
from data.models import User
from web import login_manager

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(db.session, form.email.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash("Logged in successfully")
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash("Invalid email/password combination")
    return render_template("auth/login.tmpl", form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for('main.index'))

@login_manager.user_loader
def load_user(userid):
    return db.session.query(User).get(int(userid))  # pylint: disable=E1101
