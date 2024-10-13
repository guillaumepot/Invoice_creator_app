#flask/services/mongo_connect.py


# Lib
from flask import session, jsonify
from pymongo import MongoClient, errors

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
    
    

def fetch_authenticated_client(api_key:str) -> MongoClient:
    """
    Return an authenticated connection to the MongoDB (user specific)
    """
    user_data = session.get('user_data')
    username = user_data.get('username')
    return connect_to_mongo(username = username, password = api_key, authSource = "admin")


def fetch_collection(): 
    """
    Fetch User collection
    """
    user_data = session.get('user_data')
    company = user_data.get('company')

    client = fetch_authenticated_client(session.get('api_key'))
    db = client["users"]

    collection = db[company]
    return collection



def push_update_in_collection(data:dict, document_to_update:str, mode:str = "") -> None:
    """
    Push an update in the collection (document_to_update is the type (key) of document to update)
    """
    collection = fetch_collection()

    if document_to_update == "company":
        collection.replace_one({"type":document_to_update}, data, upsert=True)

    else:
        if mode == "create":
            collection.insert_one({"type":document_to_update, **data})

        elif mode == "update":
            to_update = collection.find_one({'_id': data.get('_id'), 'type': document_to_update})
            if to_update:
                collection.replace_one({'_id': data.get('_id'), 'type': document_to_update}, data, upsert=True)
            else:
                return jsonify({"error": "Document not found"}), 404
            
        elif mode == "delete":
            to_delete = collection.find_one({'_id': data.get('_id'), 'type': document_to_update})
            if to_delete:
                collection.delete_one({'_id': data.get('_id')})
            else:
                return jsonify({"error": "Document not found"}), 404