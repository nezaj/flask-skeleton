import base64
import os

def generate_activate_token():
    "Generates a random 24 byte string, used for generating activation tokens"
    return base64.b64encode(os.urandom(24))
