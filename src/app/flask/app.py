from flask import Flask, render_template, send_file, request, jsonify
import io
import os
from weasyprint import HTML

from config import host, port, mongo_host, mongo_port

# Flask
app = Flask(__name__)


# Home
@app.route('/')
def home():
    return render_template('home.html')



# Login
@app.route('/login', methods = ['POST'])
def login() -> None:
    pass




# Companies
@app.route('/company/create', methods = ['POST'])
def create_company() -> None:
    pass

@app.route('/company/delete/<name:str>', methods = ['DELETE'])
def delete_company(name:str) -> None:
    pass

@app.route('/company/update/<name:str>', methods = ['PUT'])
def update_company(name:str) -> None:
    pass

@app.route('/company/get', methods = ['GET'])
def get_company() -> None:
    pass


# Items
@app.route('/item/create', methods = ['POST'])
def create_item() -> None:
    pass

@app.route('/item/delete/<name:str>', methods = ['DELETE'])
def delete_item(name:str) -> None:
    pass

@app.route('/item/update/<name:str>', methods = ['PUT'])
def update_item(name:str) -> None:
    pass

@app.route('/item/get', methods = ['GET'])
def get_item() -> None:
    pass





# Invoice Route
@app.route('/invoice/template', methods = ['GET', 'POST'])
def invoice():

    # Default data
    default_data = {
        'language': 'en',
        'invoice_nb': '20240101001',
        'created_date': '2024-01-01',
        'due_date': '2024-02-16',
        'currency': '€',
        'company': {
            'name': 'My compagny name',
            'address': 'XX rue XXXXXXX',
            'zipcode': 75000,
            'city': 'Paris',
            'country': 'France',
            'phone': '01 23 45 67 89',
            'email': 'mail@mail.com',
            'siret': '123456789123',
            'vat_number': '12345678912345',
        },
        'customer': {
            'name': 'My customer company',
            'address': 'XX rue XXXXXXXX',
            'zipcode': 75000,
            'city': 'Paris',
            'country': 'France',
            'phone': '01 23 45 67 89',
            'email': 'mail@mail.com',
            'siret': '123456789123',
            'vat_number': '12345678912345'
        },
        'items': [
            {
                'description': 'Description item 1',
                'rate': 50,
                'quantity': 2,
                'unit': 'h',
                'total': 100,
                'daily_rate': 600,
            },
            {
                'description': 'Description item 2',
                'rate': 50,
                'quantity': 3,
                'unit': 'h',
                'total': 150,
                'daily_rate': 600,
            },
        ],
    }


    # Initialize variables with default data
    language = default_data['language']
    invoice_nb = default_data['invoice_nb']

    created_date = default_data['created_date']
    due_date = default_data['due_date']
    if language == 'fr':
        created_date = default_data['created_date'].replace('-', '/')
        due_date = default_data['due_date'].replace('-', '/')
        # Format from Y/M-d to d/m/Y
        created_date = created_date[8:] + created_date[4:8] + created_date[:4]
        due_date = due_date[8:] + due_date[4:8] + due_date[:4]


    currency = default_data['currency']
    company = default_data['company']
    customer = default_data['customer']
    items = default_data['items']
    total_to_pay = sum([item['total'] for item in items])
    formatted_total_to_pay = "{:.2f}".format(total_to_pay)

    if request.method == 'POST':
        # Posted data
        posted_data = request.get_json() or {}

        # Generate vars
        language = posted_data.get('language', default_data['language'])
        invoice_nb = posted_data.get('invoice_nb', default_data['invoice_nb'])
        created_date = posted_data.get('created_date', default_data['created_date'])
        due_date = posted_data.get('due_date', default_data['due_date'])
        currency = posted_data.get('currency', default_data['currency'])
        company = posted_data.get('company', default_data['company'])
        customer = posted_data.get('customer', default_data['customer'])
        items = posted_data.get('items', default_data['items'])
        total_to_pay = sum([item['total'] for item in items])
        formatted_total_to_pay = "{:.2f}".format(total_to_pay)


    # Render invoice
    rendered = render_template(f'invoice_{language}.html',
                               invoice_nb=invoice_nb,
                               created_date=created_date,
                               due_date=due_date,
                               from_addr=company,
                               to_addr=customer,
                               items=items,
                               total=formatted_total_to_pay,
                               currency=currency,
                               )


    if request.method == 'GET':
        return rendered
    else:
        # Generate PDF and send it
        html = HTML(string=rendered, base_url=request.url_root)
        rendered_pdf = html.write_pdf()
        return send_file(
                io.BytesIO(rendered_pdf),
                download_name='invoice.pdf',
                as_attachment=True,
            )



# Start app
if __name__ == '__main__':
    host = os.environ.get("HOST", host)
    port = int(os.environ.get("PORT", port))
    app.run(host=host, port=port, debug=True)