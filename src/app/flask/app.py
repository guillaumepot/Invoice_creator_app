from flask import Flask, render_template, send_file, request, jsonify
from flask import session, redirect, url_for, flash, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import io
import os
import time
from uuid import uuid4
from weasyprint import HTML

from config import host, port, require_api_key, control_api_key, get_mongo_client, load_collection

# Flask
app = Flask(__name__)
app.secret_key = 'faf1Fz1daf8Z8z191Z' # DEV - Set to a random value AS ENV VAR in the future

# Limiter
limiter = Limiter(
    key_func=get_remote_address,        # Get the remote address
    app=app,                            # Flask app
    default_limits=["1000 per hour"]     # Default limit  DEV - Set to 20/minute in the future
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
        return {"message": "Invalid API key"}, 401

    else:
        session['api_key'] = api_key
        return {"message": "Logged in successfully"}, 200


# Logout
@app.route('/logout', methods=['POST'])
@require_api_key
def logout():
    session.pop('api_key', None)
    return



## HOME
@app.route('/')
def home():
    api_key = session.get('api_key')
    return render_template('home.html', api_key=api_key)



## MY_COMPANY
@app.route('/company/informations', methods = ['GET', 'PUT'])
@require_api_key
def get_company_info() -> dict:

    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Company')
    company_document = company_collection.find_one()

    if request.method == 'GET':
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


    if request.method == 'PUT':
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
@app.route('/clients', methods=['GET', 'POST', 'PUT', 'DELETE'])
@require_api_key
def client_request():
    api_key = session.get('api_key')
    client_collection = load_collection(api_key, 'Clients')
    client_documents = client_collection.find()

    if request.method == 'GET':
        clients = [{
            "_id": client.get('_id'),
            "name": client.get('name'),
            "address": client.get('address'),
            "zipcode": client.get('zipcode'),
            "city": client.get('city'),
            "country": client.get('country'),
            "phone": client.get('phone'),
            "email": client.get('email'),
            "siret": client.get('siret'),
            "vat_number": client.get('vat_number')
        } for client in client_documents]
        
        if not clients:
            return jsonify({"clients": [], "no_clients": True})
        return jsonify({"clients": clients})
    

    if request.method == 'POST':
        # Add new client
        new_client = request.json
        new_client['_id'] = str(uuid4())

        if not new_client.get('name'):
            return jsonify({"error": "Client name is required"}), 400

        client_collection.insert_one(new_client)
        return jsonify({"message": "Client added successfully"})


    if request.method == 'PUT':
        # Update clients
        posted_data = request.get_json() or {}
        client_id = posted_data.get('_id')
        existing_client = client_collection.find_one({'_id': client_id})
        if not existing_client:
            return jsonify({"error": "Client not found"}), 404
        
        client_data = {
            'name': posted_data.get('name') or existing_client.get('name'),
            'address': posted_data.get('address') or existing_client.get('address'),
            'zipcode': posted_data.get('zipcode') or existing_client.get('zipcode'),
            'city': posted_data.get('city') or existing_client.get('city'),
            'country': posted_data.get('country') or existing_client.get('country'),
            'phone': posted_data.get('phone') or existing_client.get('phone'),
            'email': posted_data.get('email') or existing_client.get('email'),
            'siret': posted_data.get('siret') or existing_client.get('siret'),
            'vat_number': posted_data.get('vat_number') or existing_client.get('vat_number'),
        }
        client_collection.replace_one({'_id': client_id}, client_data, upsert=True)
        
        return jsonify({"message": "Client updated successfully"})
    

    if request.method == 'DELETE':
        # Delete provided client datas
        posted_data = request.get_json() or {}
        client_id = posted_data.get('_id')

        client_collection.delete_one({'_id': client_id})
        return jsonify({"message": "Client deleted successfully"})






























@app.route('/client/update/<client_name>', methods=['PUT'])
@require_api_key
def update_client(client_name: str):
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Clients')
    updated_client = request.json

    if not updated_client.get('name'):
        return jsonify({"error": "Client name is required"}), 400

    company_collection.replace_one({'name': client_name}, updated_client)
    return jsonify({"message": "Client updated successfully"})


@app.route('/client/delete/<client_name>', methods=['DELETE'])
@require_api_key
def delete_client(client_name: str):
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Clients')

    company_collection.delete_one({'name': client_name})
    return jsonify({"message": "Client deleted successfully"})




## ITEMS
@app.route('/items/list', methods=['GET'])
@require_api_key
def get_items() -> dict:
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Items')
    items_documents = company_collection.find()

    items = [{
        'description': item.get('description'),
        'rate': item.get('rate'),
        'unit': item.get('unit'),
        'quantity': item.get('quantity')
    } for item in items_documents]
    
    if not items:
        return jsonify({"items": [], "no_items": True})
    return jsonify({"items": items})


@app.route('/items/info/<item_description>', methods=['GET'])
@require_api_key
def get_item_info(item_description: str) -> dict:
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Items')
    item_document = company_collection.find_one({'description': item_description})

    item_data = {
        'description': item_document.get('description') if item_document else None,
        'rate': item_document.get('rate') if item_document else None,
        'unit': item_document.get('unit') if item_document else None,
        'quantity': item_document.get('quantity') if item_document else None,
    }
    return jsonify(item_data)


@app.route('/items/add', methods=['POST'])
@require_api_key
def add_item():
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Items')
    new_item = request.json

    if not new_item.get('description'):
        return jsonify({"error": "Item description is required"}), 400
    if not new_item.get('rate'):
        return jsonify({"error": "Item rate is required"}), 400
    if not new_item.get('unit'):
        return jsonify({"error": "Item unit is required"}), 400

    company_collection.insert_one(new_item)
    return jsonify({"message": "Item added successfully"})


@app.route('/items/update/<item_description>', methods=['PUT'])
@require_api_key
def update_item(item_description: str):
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Items')
    updated_item = request.json

    if not updated_item.get('description'):
        return jsonify({"error": "Item description is required"}), 400

    company_collection.replace_one({'description': item_description}, updated_item)
    return jsonify({"message": "Item updated successfully"})


@app.route('/items/delete/<item_description>', methods=['DELETE'])
@require_api_key
def delete_item(item_description: str):
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Items')

    company_collection.delete_one({'item_description': item_description})
    return jsonify({"message": "Item deleted successfully"})




## INVOICES
@app.route('/invoice/create', methods=['POST'])
@require_api_key
def create_invoice():
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Invoices')
    invoice = request.json
    company_collection.insert_one(invoice)
    return jsonify({"message": "Invoice created successfully"})


@app.route('/invoice/delete', methods=['GET'])
@require_api_key
def delete_invoice():
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Invoices')
    company_collection.delete_many({})
    return jsonify({"message": "All invoices deleted successfully"})


@app.route('/invoice/list', methods=['GET'])
@require_api_key
def list_invoices():
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Invoices')
    invoices = company_collection.find()
    invoices_list = [{
        "invoice_number": invoice.get('invoice_number'),
        "invoice_nb": invoice.get('invoice_nb'),
        "created_date": invoice.get('created_date'),
        "customer": invoice.get('customer'),
        "total": invoice.get('total')
    } for invoice in invoices]
    if not invoices_list:
        return jsonify({"invoices": [], "no_invoices": True})
    return jsonify({"invoices": invoices_list})


@app.route('/invoice/info/<invoice_number>', methods=['GET'])
@require_api_key
def get_invoice_info(invoice_number: str):
    api_key = session.get('api_key')
    company_collection = load_collection(api_key, 'Invoices')
    invoice_document = company_collection.find_one({'invoice_number': invoice_number})

    invoice_data = {
        'language': invoice_document.get('language') if invoice_document else 'en',
        'invoice_nb': invoice_document.get('invoice_nb') if invoice_document else None,
        'created_date': invoice_document.get('created_date') if invoice_document else None,
        'due_date': invoice_document.get('due_date') if invoice_document else None,
        'currency': invoice_document.get('currency') if invoice_document else '€',
        'company': invoice_document.get('company') if invoice_document else None,
        'customer': invoice_document.get('customer') if invoice_document else None,
        'items': invoice_document.get('items') if invoice_document else None,
        'invoice_number': invoice_document.get('invoice_number') if invoice_document else None,
        'items': invoice_document.get('items') if invoice_document else None,
        'total': invoice_document.get('total') if invoice_document else None,
    }
    return jsonify(invoice_data)









# Start app
if __name__ == '__main__':
    host = os.environ.get("HOST", host)
    port = int(os.environ.get("PORT", port))
    app.run(host=host, port=port, debug=True)