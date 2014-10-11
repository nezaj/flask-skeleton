#!/usr/bin/env python

from setuptools import setup, find_packages

# hack to fix a Python 2.7.3 issue with multiprocessing module --
# see http://bugs.python.org/issue15881
try:
    import multiprocessing
except ImportError:
    pass

dependencies = [
    # Flask and extensions
    "flask==0.10.1",
    "flask-assets==0.9",
    "flask-bcrypt==0.6.0",
    "flask-login==0.2.11",
    "flask-mail==0.9.0",
    "flask-migrate==1.2.0",
    "flask-script==2.0.5",
    "flask-webtest==0.0.7",
    "flask-wtf==0.9.5",
    # Asset minification
    "cssmin==0.2.0",
    "pyscss==1.2.0",
    # Database
    "alembic==0.6.5",
    "psycopg2==2.5.2",
    "sqlalchemy==0.9.3",
    # Testing
    "pytest==2.5.2",
    "webtest==2.0.15",
    # Lint, get latest stable to stay up-to-date w/ standards
    "pep8>=1.5.6",
    "pylint>=1.2.1",
    # Prod webserver
    "gunicorn==0.17.2",
]

setup(
    name="flask-skeleton",
    version="0.1",
    url="https://github.com/nezaj/flask-skeleton",
    packages=find_packages(),
    zip_safe=False,
    install_requires=dependencies
)
