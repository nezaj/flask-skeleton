from datetime import datetime, timedelta

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, String, DateTime

from .user import User
from ..database import db
from ..mixins import CRUDModel
from ..util import generate_random_token

def tomorrow():
    return datetime.utcnow() + timedelta(days=1)

class UserPasswordToken(CRUDModel):
    __tablename__ = 'user_password_tokens'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)
    value = Column(String, nullable=False, index=True)
    used = Column(Boolean(name="used"), default=False)
    expiration_dt = Column(DateTime)

    # Use custom constructor
    # pylint: disable=W0231
    def __init__(self, **kwargs):
        self.expiration_dt = tomorrow()
        self.value = generate_random_token()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @hybrid_property
    def expired(self):
        return self.expiration_dt < datetime.utcnow()

    @hybrid_property
    def invalid(self):
        return self.used | self.expired

    @classmethod
    def invalid_tokens(cls, user_id):
        "Returns all invalid tokens for a user. A token is invalid if it has been used or has expired"
        return db.session.query(cls).filter(cls.user_id == user_id, cls.invalid)

    @classmethod
    def valid_token(cls, user_id):
        "Returns valid token for a user if it exists"
        return db.session.query(cls).filter(cls.user_id == user_id, ~cls.invalid).scalar()

    @classmethod
    def get_or_create_token(cls, user_id):
        invalid_tokens = UserPasswordToken.invalid_tokens(user_id)
        if invalid_tokens:
            invalid_tokens.delete(synchronize_session=False)
        token = UserPasswordToken.valid_token(user_id)
        return token if token else UserPasswordToken.create(user_id=user_id)
