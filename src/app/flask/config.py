from flask import request
from functools import wraps
import json
import os
from passlib.context import CryptContext
from werkzeug.exceptions import Unauthorized


# Env VARS
host= os.getenv('FLASK_HOST', '0.0.0.0')
port= os.getenv('FLASK_PORT', 5000)

mongo_host= os.getenv('MONGO_HOST', 'localhost')
mongo_port= os.getenv('MONGO_PORT', 27017)

# Api Keys file
file_path = "./api_keys.json"

# CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# SECURE ROUTES DECORATOR
def get_api_keys(file_path:str) -> list:
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise FileNotFoundError("File not found or invalid JSON.")
    else:
        keys: list = []
        for key, value in data.items():
            keys.append(value)
    finally:
        return keys


def control_api_key(api_key:str, file_path:str = file_path) -> bool:
    keys = get_api_keys(file_path)
    if not api_key or not any(pwd_context.verify(api_key, key) for key in keys):
        return False
    else:
        return True


# Require KEY - AUTH
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        keys = get_api_keys(file_path)
        if control_api_key(api_key, file_path) == False:
            raise Unauthorized()
        return f(*args, **kwargs)
    return decorated_function

