from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from data.db import db
from data.models import User
from web.forms.auth import LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(db.session, form.email.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash("Logged in successfully", "info")
            return redirect(request.args.get('next') or url_for('home.index'))
        else:
            flash("Invalid email/password combination", "danger")
    return render_template("auth/login.tmpl", form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('home.index'))
