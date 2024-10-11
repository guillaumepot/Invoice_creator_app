from flask import Flask, render_template, send_file, request, jsonify
from flask import session, redirect, url_for, flash, g
import io
import time
from uuid import uuid4
from weasyprint import HTML

from config import FLASK_HOST, FLASK_PORT, DEBUG_MODE, FLASK_SECRET_APP_KEY, require_api_key, control_api_key, get_mongo_client, load_collection



# Flask
app = Flask(__name__)
app.secret_key = FLASK_SECRET_APP_KEY


"""
Limiter
"""
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
        # Update client
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




## ITEMS
@app.route('/items', methods=['GET', 'POST', 'PUT', 'DELETE'])
@require_api_key
def get_items() -> dict:
    api_key = session.get('api_key')
    items_collection = load_collection(api_key, 'Items')
    items_documents = items_collection.find()

    if request.method == 'GET':
        items = [{
            '_id': item.get('_id'),
            'name': item.get('name'),
            'description': item.get('description'),
            'unit': item.get('unit'),
            'rate': item.get('rate')
        } for item in items_documents]
    
        if not items:
            return jsonify({"items": [], "no_items": True})
        return jsonify({"items": items})


    if request.method == 'POST':
        # Add new item
        new_item = request.json
        new_item['_id'] = str(uuid4())

        if not new_item.get('name'):
            return jsonify({"error": "Item name is required"}), 400

        items_collection.insert_one(new_item)
        return jsonify({"message": "Item added successfully"})



    if request.method == 'PUT':
        # Update item
        posted_data = request.get_json() or {}
        item_id = posted_data.get('_id')
        existing_item = items_collection.find_one({'_id': item_id})
        if not existing_item:
            return jsonify({"error": "Item not found"}), 404
        
        item_data = {
            'name': posted_data.get('name') or existing_item.get('name'),
            'description': posted_data.get('description') or existing_item.get('description'),
            'unit': posted_data.get('unit') or existing_item.get('unit'),
            'rate': posted_data.get('rate') or existing_item.get('rate')
        }
        items_collection.replace_one({'_id': item_id}, item_data, upsert=True)
        
        return jsonify({"message": "Item updated successfully"})
    

    if request.method == 'DELETE':
        # Delete provided item datas
        posted_data = request.get_json() or {}
        item_id = posted_data.get('_id')

        items_collection.delete_one({'_id': item_id})
        return jsonify({"message": "Item deleted successfully"})




## QUOTES
@app.route('/quotes', methods=['GET', 'POST', 'PUT', 'DELETE'])
@require_api_key
def create_quote():
    api_key = session.get('api_key')
    quote_collection = load_collection(api_key, 'Quotes')
    quote_documents = quote_collection.find()


    if request.method == 'GET':
        quotes = [{
            'name': quote.get('name'),
            'created_date': quote.get('created_date'),
            'valid_until': quote.get('valid_until'),
            'client': quote.get('client'),
            "total_amount": quote.get('total_amount'),
            "vat": quote.get('vat'),
            "total_amount_vat": quote.get('total_amount_vat'),
            "discount": quote.get('discount'),
            "discount_description": quote.get('discount_description'),
            "currency": quote.get('currency'),
            "notes": quote.get('notes'),
            "terms": quote.get('terms'),
            "items": quote.get('items')
        } for quote in quote_documents]


        if not quotes:
            return jsonify({"quotes": [], "no_quotes": True})
        return jsonify({"quotes": quotes})


    if request.method == 'POST':
        # Add new item
        new_item = request.json
        new_item['_id'] = str(uuid4())

        if not new_item.get('name'):
            return jsonify({"error": "Item name is required"}), 400

        quote_collection.insert_one(new_item)
        return jsonify({"message": "Quote added successfully"})



    # if request.method == 'PUT':
    #     # Update item
    #     posted_data = request.get_json() or {}
    #     item_id = posted_data.get('_id')
    #     existing_item = items_collection.find_one({'_id': item_id})
    #     if not existing_item:
    #         return jsonify({"error": "Item not found"}), 404
        
    #     item_data = {
    #         'name': posted_data.get('name') or existing_item.get('name'),
    #         'description': posted_data.get('description') or existing_item.get('description'),
    #         'unit': posted_data.get('unit') or existing_item.get('unit'),
    #         'rate': posted_data.get('rate') or existing_item.get('rate')
    #     }
    #     items_collection.replace_one({'_id': item_id}, item_data, upsert=True)
        
    #     return jsonify({"message": "Item updated successfully"})
    

    # if request.method == 'DELETE':
    #     # Delete provided item datas
    #     posted_data = request.get_json() or {}
    #     item_id = posted_data.get('_id')

    #     items_collection.delete_one({'_id': item_id})
    #     return jsonify({"message": "Item deleted successfully"})








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
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG_MODE)