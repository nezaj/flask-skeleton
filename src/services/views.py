"""
Services endpoints
"""
from flask import abort, Blueprint, render_template

blueprint = Blueprint('services', __name__)

@blueprint.route('/health')
def health():
    return "All is well :)"

# TODO: Add admin_required decorator
@blueprint.route('/preview_activate_email')
def activate_email():
    return render_template("email/activate.tmpl", activate_link="{{ activate_link }}")

@blueprint.route('/401')
def unauthorized():
    abort(401)

@blueprint.route('/403')
def forbidden():
    abort(403)

@blueprint.route('/404')
def not_found():
    abort(404)

@blueprint.route('/500')
def internal_error():
    abort(500)
