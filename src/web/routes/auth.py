from flask import (Blueprint, current_app, escape, flash,
                   render_template, redirect, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from data.db import db
from data.models import User
from data.util import generate_random_token, get_password_reset_token
from web.forms.auth import EmailForm, LoginForm, RegistrationForm
from .util import send_activation_email, send_password_reset_email

auth = Blueprint('auth', __name__)

@auth.route('/activate', methods=['GET'])
def activate():
    " Activation link for email verification "
    userid = request.args.get('userid')
    activate_token = request.args.get('activate_token')

    user = db.session.query(User).get(int(userid)) if userid else None
    if user and user.is_verified():
        flash("This account has already been activated.", 'warning')
    elif user and user.activate_token == activate_token:
        user.update(db.session, verified=True)
        flash("Thank you for verifying your email. Your account is now activated", 'info')
        return redirect(url_for('home.index'))
    else:
        flash("Invalid userid/token combination", 'warning')

    return redirect(url_for('home.index'))

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.find_by_email(db.session, form.email.data)
        if user:
            reset_token = get_password_reset_token(user)
            send_password_reset_email(user, reset_token)
            return render_template("auth/password_token_sent", user_email=user.email)
        else:
            flash("We couldn't find an account with that email. Please try again", 'warning')
    return render_template("auth/forgot_password.tmpl", form=form)

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

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('home.index'))

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

@login_required
@auth.route('/resend_activation_email', methods=['GET'])
def resend_activation_email():
    if current_user.is_verified():
        flash("This account has already been activated.", 'warning')
    else:
        current_user.update(db.session, activate_token=generate_random_token())
        send_activation_email(current_user)
        flash('Activation email sent! Please check your inbox', 'info')

    return redirect(url_for('home.index'))
