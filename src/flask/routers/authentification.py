#api/routers/authentification.py


# Lib
from flask import Blueprint, jsonify, session, request



from services.security import require_api_key, control_api_key
from utils.config import CURRENT_VERSION
from utils.limiter import limiter



"""
Router Declaration
"""
authentification_router = Blueprint('autentification', __name__)


"""
Routes Declaration
"""

@authentification_router.route('/logout', methods=['POST'])
@require_api_key
def logout():
    session.pop('api_key', None)
    session.pop('user_data', None)
    return jsonify({"message": "Logged out successfully"}), 200



@authentification_router.route('/login', methods=['POST'])
@limiter.limit("30 per hour")
def login_with_api_key():
    api_key = request.form['api_key']

    # Test the API key
    user_data = control_api_key(api_key)
    if not user_data:
        return {"message": "Invalid API key"}, 401

    else:
        session['api_key'] = api_key
        session['user_data'] = user_data
        return {"message": "Logged in successfully"}, 200