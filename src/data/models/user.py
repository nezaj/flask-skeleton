from datetime import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.schema import Column
from sqlalchemy.types import Boolean, Integer, String, Text, DateTime

from .base import Base
from config import app_config

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(64),
                   nullable=False, unique=True, index=True,
                   doc="The user's email address.")
    username = Column(String(64),
                      nullable=False, unique=True, index=True,
                      doc="The user's username.")
    password_hash = Column(String(128))
    name = Column(String(64), index=True,
                  doc="The user's full name.")
    timezone = Column(String, nullable=False, server_default="US/Pacific",
                      doc="The tzdata timezone identifier that this user prefers to see.")
    bio = Column(Text)
    is_admin = Column(Boolean(name="is_admin"))
    member_since = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def find_by_email(session, email):
        return session.query(User).filter_by(email=email).scalar()

    @staticmethod
    def find_by_username(session, username):
        return session.query(User).filter_by(username=username).scalar()

    # pylint: disable=R0201
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, app_config.BCRYPT_LOG_ROUNDS)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
