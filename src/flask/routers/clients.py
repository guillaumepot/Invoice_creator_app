#api/routers/clients.py


# Lib
from flask import Blueprint, jsonify, request
from uuid import uuid4


from services.mongo_connect import push_update_in_collection, fetch_collection
from services.security import require_api_key
from utils.limiter import limiter


"""
Router Declaration
"""
clients_router = Blueprint('clients', __name__)


"""
Routes Declaration
"""
@clients_router.route('/all')
@limiter.limit("3000 per minute")
@require_api_key
def get_clients() -> dict:

    collection = fetch_collection()
    clients_documents = collection.find({"type": "client"})

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
    } for client in clients_documents]
    
    if not clients:
        return jsonify({"clients": [], "no_clients": True})
    return jsonify({"clients": clients})
    


@clients_router.route('/new', methods=['POST'])
@limiter.limit("3000 per minute")
@require_api_key
def create_new_client() -> dict:
    new_client = request.json
    new_client['_id'] = str(uuid4())
    new_client['type'] = "client"

    if not new_client.get('name'):
        return jsonify({"error": "Client name is required"}), 400

    else:
        push_update_in_collection(data = new_client, document_to_update = "client", mode = "create")
        return jsonify({"message": "Client added successfully"})
    


@clients_router.route('/update', methods=['PUT'])
@limiter.limit("3000 per minute")
@require_api_key
def update_existing_client() -> dict:
    posted_data = request.get_json()

    client_data = {
        '_id': posted_data.get('_id'),
        'type': 'client',
        'name': posted_data.get('name') if posted_data.get('name') else None,
        'address': posted_data.get('address') if posted_data.get('address') else None,
        'zipcode': posted_data.get('zipcode') if posted_data.get('zipcode') else None,
        'city': posted_data.get('city') if posted_data.get('city') else None,
        'country': posted_data.get('country') if posted_data.get('country') else None,
        'phone': posted_data.get('phone') if posted_data.get('phone') else None,
        'email': posted_data.get('email') if posted_data.get('email') else None,
        'siret': posted_data.get('siret') if posted_data.get('siret') else None,
        'vat_number': posted_data.get('vat_number') if posted_data.get('vat_number') else None,
    }

    push_update_in_collection(data = client_data, document_to_update = "client", mode = "update")

    return jsonify({"message": "Client updated successfully"})



@clients_router.route('/delete', methods=['DELETE'])
@limiter.limit("3000 per minute")
@require_api_key
def delete_existing_client() -> dict:
    posted_data = request.get_json() or {}
    client_data = {
        '_id': posted_data.get('_id'),
        'type': 'client'
    }

    push_update_in_collection(data = client_data, document_to_update = "client", mode = "delete")
    return jsonify({"message": "Client deleted successfully"})