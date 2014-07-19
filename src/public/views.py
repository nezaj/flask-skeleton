"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template

blueprint = Blueprint('public', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')
