from web import mail
from web.decorators import async

@async
def send_async_email(app, msg, success_str=None, fail_str=None):
    with app.app_context():
        try:
            mail.send(msg)
            if success_str:
                app.logger.info(success_str)
        except Exception:  # pylint: disable=W0703
            if fail_str:
                app.logger.info(fail_str)
