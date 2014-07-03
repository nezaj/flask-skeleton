import base64
import os

def generate_random_token():
    "Generates a random 24 byte string"
    return base64.b64encode(os.urandom(24))

def get_password_reset_token(user):
    # Create a new token if no token exists
    # If a token exists but is expired, delete it and generate a new one
    # If a token exists and is not expired, but is used delete it and generate a new one
    # If a token exists, is not expired, and is not used, return it
    pass
