"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template

home = Blueprint('main', __name__)

@home.route('/', methods=['GET'])
def index():
    return render_template('/main/index.tmpl')
