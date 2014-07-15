"""
Logic for dashboard related routes
"""
from flask import Blueprint, render_template

bp = Blueprint('public', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('public/index.tmpl')
