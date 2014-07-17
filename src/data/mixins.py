from .db import db

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
