#flask/services/security.py


# Lib
from flask import session
from functools import wraps
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
    keys = collection.find({}, {"password": 1, "_id": 0})

    user_data: dict = {}


    for key in keys:
        if pwd_context.verify(api_key, key["password"]):
            user_doc = collection.find_one({"password": key["password"]}, {"username": 1, "company": 1, "_id": 0})
            if user_doc:
                user_data["username"] = user_doc["username"]
                user_data["company"] = user_doc["company"]
                return user_data
            
            return False