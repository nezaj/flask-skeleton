from web import mail
from web.decorators import async

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
