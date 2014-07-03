from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Boolean, Integer, String, DateTime

from .base import Base
from .mixins import CRUDMixin
from .user import User
from data.util import generate_random_token

def tomorrow():
    return datetime.utcnow() + timedelta(seconds=30)

class UserPasswordToken(Base, CRUDMixin):
    __tablename__ = 'user_password_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship(User)
    token = Column(String, nullable=False, default=generate_random_token)
    is_used = Column(Boolean(name="used"), default=False)
    expiration_dt = Column(DateTime, default=tomorrow())
    expired = (expiration_dt != None) & (expiration_dt < func.now())
