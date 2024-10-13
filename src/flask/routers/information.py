#api/routers/information.py


# Lib
from flask import Blueprint, jsonify
from pymongo import MongoClient


from services.mongo_connect import check_mongo_availability
from services.security import require_api_key
from utils.config import CURRENT_VERSION, MONGO_HOST, MONGO_PORT
from utils.limiter import limiter



"""
Router Declaration
"""
information_router = Blueprint('information', __name__)


"""
Routes Declaration
"""

@information_router.route('/status', methods=['GET'])
@limiter.limit("5 per minute")
def get_status():
    """
    Get the status of the API
    """
    return jsonify({"status": f"API is running, version: {CURRENT_VERSION}"})



@information_router.route('/checkmongo', methods=['GET'])
@limiter.limit("5 per minute")
@require_api_key
def get_check_mongo():
    """
    Check if the API can connect to the MongoDB
    """
    return check_mongo_availability()