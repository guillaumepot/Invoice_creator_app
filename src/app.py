from flask import Flask, render_template, send_file, request
import io
import os
from weasyprint import HTML

from config import host, port


# Flask
app = Flask(__name__)


# Home Route
@app.route('/')
def home():
    return 'Hello World!'



# Invoice Route
@app.route('/invoice', methods = ['GET', 'POST'])
def invoice():

    # Default data
    default_data = {
        'invoice_nb': '20240101001',
        'created_date': '2024-01-01',
        'due_date': '2024-02-16',
        'currency': '€',
        'company': {
            'company_name': 'My compagny name',
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
            'company_name': 'My customer company',
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
                'hour_rate': 50,
                'quantity': 2,
                'unit': 'hour',
                'total': 100,
                'daily_rate': 600,
            },
        ],
    }


    # Initialize variables with default data
    invoice_nb = default_data['invoice_nb']
    created_date = default_data['created_date']
    due_date = default_data['due_date']
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
    rendered = render_template('invoice.html',
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
    app.run(host=host, port=port, debug=False)