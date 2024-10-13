#api/routers/items.py


# Lib
from flask import Blueprint, jsonify, request
from uuid import uuid4


from services.mongo_connect import push_update_in_collection, fetch_collection
from services.security import require_api_key
from utils.limiter import limiter


"""
Router Declaration
"""
items_router = Blueprint('items', __name__)


"""
Routes Declaration
"""
@items_router.route('/all')
@limiter.limit("3000 per minute")
@require_api_key
def get_items() -> dict:
    collection = fetch_collection()
    items_documents = collection.find({"type": "item"})

    items = [{
        "_id": item.get('_id'),
        "name": item.get('name'),
        "description": item.get('description'),
        "unit": item.get('unit'),
        "rate": item.get('rate'),
    } for item in items_documents]
    
    if not items:
        return jsonify({"items": [], "no_items": True})
    return jsonify({"items": items})
    


@items_router.route('/new', methods=['POST'])
@limiter.limit("3000 per minute")
@require_api_key
def create_new_item() -> dict:
    new_item = request.json
    new_item['_id'] = str(uuid4())
    new_item['type'] = "item"

    if not new_item.get('name'):
        return jsonify({"error": "Item name is required"}), 400

    else:
        push_update_in_collection(data = new_item, document_to_update = "item", mode = "create")
        return jsonify({"message": "Item added successfully"})
    


@items_router.route('/update', methods=['PUT'])
@limiter.limit("3000 per minute")
@require_api_key
def update_existing_item() -> dict:
        

    posted_data = request.get_json()

    item_data = {
        '_id': posted_data.get('_id'),
        'type': 'item',
        'name': posted_data.get('name') if posted_data.get('name') else None,
        'description': posted_data.get('description') if posted_data.get('description') else None,
        'unit': posted_data.get('unit') if posted_data.get('unit') else None,
        'rate': posted_data.get('rate') if posted_data.get('rate') else None,
    }

    push_update_in_collection(data = item_data, document_to_update = "item", mode = "update")
    return jsonify({"message": "Item updated successfully"})



@items_router.route('/delete', methods=['DELETE'])
@limiter.limit("3000 per minute")
@require_api_key
def delete_existing_item() -> dict:

    posted_data = request.get_json() or {}
    item_data = {
        '_id': posted_data.get('_id'),
        'type': 'item'
    }
    push_update_in_collection(data = item_data, document_to_update = "item", mode = "delete")
    return jsonify({"message": "Item deleted successfully"})