"""
Services endpoints
"""
from flask import Blueprint, render_template

services = Blueprint('services', __name__)

@services.route('/health')
def health():
    return "All is well :)"

# TODO: Add admin_required decorator
@services.route('/preview_activate_email', methods=['GET'])
def activate_email():
    return render_template("email/activate.tmpl", activate_link="{{ activate_link }}")
