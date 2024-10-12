#flask/services/security.py


# Lib
from flask import session
from functools import wraps
import json
import os
from pymongo import MongoClient
from werkzeug.exceptions import Unauthorized


from utils.config import pwd_context, MONGO_API_USERNAME, MONGO_API_PASSWORD
from services.mongo_connect import check_mongo_availability, connect_to_mongo




# Require KEY DECORATOR - AUTH
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = session.get('api_key')
        if not api_key:
            raise Unauthorized("Unauthorized")
        return f(*args, **kwargs)
    return decorated_function


def control_api_key(api_key:str) -> bool:
    check_mongo_availability()
    client = connect_to_mongo(username = MONGO_API_USERNAME, password = MONGO_API_PASSWORD, authSource = "admin")

    db = client["users"]
    collection = db["user_data"]
    keys = collection.find()


    if not api_key or not any(pwd_context.verify(api_key, key) for key in keys):
        return False
    else:
        return True








# def get_api_keys(file_path:str) -> list:
#     try:
#         with open(file_path, "r") as f:
#             data = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         raise FileNotFoundError("File not found or invalid JSON.")
#     else:
#         keys: list = []
#         for key, value in data.items():
#             keys.append(value["key"])
#     finally:
#         return keys



