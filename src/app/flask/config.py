from flask import session
from functools import wraps
import json
import os
from passlib.context import CryptContext
from pymongo import MongoClient
from werkzeug.exceptions import Unauthorized



# Env VARS
host= os.getenv('FLASK_HOST', '0.0.0.0')
port = int(os.getenv('FLASK_PORT', 5000))

mongo_host= os.getenv('MONGO_HOST', 'app-mongodb-1')
mongo_port = int(os.getenv('MONGO_PORT', 27017))

# Api Keys file
keys_file_path = "./api_keys.json"

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
            keys.append(value["key"])
    finally:
        return keys


def control_api_key(api_key:str, file_path:str = keys_file_path) -> bool:
    keys = get_api_keys(keys_file_path)
    if not api_key or not any(pwd_context.verify(api_key, key) for key in keys):
        return False
    else:
        return True


# Require KEY - AUTH
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = session.get('api_key')
        if not api_key:
            raise Unauthorized("Unauthorized")
        return f(*args, **kwargs)
    return decorated_function


# MongoDB connection
def get_mongodb_username(api_key:str) -> dict:
    user = None
    company = None

    # Open user json
    with open(keys_file_path, "r") as f:
        data = json.load(f)
    
    for key, value in data.items():
        if pwd_context.verify(api_key, value["key"]):
            user = value["username"]
            company = value["company"]
            break
    
    if user is None or company is None:
        raise Unauthorized("User or company not found.")

    user_data = {
        "user" : user,
        "company" : company
    }

    return user_data



def get_mongo_client(api_key: str) -> MongoClient:

    user_data = get_mongodb_username(api_key)
    username = user_data["user"]
    company = user_data["company"]

    return MongoClient(
                        host = mongo_host,
                        port = mongo_port,
                        username = username,
                        password = api_key,
                        authSource = company
                        ), company


def load_collection(api_key:str, collection:str) -> MongoClient:
    client, company = get_mongo_client(api_key)
    db = client[company]
    company_collection = db[collection]
    return company_collection
