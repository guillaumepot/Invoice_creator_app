#flask/services/mongo_connect.py


# Lib
from flask import session, jsonify
from functools import wraps
import json
import os
from pymongo import MongoClient, errors

from werkzeug.exceptions import Unauthorized


from utils.config import MONGO_HOST, MONGO_PORT, MONGO_API_USERNAME, MONGO_API_PASSWORD



def connect_to_mongo(username:str, password:str, authSource:str) -> MongoClient:
    """
    Return an authenticated connection to the MongoDB
    """
    try:
        return MongoClient(
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=username,
            password=password,
            authSource=authSource,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=3000,
            socketTimeoutMS=10000
        )
    
    except (errors.ConnectionError, errors.ServerSelectionTimeoutError) as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    


def check_mongo_availability() -> dict:
    """
    Ping MongoDB, check if available
    """
    try:
        client = connect_to_mongo(MONGO_API_USERNAME, MONGO_API_PASSWORD, "admin")
        client.admin.command("ping")
        return jsonify({"status": "MongoDB is available."})
        

    except errors.ServerSelectionTimeoutError as e:
        return jsonify({"status": "MongoDB is not available.", "error": str(e)})
    except Exception as e:
        return jsonify({"status": "MongoDB is not available.", "error": str(e)})














    # else:
    #     user_data = get_mongodb_username(api_key)
    #     username = user_data["user"]
    #     company = user_data["company"]

    #     return MongoClient(
    #                         host = MONGO_HOST,
    #                         port = MONGO_PORT,
    #                         username = username,
    #                         password = api_key,
    #                         authSource = company
    #                         ), company











# MongoDB connection
def get_mongodb_username(api_key:str) -> dict:
    user = None
    company = None
    pass

    # # Open user json
    # with open(keys_file_path, "r") as f:
    #     data = json.load(f)
    
    # for key, value in data.items():
    #     if pwd_context.verify(api_key, value["key"]):
    #         user = value["username"]
    #         company = value["company"]
    #         break
    
    # if user is None or company is None:
    #     raise Unauthorized("User or company not found.")

    # user_data = {
    #     "user" : user,
    #     "company" : company
    # }

    # return user_data





