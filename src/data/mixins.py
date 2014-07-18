from sqlalchemy.schema import Column
from sqlalchemy.types import Integer

from .base import Base
from .database import db

class CRUDMixin(object):
    " Provides CRUD interface for models "

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """
    A mixin that adds a surrogate integer 'primary key' column named
    `id` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    # We `id` to be the column name
    # pylint: disable=W0622
    id = Column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any((isinstance(id, basestring) and id.isdigit(),
                isinstance(id, (int, float))),):
            return db.session.query(cls).get(int(id))
        return None

class CRUDModel(Base, CRUDMixin, SurrogatePK):
    """Model class that includes CRUD convenience methods"""
    __abstract__ = True
