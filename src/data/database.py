from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from .base import Base, BaseQuery
from ..settings import app_config

class DatabaseConnection(object):
    " A database connection "
    def __init__(self, url, **factory_args):
        self.engine = create_engine(url)
        self.session_factory = sessionmaker(bind=self.engine, query_cls=BaseQuery, **factory_args)
        self.session = scoped_session(self.session_factory)

    def create_all(self):
        "Creates tables defined on Base metadata"
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        "Drops tables defined on Base metadata"
        Base.metadata.drop_all(self.engine)

    # Alembic configuration uses db.metadata to detect schema changes
    # pylint: disable=R0201
    @property
    def metadata(self):
        return Base.metadata

    @contextmanager
    def transient_session(self):
        "A shortcut for handling short-lived SQLAlchemy sessions."
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

db = DatabaseConnection(app_config.SQLALCHEMY_DATABASE_URI)
