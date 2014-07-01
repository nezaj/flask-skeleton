"""
Code for easy pagination in queries and views, thanks to
Flask-SQLAlchemy (https://github.com/mitsuhiko/flask-sqlalchemy).
"""

from math import ceil

class Pagination(object):

    # pylint: disable=R0913
    def __init__(self, query, page, per_page, total, items):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        """The total number of pages."""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def start(self):
        """The index of the first item in this page."""
        return ((self.page - 1) * self.per_page) + 1

    @property
    def end(self):
        """The index of the last item in this page."""
        return self.total if self.page == self.pages else self.page * self.per_page

    def prev(self, error_out=False):
        """Returns a Pagination object for the previous page."""
        assert self.query is not None, "A query object is required for this method to work."
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists."""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a Pagination object for the next page."""
        assert self.query is not None, "A query object is required for this method to work."
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page."""
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """
        Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as None.
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or (num > self.page - left_current - 1 and num < self.page + right_current) \
                    or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
