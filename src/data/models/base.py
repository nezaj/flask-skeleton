from sqlalchemy.orm import Query
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

from data.pagination import Pagination

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
        disabled by setting `die` to `False`. If sort_attr and
        sort_dir are specified, then order the items appropriately.
        If search_cols and search_query are specified, then only
        return items where the given cols match the query string.
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

Base = named_declarative_base()
