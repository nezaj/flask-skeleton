from flask import (Blueprint, escape, flash, render_template,
                   redirect, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from data.db import db
from data.models import User, UserPasswordToken
from data.util import generate_random_token
from web.forms.auth import EmailForm, LoginForm, RegistrationForm
from .util import send_activation, send_password_reset

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
            reset_token = UserPasswordToken.get_or_create_token(db.session, user.id).token
            send_password_reset(user, reset_token)
            flash("Passowrd reset instructions have been sent to {}. Please check your inbox".format(user.email),
                  'info')
            return redirect(url_for("home.index"))
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
        send_activation(new_user)
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
        send_activation(current_user)
        flash('Activation email sent! Please check your inbox', 'info')

    return redirect(url_for('home.index'))

@auth.route('/reset_password', methods=['GET'])
def reset_password():
    userid = request.args.get('userid')
    reset_token = request.args.get('reset_token')

    user_token = db.session.query(UserPasswordToken).filter_by(token=reset_token).scalar()
    if user_token and user_token.user_id == userid and user_token.valid:
        user_token.update(db.session, is_used=True)
        flash("Success!")
    else:
        flash("This token is no longer valid.", 'warning')

    return redirect(url_for('home.index'))
