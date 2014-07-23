from sqlalchemy.orm import Query
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

from .pagination import Pagination

class BaseModel(object):
    """
    The base class for all of our database models.
    """

    @classmethod
    def columns(cls):
        "Returns all the columns on this model class."
        return cls.__table__.columns  # pylint: disable=E1101

    def _is_loaded(self, attr):
        "Whether an attribute on a model is loaded and unexpired."
        return attr not in self._sa_instance_state.unloaded

    @classmethod
    def get_defaults(cls, columns=None):
        """
        Returns a dict mapping the given columns to their default values.
        """
        columns = cls.columns() if columns is None else columns
        return {col: col.default for col in columns if col.default}

    def to_dict(self, columns=None):
        """
        Returns a dict mapping the given columns to their values.
        """
        columns = self.columns() if columns is None else columns
        return {col: getattr(self, col.key) for col in columns if self._is_loaded(col.key)}

    def _format_ctor(self, col_dict):
        """
        Prints a Python-constructor-like representation of this model
        with the provided attributes.
        """
        def format_assignment(col, value):
            return '{}={}'.format(col.key, repr(value))

        arglist = "{}".format(', '.join([format_assignment(*pair) for pair in col_dict.iteritems()]))
        return "{}({})".format(type(self).__name__, arglist)

    def __str__(self):
        key_columns = self.__mapper__.primary_key
        return self._format_ctor(self.to_dict(columns=key_columns))

    def __repr__(self):
        return self._format_ctor(self.to_dict())

class BaseQuery(Query):
    """
    A custom query object for supporting extra helpful operations
    in addition to SQLAlchemy's built-in Query object
    """

    def paginate(self, page=1, per_page=10, die=True):
        """
        Returns a Pagination object containing `per_page` items from page
        `page`. By default it will abort with 404 if no items were
        found and the page was larger than 1. This behavior can be
        disabled by setting `die` to `False`.
        """
        if die and page < 1:
            from flask import abort
            abort(404)

        items = self.limit(per_page).offset((page - 1) * per_page).all()

        if not items and page != 1 and die:
            from flask import abort
            abort(404)

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.count()

        return Pagination(self, page, per_page, total, items)

def named_declarative_base(**kwargs):
    """
    Returns a declarative base SQLAlchemy object with naming conventions
    for indexes, unique-keys, constraints, foreign-keys, and primary-keys.

    This is useful for altering tables. See below for details
    http://docs.sqlalchemy.org/en/rel_0_9/core/constraints.html#constraint-naming-conventions
    http://alembic.readthedocs.org/en/latest/tutorial.html#integration-of-naming-conventions-into-operations-autogenerate
    """
    convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    metadata = MetaData(naming_convention=convention)

    return declarative_base(metadata=metadata, **kwargs)

Base = named_declarative_base(cls=BaseModel)
