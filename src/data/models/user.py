from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.schema import Column
from sqlalchemy.types import Boolean, Integer, String, Text, DateTime

from ..db import db
from ..mixins import CRUDModel
from ..util import generate_random_token
from ...settings import app_config
from ...extensions import bcrypt

class User(CRUDModel, UserMixin):
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
    activate_token = Column(String, nullable=False,
                            doc="Activation token for email verification")
    verified = Column(Boolean(name="verified"), nullable=False, default=False)
    is_admin = Column(Boolean(name="is_admin"))
    member_since = Column(DateTime, default=datetime.utcnow)

    # Use custom constructor
    # pylint: disable=W0231
    def __init__(self, **kwargs):
        self.activate_token = generate_random_token()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def find_by_email(email):
        return db.session.query(User).filter_by(email=email).scalar()

    @staticmethod
    def find_by_username(username):
        return db.session.query(User).filter_by(username=username).scalar()

    # pylint: disable=R0201
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password, app_config.BCRYPT_LOG_ROUNDS)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_verified(self):
        " Returns whether a user has verified their email "
        return self.verified is True
