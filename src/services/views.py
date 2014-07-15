"""
Services endpoints
"""
from flask import Blueprint, render_template

bp = Blueprint('services', __name__)

@bp.route('/health')
def health():
    return "All is well :)"

# TODO: Add admin_required decorator
@bp.route('/preview_activate_email', methods=['GET'])
def activate_email():
    return render_template("email/activate.tmpl", activate_link="{{ activate_link }}")
