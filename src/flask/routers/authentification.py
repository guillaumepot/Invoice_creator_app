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
    return



@authentification_router.route('/login', methods=['POST'])
@limiter.limit("30 per hour")
def set_api_key():
    api_key = request.form['api_key']

    # Test the API key
    if not control_api_key(api_key):
        return {"message": "Invalid API key"}, 401

    else:
        session['api_key'] = api_key
        return {"message": "Logged in successfully"}, 200