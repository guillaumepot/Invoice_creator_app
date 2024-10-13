#api/routers/quotes.py


# Lib
from flask import Blueprint, jsonify, request
import random
from uuid import uuid4


from services.mongo_connect import push_update_in_collection, fetch_collection
from services.security import require_api_key
from utils.limiter import limiter

"""
Router Declaration
"""
quotes_router = Blueprint('quotes', __name__)


"""
Routes Declaration
"""
@quotes_router.route('/all')
@limiter.limit("3000 per minute")
@require_api_key
def get_quotes() -> dict:
    collection = fetch_collection()
    quotes_documents = collection.find({"type": "quote"})

    quotes = [{
        "_id": quote.get('_id'),
        "name": quote.get('name'),
        "number": quote.get('number'),
        "description": quote.get('description'),
        "client": quote.get('client'),
        "created_date": quote.get('created_date'),
        "valid_until": quote.get('valid_until'),
        "total_amount_no_vat": quote.get('total_amount_no_vat'),
        "vat": quote.get('vat'),
        "discount": quote.get('discount'),
        "total_amount_with_discount": quote.get('total_amount_with_discount'),
        "total_amount_with_vat": quote.get('total_amount_with_vat'),
        "discount_description": quote.get('discount_description'),
        "currency": quote.get('currency'),
        "terms": quote.get('terms'),
        "items": quote.get('items'),
    } for quote in quotes_documents]
    
    if not quotes:
        return jsonify({"quotes": [], "no_quotes": True})
    return jsonify({"quotes": quotes})
    


@quotes_router.route('/new', methods=['POST'])
@limiter.limit("3000 per minute")
@require_api_key
def create_new_item() -> dict:
    new_quote = request.json
    new_quote['_id'] = str(uuid4())
    new_quote['type'] = "quote"
    new_quote['number'] = new_quote['created_date'].replace("-","") + str(random.randint(000, 999))

    if not new_quote.get('name'):
        return jsonify({"error": "Quote name is required"}), 400

    else:
        push_update_in_collection(data = new_quote, document_to_update = "quote", mode = "create")
        return jsonify({"message": "Quote added successfully"})
    


@quotes_router.route('/delete', methods=['DELETE'])
@limiter.limit("3000 per minute")
@require_api_key
def delete_existing_quote() -> dict:

    posted_data = request.get_json() or {}
    quote_data = {
        '_id': posted_data.get('_id'),
        'type': 'quote'
    }
    push_update_in_collection(data = quote_data, document_to_update = "quote", mode = "delete")
    return jsonify({"message": "Quote deleted successfully"})