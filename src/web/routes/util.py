from flask import current_app, url_for, render_template
from flask_mail import Message
from web.util import send_async_email

def send_activation(new_user):
    current_app.logger.info("Begin sending activation email to {}...".format(new_user.email))

    activate_link = url_for('auth.activate', userid=new_user.id, activate_token=new_user.activate_token, _external=True)

    msg = Message(subject="Confirm your account", recipients=[new_user.email])
    msg.body = render_template('email/activate.txt', activate_link=activate_link)
    msg.html = render_template('email/activate.tmpl', activate_link=activate_link)

    # Hack to have access to app object outside of HTTP request. Useful so email can be sent async
    app = current_app._get_current_object()  # pylint: disable=W0212
    success = "Activation email successfuly sent to {}".format(new_user.email)
    failure = "Activation email failed to send to {}".format(new_user.email)
    send_async_email(app, msg, success, failure)

def send_password_reset(user, reset_token):
    current_app.logger.info("Begin sending password resend email to {}...".format(user.email))

    reset_link = url_for('auth.reset_password', userid=user.id, reset_token=reset_token, _external=True)

    msg = Message(subject="Reset your password", recipients=[user.email])
    msg.body = render_template('email/password_reset.txt', reset_link=reset_link)
    msg.html = render_template('email/password_reset.tmpl', reset_link=reset_link)

    # Hack to have access to app object outside of HTTP request. Useful so email can be sent async
    app = current_app._get_current_object()  # pylint: disable=W0212
    success = "Password reset email successfuly sent to {}".format(user.email)
    failure = "Password reset email failed to send to {}".format(user.email)
    send_async_email(app, msg, success, failure)
