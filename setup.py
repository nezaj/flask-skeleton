#!/usr/bin/env python

from setuptools import setup, find_packages

dependencies = [
    "pep8",
    "pylint",
    "nose>=1.3.0",
    "cssmin>=0.2.0",
    "pyscss>=1.2.0",
    "gunicorn>=0.17.2",
    "flask>=0.10.1",
    "sqlalchemy>=0.9.3",
    "psycopg2>=2.5.2",
    "alembic>=0.6.3",
    "flask-assets>=0.9",
    "flask-script>=2.0.5",
]

setup(
    name="flask-skeleton",
    version="0.1",
    url="https://github.com/nezaj/flask-skeleton",
    packages=find_packages(),
    zip_safe=False,
    install_requires=dependencies
)
