"""
Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log-in to continue'
login_manager.login_message_category = 'warning'

from flask_mail import Mail
mail = Mail()

from flask_migrate import Migrate
migrate = Migrate()
