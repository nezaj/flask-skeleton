from flask import (Blueprint, current_app, escape, flash,
                   render_template, redirect, request, url_for)
from flask_login import login_required, login_user, logout_user
from flask_mail import Message

from data.db import db
from data.models import User
from web.forms.auth import LoginForm, RegistrationForm
from web.util import send_async_email

auth = Blueprint('auth', __name__)

def send_activation_email(new_user):
    current_app.logger.info("Begin sending activation email to {}...".format(new_user.email))

    msg = Message(subject="confirm your account", recipients=[new_user.email])
    msg.body = render_template('email/activate.txt')
    msg.html = render_template('email/activate.tmpl')

    # Hack to have access to app object outside of HTTP request. Useful so email can be sent async
    app = current_app._get_current_object()  # pylint: disable=W0212

    send_async_email(app, msg)
    current_app.logger.info("Activation email successfully sent to {}".format(new_user.email))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(db.session, form.email.data)
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully", "info")
            return redirect(request.args.get('next') or url_for('home.index'))
        else:
            flash("Invalid email/password combination", "danger")
    return render_template("auth/login.tmpl", form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User.create(db.session, **form.data)
        login_user(new_user)
        send_activation_email(new_user)
        flash("Thanks for signing up {}. Welcome!".format(escape(new_user.username)), 'info')
        return redirect(url_for('home.index'))
    return render_template("auth/register.tmpl", form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('home.index'))
