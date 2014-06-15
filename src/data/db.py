from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import app_config
from data.models.base import BaseQuery

class DatabaseConnection(object):
    " A database connection "
    def __init__(self, url, **factory_args):
        self.engine = create_engine(url)
        self.session_factory = sessionmaker(bind=self.engine, query_cls=BaseQuery, **factory_args)
        self.session = scoped_session(self.session_factory)

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

def db_connect(db_url=app_config.SQLALCHEMY_DATABASE_URI):
    " Returns a DatabaseConnection object connected to the specified url "
    return DatabaseConnection(db_url)
