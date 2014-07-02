class CRUDMixin(object):
    " Provides CRUD interface for models "

    @classmethod
    def create(cls, session, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(session, commit)

    def update(self, session, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        if commit:
            return self.save(session)
        return self

    def delete(self, session, commit=True):
        session.delete(self)
        if commit:
            session.commit()

    def save(self, session, commit=True):
        session.add(self)
        if commit:
            session.commit()
        return self
