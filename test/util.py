"""
Utilities for running tests
"""
from flask import url_for

def fill_register_form(register_form, user, password=None):
    register_form['email'] = user.email
    register_form['username'] = user.username
    register_form['password'] = password or user.username
    return register_form

def login_el(res):
    return res.html.find('a', href=url_for('auth.login'))

def logout_el(res):
    return res.html.find('a', href=url_for('auth.logout'))
