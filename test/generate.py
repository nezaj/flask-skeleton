"""
Helper functions used for generating data
"""
from src.data.models import User

def generate_model(cls, cls_attrs):
    return cls(**cls_attrs)

def generate_user(**kwargs):
    options = dict(email="mock@example.com",
                   username="mock",
                   password="mock")
    options.update(**kwargs)
    return generate_model(User, options)
