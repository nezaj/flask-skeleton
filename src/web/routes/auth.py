from flask import (Blueprint, current_app, escape, flash,
                   render_template, redirect, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from data.db import db
from data.models import User
from data.util import generate_activate_token
from web.forms.auth import LoginForm, RegistrationForm
from web.util import send_async_email

auth = Blueprint('auth', __name__)

def send_activation_email(new_user):
    current_app.logger.info("Begin sending activation email to {}...".format(new_user.email))

    msg = Message(subject="Confirm your account", recipients=[new_user.email])
    activate_link = url_for('auth.activate', userid=new_user.id, activate_token=new_user.activate_token, _external=True)
    msg.body = render_template('email/activate.txt', activate_link=activate_link)
    msg.html = render_template('email/activate.tmpl', activate_link=activate_link)

    # Hack to have access to app object outside of HTTP request. Useful so email can be sent async
    app = current_app._get_current_object()  # pylint: disable=W0212

    send_async_email(app, msg)
    current_app.logger.info("Activation email successfully sent to {}".format(new_user.email))

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

@login_required
@auth.route('/resend_activation_email', methods=['GET'])
def resend_activation_email():
    if current_user.is_verified():
        flash("This account has already been activated.", 'warning')
    else:
        current_user.update(db.session, activate_token=generate_activate_token())
        send_activation_email(current_user)
        flash('Activation email sent! Please check your inbox', 'info')

    return redirect(url_for('home.index'))

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
