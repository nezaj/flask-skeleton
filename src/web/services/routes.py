"""
Services endpoints
"""
from . import services

@services.route('/health')
def health():
    return "All is well :)"
