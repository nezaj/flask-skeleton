#!/usr/bin/env python

from setuptools import setup, find_packages

dependencies = [
    # Get latest packages for lint tools
    "pep8>=1.5.6",
    "pylint>=1.2.1",
    # Flask and extensions
    "flask==0.10.1",
    "flask-assets==0.9",
    "flask-bcrypt==0.6.0",
    "flask-login==0.2.11",
    "flask-mail==0.9.0",
    "flask-migrate==1.2.0",
    "flask-script==2.0.5",
    "flask-wtf==0.9.5",
    # Additional packages
    "alembic==0.6.5",
    "pytest==2.5.2",
    "webtest==2.0.15",
    "cssmin==0.2.0",
    "gunicorn==0.17.2",
    "psycopg2==2.5.2",
    "pyscss==1.2.0",
    "sqlalchemy==0.9.3",
]

setup(
    name="flask-skeleton",
    version="0.1",
    url="https://github.com/nezaj/flask-skeleton",
    packages=find_packages(),
    zip_safe=False,
    install_requires=dependencies
)
