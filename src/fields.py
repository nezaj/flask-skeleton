"""
Generic form classes and helpers to use throughout the application
"""
from wtforms.validators import ValidationError

class Predicate(object):

    def __init__(self, f, message=None):
        self.f = f
        self.message = message

    def __call__(self, form, field):
        valid = self.f(field.data)
        if not valid:
            message = self.message or "Invalid value"
            raise ValidationError(message)
