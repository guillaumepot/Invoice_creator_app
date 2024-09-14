from dataclasses import dataclass, field
from datetime import datetime, timedelta
import requests

# Classes
@dataclass(frozen=False, kw_only=True, order=False, slots=False)
class Company:
    company_name: str
    address: str
    zipcode: int
    city: str
    country: str
    phone: str
    email: str
    siret: str
    vat_number: str

    def to_dict(self):
        return {
            'company_name': self.company_name,
            'address': self.address,
            'zipcode': self.zipcode,
            'city': self.city,
            'country': self.country,
            'phone': self.phone,
            'email': self.email,
            'siret': self.siret,
            'vat_number': self.vat_number
        }

    def __str__(self):
        return f"{self.company_name} - {self.address} - {self.zipcode} - {self.city} - {self.country} - {self.phone} - {self.email} - {self.siret} - {self.vat_number}"

@dataclass(frozen=False, kw_only=True, order=False, slots=False)
class Item:
    description: str
    hour_rate: float = 0
    quantity: float = 0
    unit: str = 'hour'
    daily_rate: float = 0
    total: float = 0

    def __post_init__(self):
        self.daily_rate = 8 * self.hour_rate
        self.total = self.hour_rate * self.quantity
        self.hour_rate = "{:.2f}".format(self.hour_rate)
        self.daily_rate = "{:.2f}".format(self.daily_rate)

    def to_dict(self):
        return {
            'description': self.description,
            'hour_rate': self.hour_rate,
            'quantity': self.quantity,
            'unit': self.unit,
            'daily_rate': self.daily_rate,
            'total': self.total
        }

    def __str__(self):
        return f"{self.description} - {self.total}"

date_format: dict = {
    'en': '%Y-%m-%d',
    'fr': '%d-%m-%Y',
}


# Config
url: str = 'http://127.0.0.1:5000/invoice'
due_date_days: int = 45
currency: str = '€'
language: str = 'fr' # en, fr


company = Company(
    company_name='My company name',
    address='XX rue XXX',
    zipcode=75000,
    city='Paris',
    country='France',
    phone='01 23 45 67 89',
    email='mail@mail.com',
    siret='123456789123',
    vat_number='12345678912345'
)

customer = Company(
    company_name='Incredible Hulk',
    address='Hulk Street',
    zipcode=75000,
    city='Paris',
    country='France',
    phone='555 555 555',
    email='Hulk@incredible.com',
    siret='465464161',
    vat_number='1651691'
)

items = [
    Item(description='Description item 1', hour_rate=50.00, quantity=2, unit= 'hour').to_dict(),
    Item(description='Description item 2', hour_rate=50.00, quantity=2, unit= 'hour').to_dict(),
    Item(description='Description item 3', hour_rate=50.00, quantity=2, unit= 'hour').to_dict(),
]


if __name__ == '__main__':
    series_nb: str = input('Enter the series number: ')

    created_date = datetime.today().strftime(date_format['fr'])
    invoice_nb = f"{created_date.replace('-', '')}{series_nb}"

    # due date
    created_date_obj = datetime.strptime(created_date, date_format['fr'])
    due_date_obj = created_date_obj + timedelta(days=due_date_days)
    due_date = due_date_obj.strftime(date_format['fr'])

    # data
    data = {
        'language': language,
        'invoice_nb': invoice_nb,
        'created_date': created_date,
        'due_date': due_date,
        'currency': currency,
        'company': company.to_dict(),
        'customer': customer.to_dict(),
        'items': items
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(f'../documents/invoice_{invoice_nb}.pdf', 'wb') as f:
            f.write(response.content)
        print(f"Invoice successfully created and saved as invoice_{invoice_nb}.pdf")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")