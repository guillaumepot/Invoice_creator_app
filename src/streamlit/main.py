"""
### STREAMLIT APP - Main file ###
"""

# LIBS
import datetime
import requests
import streamlit as st

from api_requests import *


# Set page configuration
st.set_page_config(layout="wide")



# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = False
if 'status' not in st.session_state:
    st.session_state.status = None
if 'lang' not in st.session_state:
    st.session_state.lang = "en"
if 'prev_lang' not in st.session_state:
    st.session_state.prev_lang = st.session_state.lang
if 'session' not in st.session_state:
    st.session_state.session = requests.Session()




### SIDEBAR ###

# Navigation
st.sidebar.title("My company companion app")


# Authentication panel
st.sidebar.subheader("Authentication")
if st.session_state.api_key == False:

    # Display error message if not logged in on the main page
    st.error("Please Log In to access the app.")


    api_key_field_value = st.sidebar.text_input("API Key", type="password")
    st.sidebar.button("Log In", on_click=request_check_api_key, args=(api_key_field_value,))
    st.stop()



else:
    # Logout button
    st.sidebar.empty()
    if st.sidebar.button("Log Out", on_click=request_logout):
        st.session_state.api_key = False
        st.rerun()



    # Change language
    st.sidebar.subheader("Language")
    lang = st.sidebar.radio("Select language", ["English", "Français"])

    if lang != st.session_state.prev_lang:
        st.session_state.lang = "en" if lang == "English" else "fr"
        st.session_state.prev_lang = lang
        st.rerun()



## END OF SIDEBAR ##


## PAGES
page_names = {
    'en': ["Overview", "My Company", "Clients", "Items", "Quotes", "Invoices", "Settings"],
    'fr': ["Vue d'ensemble", "Mon entreprise", "Clients", "Articles", "Devis", "Factures", "Paramètres"]
}

pages = [page_names[st.session_state.lang][i] for i in range(7)]
page = st.sidebar.radio("Navigation", pages)


if page == pages[0]: # Overview
    st.subheader(page_names[st.session_state.lang][0])

    ### WIP ###

if page == pages[1]: # My Company
    st.title(page_names[st.session_state.lang][1])

    # Fetch my company informations
    data = fetch_my_company_informations()

    if data:
        keys_order = ["name", "address", "zipcode", "city", "country", "email", "phone", "siret", "vat_number", "iban", "bic"]
        updated_data = {}
        for key in keys_order:
            value = data.get(key)
            input_value = st.text_input(label=f"{key.capitalize()}", value=value, key=key)
            updated_data[key] = input_value if input_value else None            
        if st.button("Update"):
            update_my_company(updated_data)
            st.rerun()



if page == pages[2]:  # Clients

    # Add new child pages
    subpages_name = {
        'en': ["Client List", "New Client"],
        'fr': ["Liste des clients", "Nouveau client"]
    }
    subpages = [subpages_name[st.session_state.lang][i] for i in range(len(subpages_name[st.session_state.lang]))]
    subpage = st.sidebar.radio("Clients", subpages)


    if subpage == subpages[0]:  # Client List
        st.title(subpages_name[st.session_state.lang][0])


        data = fetch_clients()
        
        if "clients" in data:
            sorted_clients = sorted(data["clients"], key=lambda client: client["name"])

            for client in sorted_clients:
                with st.expander(client["name"], expanded=False):
                    # First row
                    keys_order_row1 = ["name", "address", "zipcode", "city", "country"]
                    column_widths_row1 = [3, 4, 2, 1, 1]
                    cols_row1 = st.columns(column_widths_row1)
                    for col, key in zip(cols_row1, keys_order_row1):
                        unique_key = f"{client['_id']}_{key}"
                        col.text_input(key.capitalize(), client.get(key, ""), key=unique_key)

                    # Second row
                    keys_order_row2 = ["email", "phone", "siret", "vat_number"]
                    column_widths_row2 = [3, 2, 2, 2]
                    cols_row2 = st.columns(column_widths_row2)
                    for col, key in zip(cols_row2, keys_order_row2):
                        unique_key = f"{client['_id']}_{key}"
                        col.text_input(key.capitalize(), client.get(key, ""), key=unique_key)

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Update", key=f"update_{client['_id']}"):
                            updated_client_data = {}
                            updated_client_data["_id"] = client["_id"]
                            for key in keys_order_row1 + keys_order_row2:
                                unique_key = f"{client['_id']}_{key}"
                                updated_client_data[key] = st.session_state.get(unique_key, client.get(key, ""))

                            update_client(updated_client_data)
                            #st.rerun()
                    with col2:
                        if st.button("Delete", key=f"delete_{client['_id']}"):
                            delete_client(client["_id"])
                            st.rerun()
                            
        else:
            st.write("No clients found.")




    elif subpage == subpages[1]: # New Client
        st.title(subpages_name[st.session_state.lang][1])


        # First row
        keys_order_row1 = ["name", "address", "zipcode", "city", "country"]
        column_widths_row1 = [3, 4, 2, 1, 1]
        cols_row1 = st.columns(column_widths_row1)
        client_data_row1 = {}
        for col, key in zip(cols_row1, keys_order_row1):
            client_data_row1[key] = col.text_input(key.capitalize(), key=key)

        # Second row
        keys_order_row2 = ["email", "phone", "siret", "vat_number"]
        column_widths_row2 = [3, 2, 2, 2]
        cols_row2 = st.columns(column_widths_row2)
        client_data_row2 = {}
        for col, key in zip(cols_row2, keys_order_row2):
            client_data_row2[key] = col.text_input(key.capitalize(), key=key)

        # Combine client data from both rows
        client_data = {**client_data_row1, **client_data_row2}

        if st.button("Create"):
            create_new_client(client_data)




if page == pages[3]: # Items


    # Add new child pages
    subpages_name = {
        'en': ["Item List", "New Item"],
        'fr': ["Liste des articles", "Nouvel article"]
    }
    subpages = [subpages_name[st.session_state.lang][i] for i in range(len(subpages_name[st.session_state.lang]))]
    subpage = st.sidebar.radio("Items", subpages)

    if subpage == subpages[0]:  # Item List
        st.title(subpages_name[st.session_state.lang][0])

        data = fetch_items()
            
        
        if "items" in data:
            sorted_items = sorted(data["items"], key=lambda item: item["name"])

            for item in sorted_items:
                with st.expander(item["name"], expanded=False):
                    # First row
                    keys_order_row1 = ["name", "description"]
                    column_widths_row1 = [1, 2]
                    cols_row1 = st.columns(column_widths_row1)
                    for col, key in zip(cols_row1, keys_order_row1):
                        unique_key = f"{item['_id']}_{key}"
                        col.text_input(key.capitalize(), item.get(key, ""), key=unique_key)

                    # Second row
                    keys_order_row2 = ["unit", "rate"]
                    column_widths_row2 = [2, 1]
                    cols_row2 = st.columns(column_widths_row2)
                    for col, key in zip(cols_row2, keys_order_row2):
                        unique_key = f"{item['_id']}_{key}"
                        col.text_input(key.capitalize(), item.get(key, ""), key=unique_key)

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Update", key=f"update_{item['_id']}"):
                            updated_item_data = {}
                            updated_item_data["_id"] = item["_id"]
                            for key in keys_order_row1 + keys_order_row2:
                                unique_key = f"{item['_id']}_{key}"
                                updated_item_data[key] = st.session_state.get(unique_key, item.get(key, ""))

                            update_item(updated_item_data)
                            st.rerun()
                    with col2:
                        if st.button("Delete", key=f"delete_{item['_id']}"):
                            delete_item(item["_id"])
                            st.rerun()
                            
        else:
            st.write("No items found.")


    elif subpage == subpages[1]: # New Item
        st.title(subpages_name[st.session_state.lang][1])

        # First row
        keys_order_row1 = ["name", "description"]
        column_widths_row1 = [1,2]
        cols_row1 = st.columns(column_widths_row1)
        item_data_row1 = {}
        for col, key in zip(cols_row1, keys_order_row1):
            item_data_row1[key] = col.text_input(key.capitalize(), key=key)

        # Second row
        keys_order_row2 = ["unit", "rate"]
        column_widths_row2 = [2, 1]
        cols_row2 = st.columns(column_widths_row2)
        item_data_row2 = {}
        for col, key in zip(cols_row2, keys_order_row2):
            item_data_row2[key] = col.text_input(key.capitalize(), key=key)

        # Combine item data from both rows
        item_data = {**item_data_row1, **item_data_row2}

        if st.button("Create"):
            create_new_item(item_data)




if page == pages[4]:  # Quotes

    # Add new child pages
    subpages_name = {
        'en': ["Quote List", "New Quote"],
        'fr': ["Liste des devis", "Nouveau devis"]
    }
    subpages = [subpages_name[st.session_state.lang][i] for i in range(len(subpages_name[st.session_state.lang]))]
    subpage = st.sidebar.radio("Quotes", subpages)

    if subpage == subpages[0]:  # Quote List
        st.title(subpages_name[st.session_state.lang][0])
        

        # Fetch quotes
        data = fetch_quotes()

        if "quotes" in data:
            sorted_quotes = sorted(data["quotes"], key=lambda quote: quote["name"])

            for quote in sorted_quotes:
                with st.expander(quote["name"], expanded=False):

                    # First row
                    keys_order_row1 = ["name", "number"]
                    column_widths_row1 = [1, 1]
                    cols_row1 = st.columns(column_widths_row1)
                    for col, key in zip(cols_row1, keys_order_row1):
                        st.text(key.capitalize() + ": " + str(quote.get(key, "")))
                    
                    # Second row
                    keys_order_row2 = ["client"]
                    column_widths_row2 = [1]
                    cols_row2 = st.columns(column_widths_row2)
                    for col, key in zip(cols_row2, keys_order_row2):
                        st.text(key.capitalize() + ": " + str(quote.get(key, "")))

                    # Third row
                    keys_order_row3 = ["created_date", "valid_until"]
                    column_widths_row3 = [1, 1]
                    cols_row3 = st.columns(column_widths_row3)
                    for col, key in zip(cols_row3, keys_order_row3):
                        col.text(key.capitalize() + ": " + str(quote.get(key, "")))

                    # Fourth row
                    keys_order_row4 = ["total_amount_no_vat", "vat"]
                    column_widths_row4 = [2, 1]
                    cols_row4 = st.columns(column_widths_row4)
                    for col, key in zip(cols_row4, keys_order_row4):
                        col.text(key.capitalize() + ": " + str(quote.get(key, "")))

                    # Fifth row
                    keys_order_row5 = ["total_amount_with_discount", "discount"]
                    column_widths_row5 = [2, 1]
                    cols_row5 = st.columns(column_widths_row5)
                    for col, key in zip(cols_row5, keys_order_row5):
                        col.text(key.capitalize() + ": " + str(quote.get(key, "")))

                    # Sixth row
                    keys_order_row6 = ["total_amount_with_vat"]
                    column_widths_row6 = [1]
                    cols_row6 = st.columns(column_widths_row6)
                    for col, key in zip(cols_row6, keys_order_row6):
                        col.text(key.capitalize() + ": " + str(quote.get(key, "")))

                    # Seventh row
                    keys_order_row7 = ["currency", "discount_description"]
                    column_widths_row7 = [1, 3]
                    cols_row7 = st.columns(column_widths_row7)
                    for col, key in zip(cols_row7, keys_order_row7):
                        col.text(key.capitalize() + ": " + str(quote.get(key, "")))

                    # Eighth row
                    keys_order_row8 = ["items"]
                    for key in keys_order_row8:
                        items = quote.get(key, [])
                        if isinstance(items, list):
                            items_str = ", ".join([str(item) for item in items])
                        else:
                            items_str = str(items)
                        st.text(key.capitalize() + ": " + items_str)

                    # Ninth row
                    keys_order_row9 = ["description"]
                    column_widths_row9 = [1]
                    cols_row9 = st.columns(column_widths_row9)
                    for col, key in zip(cols_row9, keys_order_row9):
                        col.text(key.capitalize() + ": " + str(quote.get(key, "")))

                    # Tenth row
                    keys_order_row10 = ["terms"]
                    column_widths_row10 = [1]
                    cols_row10 = st.columns(column_widths_row10)
                    for col, key in zip(cols_row10, keys_order_row10):
                        col.text(key.capitalize() + ": " + str(quote.get(key, "")))


                    # Define columns for buttons
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Delete", key=f"delete_{quote['_id']}"):
                            delete_quote(quote["_id"])
                            st.rerun()

        else:
            st.write("No quotes found.")



    elif subpage == subpages[1]:  # New Quote
        st.title(subpages_name[st.session_state.lang][1])

        # Fetch clients and items data
        clients_data = fetch_clients()
        items_data = fetch_items()

        col1, col2 = st.columns(2)
        with col1:
            quote_name = st.text_input("Name")
            client_names = [client["name"] for client in clients_data.get("clients", [])]
            selected_client = st.selectbox("Client", client_names)

        with col2:
            # Quote details input fields
            created_date = st.date_input("Created Date", value=datetime.date.today())
            valid_until = st.date_input("Valid Until", value=datetime.date.today() + datetime.timedelta(days=30))

        with st.expander("Currency, description, and terms", expanded=False):
            # Currency, notes, and terms
            currency = st.selectbox("Currency", ["EUR", "USD", "GBP"])
            description = st.text_area("Description")
            terms = st.text_area("Terms")

        with st.expander("Items", expanded=False):
            item_names = [item["name"] for item in items_data.get("items", [])]
            selected_items = st.multiselect("Select Items", item_names)
            item_quantities = {item: st.number_input(f"Quantity for {item}", min_value=0, value=1) for item in selected_items}

        with st.expander("Amounts", expanded=False):
            # VAT and discount
            vat = st.text_input("VAT", value="0%")
            discount = st.text_input("Discount", value="0%")
            discount_description = st.text_input("Discount Description")

        # Calculate amounts
        total_amount_no_vat = sum(float(items_data["items"][item_names.index(item)]["rate"]) * quantity for item, quantity in item_quantities.items())
        total_amount_with_discount = total_amount_no_vat * (1 - float(discount.strip('%')) / 100)
        vat_percentage = float(vat.strip('%')) / 100
        total_amount_with_vat = total_amount_with_discount * (1 + vat_percentage)

        # Create quote data
        quote_data = {
            "name": quote_name,
            "client": selected_client,
            "created_date": str(created_date),
            "valid_until": str(valid_until),
            "items": [
                {
                    "name": item,
                    "unit": items_data["items"][item_names.index(item)]["unit"],
                    "rate": items_data["items"][item_names.index(item)]["rate"],
                    "quantity": quantity
                }
                for item, quantity in item_quantities.items()
            ],
            "total_amount_no_vat": total_amount_no_vat,
            "total_amount_with_discount": total_amount_with_discount,
            "vat": vat,
            "total_amount_with_vat": total_amount_with_vat,
            "discount": discount,
            "discount_description": discount_description,
            "currency": currency,
            "description": description,
            "terms": terms
        }

        if st.button("Create"):
            create_new_quote(quote_data)



if page == pages[5]: # Invoices

    # Add new child pages
    subpages_name = {
        'en': ["Invoice List", "New Invoice"],
        'fr': ["Liste des factures", "Nouvelle facture"]
    }
    subpages = [subpages_name[st.session_state.lang][i] for i in range(len(subpages_name[st.session_state.lang]))]
    subpage = st.sidebar.radio("Invoices", subpages)

    if subpage == subpages[0]:  # Invoice List
        st.title(subpages_name[st.session_state.lang][0])
        

        # Fetch invoices
        data = fetch_invoices()

        if "invoices" in data:
            sorted_invoices = sorted(data["invoices"], key=lambda invoice: invoice["name"])

            for invoice in sorted_invoices:
                with st.expander(invoice["name"], expanded=False):

                    # First row
                    keys_order_row1 = ["name", "number"]
                    column_widths_row1 = [1, 1]
                    cols_row1 = st.columns(column_widths_row1)
                    for col, key in zip(cols_row1, keys_order_row1):
                        st.text(key.capitalize() + ": " + str(invoice.get(key, "")))
                    
                    # Second row
                    keys_order_row2 = ["state"]
                    column_widths_row2 = [1]
                    cols_row2 = st.columns(column_widths_row2)
                    for col, key in zip(cols_row2, keys_order_row2):
                        st.text(key.capitalize() + ": " + str(invoice.get(key, "")))
                        new_state = st.selectbox("Update State", ["draft", "sent", "paid", "cancelled"], key=f"state_{invoice['_id']}")
                        new_state = {"state": new_state, "_id": invoice["_id"]}
                        if st.button("Update", key=f"update_{invoice['_id']}"):
                            update_invoice_state(new_state)
                            st.rerun()


                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Delete", key=f"delete_{invoice['_id']}"):
                            delete_invoice(invoice["_id"])
                            st.rerun()


        else:
            st.write("No Invoice found.")




    elif subpage == subpages[1]:  # New Invoice
        st.title(subpages_name[st.session_state.lang][1])


        quotes = fetch_quotes()
        if "quotes" in quotes:
            sorted_quotes = sorted(quotes["quotes"], key=lambda quote: quote["name"])
            quote_name = st.selectbox("From quote", [quote["name"] for quote in sorted_quotes])
            quote = [quote for quote in sorted_quotes if quote["name"] == quote_name][0]

        else:
            st.warning("No quotes available.")
        

        company_data = fetch_my_company_informations()

        clients_data = fetch_clients()
        client = [client for client in clients_data.get("clients", []) if client["name"] == quote["client"]][0]

        col1, col2 = st.columns(2)
        with col1:
            created_date = st.date_input("Created Date", value=datetime.date.today())
        with col2:
            dure_date = st.date_input("Due Date", value=datetime.date.today() + datetime.timedelta(days=45))

        invoice_terms = st.text_area("Terms")


        invoice_data = {
            "name": f"{quote['name']}-invoice",
            "emitter": company_data,
            "client": client,
            "created_date": created_date.isoformat(),
            "due_date": dure_date.isoformat(),
            "items": quote["items"],
            "total_amount_no_vat": quote["total_amount_no_vat"],
            "total_amount_with_discount": quote["total_amount_with_discount"],
            "vat": quote["vat"],
            "total_amount_with_vat": quote["total_amount_with_vat"],
            "discount": quote["discount"],
            "discount_description": quote["discount_description"],
            "currency": quote["currency"],
            "description": quote["description"],
            "terms": invoice_terms,
            }


        if st.button("Create"):
            generate_invoice(invoice_data)


if page == pages[6]: # Settings
    st.title(page_names[st.session_state.lang][6])