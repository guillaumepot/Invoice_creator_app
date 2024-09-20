from flask import Flask, render_template, send_file, request, jsonify
from flask import session, redirect, url_for, flash, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import io
import os
import time
from weasyprint import HTML

from config import host, port, require_api_key, control_api_key, get_mongo_client, load_collection

# Flask
app = Flask(__name__)
app.secret_key = 'faf1Fz1daf8Z8z191Z' # DEV - Set to a random value AS ENV VAR in the future

# Limiter
limiter = Limiter(
    key_func=get_remote_address,        # Get the remote address
    app=app,                            # Flask app
    default_limits=["500 per hour"]     # Default limit  DEV - Set to 20/minute in the future
)
# Rate limit exceeded handler
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Rate limit exceeded"), 429
# Middleware to add processing time header
@app.before_request
def before_request():
    g.start_time = time.time()
@app.after_request
def after_request(response):
    process_time = time.time() - g.start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


### ROUTES

## AUTH
# Login
@app.route('/login', methods=['POST'])
@limiter.limit("300 per hour") # DEV - Set to 3/hour in the future
def set_api_key():
    api_key = request.form['api_key']

    # Test the API key
    if not control_api_key(api_key):
        flash('Bad key', 'error')
    else:
        session['api_key'] = api_key
    return redirect(url_for('home'))

# Logout
@app.route('/logout', methods=['POST'])
@require_api_key
def logout():
    session.pop('api_key', None)
    return redirect(url_for('home'))

## HOME

# Home
@app.route('/')
def home():
    api_key = session.get('api_key')
    return render_template('home.html', api_key=api_key)


## MY_COMPANY
@app.route('/company/info', methods = ['GET'])
@require_api_key
def get_company_info() -> dict:

    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Company')
    company_document = company_collection.find_one()

    company_data = {
        'name': company_document.get('name') if company_document else None,
        'address': company_document.get('address') if company_document else None,
        'zipcode': company_document.get('zipcode') if company_document else None,
        'city': company_document.get('city') if company_document else None,
        'country': company_document.get('country') if company_document else None,
        'phone': company_document.get('phone') if company_document else None,
        'email': company_document.get('email') if company_document else None,
        'siret': company_document.get('siret') if company_document else None,
        'vat_number': company_document.get('vat_number') if company_document else None,
    }
    return jsonify(company_data)


@app.route('/company/update', methods = ['PUT'])
@require_api_key
def update_company() -> None:
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Company')
    company_document = company_collection.find_one()

    posted_data = request.get_json() or {}

    company_data = {
        'name': posted_data.get('name') or company_document.get('name'),
        'address': posted_data.get('address') or company_document.get('address'),
        'zipcode': posted_data.get('zipcode') or company_document.get('zipcode'),
        'city': posted_data.get('city') or company_document.get('city'),
        'country': posted_data.get('country') or company_document.get('country'),
        'phone': posted_data.get('phone') or company_document.get('phone'),
        'email': posted_data.get('email') or company_document.get('email'),
        'siret': posted_data.get('siret') or company_document.get('siret'),
        'vat_number': posted_data.get('vat_number') or company_document.get('vat_number'),
    }

    company_collection.replace_one({}, company_data, upsert=True)

    return jsonify(company_data)

## CLIENTS
@app.route('/client/list', methods=['GET'])
@require_api_key
def get_client_list() -> dict:
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Clients')
    client_documents = company_collection.find()

    clients = [{"name": client.get('name')} for client in client_documents]
    if not clients:
        return jsonify({"clients": [], "no_clients": True})
    return jsonify({"clients": clients})


@app.route('/client/add', methods=['POST'])
@require_api_key
def add_client():
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Clients')
    new_client = request.json

    if not new_client.get('name'):
        return jsonify({"error": "Client name is required"}), 400

    company_collection.insert_one(new_client)
    return jsonify({"message": "Client added successfully"})


@app.route('/client/info/<client_name>', methods=['GET'])
@require_api_key
def get_client_info(client_name: str) -> dict:
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Clients')
    client_document = company_collection.find_one({'name': client_name})

    client_data = {
        'name': client_document.get('name') if client_document else None,
        'address': client_document.get('address') if client_document else None,
        'zipcode': client_document.get('zipcode') if client_document else None,
        'city': client_document.get('city') if client_document else None,
        'country': client_document.get('country') if client_document else None,
        'phone': client_document.get('phone') if client_document else None,
        'email': client_document.get('email') if client_document else None,
        'siret': client_document.get('siret') if client_document else None,
        'vat_number': client_document.get('vat_number') if client_document else None,
    }
    return jsonify(client_data)



# Start app
if __name__ == '__main__':
    host = os.environ.get("HOST", host)
    port = int(os.environ.get("PORT", port))
    app.run(host=host, port=port, debug=True)