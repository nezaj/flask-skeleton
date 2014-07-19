from flask import (Blueprint, escape, flash, render_template,
                   redirect, request, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from .forms import ResetPasswordForm, EmailForm, LoginForm, RegistrationForm
from ..data.database import db
from ..data.models import User, UserPasswordToken
from ..data.util import generate_random_token
from ..decorators import reset_token_required
from ..emails import send_activation, send_password_reset
from ..extensions import login_manager

blueprint = Blueprint('auth', __name__)

@blueprint.route('/activate', methods=['GET'])
def activate():
    " Activation link for email verification "
    userid = request.args.get('userid')
    activate_token = request.args.get('activate_token')

    user = db.session.query(User).get(int(userid)) if userid else None
    if user and user.is_verified():
        flash("Your account is already verified.", 'info')
    elif user and user.activate_token == activate_token:
        user.update(verified=True)
        flash("Thank you for verifying your email. Your account is now activated", 'info')
        return redirect(url_for('public.index'))
    else:
        flash("Invalid userid/token combination", 'warning')

    return redirect(url_for('public.index'))

@blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if user:
            reset_value = UserPasswordToken.get_or_create_token(user.id).value
            send_password_reset(user, reset_value)
            flash("Passowrd reset instructions have been sent to {}. Please check your inbox".format(user.email),
                  'info')
            return redirect(url_for("public.index"))
        else:
            flash("We couldn't find an account with that email. Please try again", 'warning')
    return render_template("auth/forgot_password.tmpl", form=form)

@login_manager.user_loader
def load_user(userid):  # pylint: disable=W0612
    "Register callback for loading users from session"
    return db.session.query(User).get(int(userid))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully", "info")
            return redirect(request.args.get('next') or url_for('public.index'))
        else:
            flash("Invalid email/password combination", "danger")
    return render_template("auth/login.tmpl", form=form)

@blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('public.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User.create(**form.data)
        login_user(new_user)
        send_activation(new_user)
        flash("Thanks for signing up {}. Welcome!".format(escape(new_user.username)), 'info')
        return redirect(url_for('public.index'))
    return render_template("auth/register.tmpl", form=form)

@login_required
@blueprint.route('/resend_activation_email', methods=['GET'])
def resend_activation_email():
    if current_user.is_verified():
        flash("This account has already been activated.", 'warning')
    else:
        current_user.update(activate_token=generate_random_token())
        send_activation(current_user)
        flash('Activation email sent! Please check your inbox', 'info')

    return redirect(url_for('public.index'))

@blueprint.route('/reset_password', methods=['GET', 'POST'])
@reset_token_required
def reset_password(userid, user_token):
    user = db.session.query(User).get(userid)
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.update(password=form.password.data)
        user_token.update(used=True)
        flash("Password updated! Please log in to your account", "info")
        return redirect(url_for('public.index'))
    return render_template("auth/reset_password.tmpl", form=form)
