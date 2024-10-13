#api/routers/invoices.py


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
invoices_router = Blueprint('invoices', __name__)


"""
Routes Declaration
"""
@invoices_router.route('/all')
@limiter.limit("3000 per minute")
@require_api_key
def get_invoices() -> dict:
    collection = fetch_collection()
    invoices_documents = collection.find({"type": "invoice"})

    invoices = [{
        "_id": invoice.get('_id'),
        "name": invoice.get('name'),
        "number": invoice.get('number'),
        "state": invoice.get('state'),
        "description": invoice.get('description'),
        "client": invoice.get('client'),
        "created_date": invoice.get('created_date'),
        "valid_until": invoice.get('valid_until'),
        "total_amount_no_vat": invoice.get('total_amount_no_vat'),
        "vat": invoice.get('vat'),
        "discount": invoice.get('discount'),
        "total_amount_with_discount": invoice.get('total_amount_with_discount'),
        "total_amount_with_vat": invoice.get('total_amount_with_vat'),
        "discount_description": invoice.get('discount_description'),
        "currency": invoice.get('currency'),
        "terms": invoice.get('terms'),
        "items": invoice.get('items'),
    } for invoice in invoices_documents]
    
    if not invoices:
        return jsonify({"invoices": [], "no_invoices": True})
    return jsonify({"invoices": invoices})
    

@invoices_router.route('/new', methods=['POST'])
@limiter.limit("3000 per minute")
@require_api_key
def create_new_invoice() -> dict:
    new_invoice = request.json
    new_invoice['_id'] = str(uuid4())
    new_invoice['type'] = "invoice"
    new_invoice['number'] = new_invoice['created_date'].replace("-","") + str(random.randint(000, 999))
    new_invoice['state'] = "draft"

    if not new_invoice.get('name'):
        return jsonify({"error": "Invoice name is required"}), 400

    else:
        push_update_in_collection(data = new_invoice, document_to_update = "invoice", mode = "create")
        return jsonify({"message": "invoice added successfully"})
    


@invoices_router.route('/update', methods=['PUT'])
@limiter.limit("3000 per minute")
@require_api_key
def update_invoice() -> dict:

    posted_data = request.get_json()

    invoice_data = {
        '_id': posted_data.get('_id'),
        'state': posted_data.get('state') if posted_data.get('state') else 'draft',
    }

    push_update_in_collection(data = invoice_data, document_to_update = "invoice", mode = "update")
    return jsonify({"message": "Invoice updated successfully"})



@invoices_router.route('/delete', methods=['DELETE'])
@limiter.limit("3000 per minute")
@require_api_key
def delete_existing_invoice() -> dict:

    posted_data = request.get_json() or {}
    invoice_data = {
        '_id': posted_data.get('_id'),
        'type': 'invoice'
    }
    push_update_in_collection(data = invoice_data, document_to_update = "invoice", mode = "delete")
    return jsonify({"message": "Invoice deleted successfully"})
