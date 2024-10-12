from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import requests



# Config
url: str = 'http://127.0.0.1:5000/invoice/template'
# Datas
due_date_days: int = 45
currency: str = '€'
language: str = 'fr' # en, fr



@dataclass(frozen=False, kw_only=True, order=False, slots=False)
class Item:
    description: str
    rate: float = 0
    quantity: float = 0
    unit: str = 'h'
    daily_rate: float = 0
    total: float = 0

    def __post_init__(self):
        self.daily_rate = 8 * self.rate
        self.total = self.rate * self.quantity
        self.rate = "{:.2f}".format(self.rate)
        self.daily_rate = "{:.2f}".format(self.daily_rate)

    def to_dict(self):
        return {
            'description': self.description,
            'rate': self.rate,
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


# Functions
def display_list(providers:dict) -> list:
    """
    
    """
    # Generate providers list to display
    i=1
    i_list = [1]
    for provider in providers:
        print(f"{i}. {provider}")
        i+=1
        i_list.append(i)
    print(f"{i}. Set new company \n")
    return i_list


def set_new_provider_customer(type="customer") -> dict:
    """

    """

    print(f"\n\n Setting new {type}")
    company_name = input('Enter the company name: ')
    address = input('Enter the address: ')
    zipcode = input('Enter the zipcode: ')
    city = input('Enter the city: ')
    country = input('Enter the country: ')
    phone = input('Enter the phone: ')
    email = input('Enter the email: ')
    siret = input('Enter the siret: ')
    vat_number = input('Enter the vat number: ')

    datas = {}
    # Append new type to type.json
    datas[company_name] = {
        'name': company_name,
        'address': address,
        'zipcode': zipcode,
        'city': city,
        'country': country,
        'phone': phone,
        'email': email,
        'siret': siret,
        'vat_number': vat_number
    }

    with open(f'./{type}s.json', 'w') as f:
        json.dump(datas, f, indent=4)
    print("\n\n New provider added successfully")

    return datas[company_name]


if __name__ == '__main__':

    print("Set Provider: \n")
    # Fetch providers
    with open('./providers.json', 'r') as f:
        providers = json.load(f)
    

    # Display providers list
    p_list = display_list(providers)
    
    # Get provider choice
    provider_choice_nb = int(input('Enter the provider number: '))

    # Loop while provider_choice is not in p_list
    while provider_choice_nb not in p_list:
        print("\n Invalid provider choice")
        provider_choice_nb = int(input('Enter the provider number: '))

    # Set new provider
    if provider_choice_nb == p_list[-1]:
        provider = set_new_provider_customer(type="provider")
        print(provider)

    # Set provider
    else:
        provider = providers[list(providers.keys())[provider_choice_nb-1]]

    
    print("\n Chosen provider:")
    print(provider)


    print("\n\nSet Customer: \n")
    # Fetch customers
    with open('./customers.json', 'r') as f:
        customers = json.load(f)
    

    # Display providers list
    c_list = display_list(customers)
    
    # Get provider choice
    customer_choice_nb = int(input('Enter the customer number: '))

    # Loop while provider_choice is not in c_list
    while customer_choice_nb not in c_list:
        print("\n Invalid customer choice")
        customer_choice_nb = int(input('Enter the customer number: '))

    # Set new customer
    if customer_choice_nb == c_list[-1]:
        customer = set_new_provider_customer()
        print(customer)

    # Set customer
    else:
        customer = customers[list(customers.keys())[customer_choice_nb-1]]

    
    print("\n Chosen customer:")
    print(customer)


    # Set items
    print("\nSet Items: \n")
    items_nb = int(input('Enter the number of items: '))
    items = []
    for i in range(items_nb):
        print(f"\nItem {i+1}")
        description = input('Enter the description: ')
        quantity = float(input('Enter the quantity: '))
        unit = input('Enter the unit: ')
        rate = float(input('Enter the  rate: '))

        item = Item(description=description, rate=rate, quantity=quantity, unit=unit)
        items.append(item.to_dict())
        print("\nItem added: \n", item)
    

    # Generate data
    print("\n\n Generating invoice...")
    #created_date = datetime.today().strftime(date_format['en'])
    created_date = '2024-09-14'

    # Open emitted_invoices.json
    with open('./emitted_invoices.json', 'r') as f:
        emitted_invoices = json.load(f)


    # series_nb should be a format of three int '001'
    created_invoices_nb_today = [int(invoice_nb[-3:]) for invoice_nb in emitted_invoices.keys() if invoice_nb.startswith(created_date.replace('-', ''))]
    
    if created_invoices_nb_today:
        series_nb = str(max(created_invoices_nb_today) + 1).zfill(3)
    else:
        series_nb = '001'

    invoice_nb = f"{created_date.replace('-', '')}{series_nb}"
    #created_date = datetime.today().strftime(date_format[language])
    created_date = '14-09-2024'
    created_date_obj = datetime.strptime(created_date, date_format['fr'])
    due_date_obj = created_date_obj + timedelta(days=due_date_days)
    due_date = due_date_obj.strftime(date_format['fr'])


    data = {
        'language': language,
        'invoice_nb': invoice_nb,
        'created_date': created_date,
        'due_date': due_date,
        'currency': currency,
        'company': provider,
        'customer': customer,
        'items': items
    }


    # Request invoice
    print("\n\n Requesting invoice...")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        with open(f"../documents/{customer['name']}_{invoice_nb}.pdf", 'wb') as f:
            f.write(response.content)
        print(f"Invoice successfully created and saved as invoice_{invoice_nb}.pdf")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


    emitted_invoices[invoice_nb] = data

    with open('./emitted_invoices.json', 'w') as f:
        json.dump(emitted_invoices, f, indent=4)