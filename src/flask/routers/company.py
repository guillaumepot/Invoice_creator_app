#api/routers/company.py


# Lib
from flask import Blueprint, jsonify, request


from services.mongo_connect import push_update_in_collection, fetch_collection
from services.security import require_api_key
from utils.limiter import limiter



"""
Router Declaration
"""
company_router = Blueprint('company', __name__)


"""
Routes Declaration
"""
@company_router.route('/info')
@limiter.limit("3000 per minute")
@require_api_key
def get_company_informations() -> dict:

    collection = fetch_collection()
    company_document = collection.find_one({"type": "company"})

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
        'iban': company_document.get('iban') if company_document else None,
        'bic': company_document.get('bic') if company_document else None,
    }

    return jsonify(company_data)



@company_router.route('/update', methods=['PUT'])
@limiter.limit("3000 per minute")
@require_api_key
def put_company_info() -> dict:

    posted_data = request.get_json()

    company_data = {
        'type': 'company',
        'name': posted_data.get('name') if posted_data.get('name') else None,
        'address': posted_data.get('address') if posted_data.get('address') else None,
        'zipcode': posted_data.get('zipcode') if posted_data.get('zipcode') else None,
        'city': posted_data.get('city') if posted_data.get('city') else None,
        'country': posted_data.get('country') if posted_data.get('country') else None,
        'phone': posted_data.get('phone') if posted_data.get('phone') else None,
        'email': posted_data.get('email') if posted_data.get('email') else None,
        'siret': posted_data.get('siret') if posted_data.get('siret') else None,
        'vat_number': posted_data.get('vat_number') if posted_data.get('vat_number') else None,
        'iban': posted_data.get('iban') if posted_data.get('iban') else None,
        'bic': posted_data.get('bic') if posted_data.get('bic') else None,
    }

    push_update_in_collection(data = company_data, document_to_update = "company")
    return jsonify(company_data)
