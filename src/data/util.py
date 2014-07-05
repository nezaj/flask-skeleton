import base64
import os

def generate_random_token():
    "Generates a random 24 byte string"
    return base64.b64encode(os.urandom(24))
