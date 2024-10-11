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



if page == pages[1]: # My Company
    st.title(page_names[st.session_state.lang][1])

    # Fetch my company informations
    data = fetch_my_company_informations()

    if data:
        keys_order = ["name", "address", "zipcode", "city", "country", "email", "phone", "siret", "vat_number"]
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
                    keys_order_row1 = ["description"]
                    column_widths_row1 = [1]
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

        # Items selection within the expander but outside the form
        with st.expander("Items", expanded=False):
            item_names = [item["name"] for item in items_data.get("items", [])]
            selected_items = st.multiselect("Select Items", item_names)
            
            # Debug statement to check selected items
            st.write("Selected Items:", selected_items)
            
            # Ensure number input fields are created
            item_quantities = {item: st.number_input(f"Quantity for {item}", min_value=0, value=1) for item in selected_items}

        with st.expander("Amounts", expanded=False):
            # VAT and discount
            vat = st.text_input("VAT", value="0%")
            discount = st.text_input("Discount", value="0%")
            discount_description = st.text_input("Discount Description")

        with st.expander("Currency, notes, and terms", expanded=False):
            # Currency, notes, and terms
            currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])
            notes = st.text_area("Notes")
            terms = st.text_area("Terms")

        # Calculate amounts
        total_amount = sum(items_data["items"][item_names.index(item)]["rate"] * quantity for item, quantity in item_quantities.items())
        vat_percentage = float(vat.strip('%')) / 100
        total_amount_vat = total_amount * (1 + vat_percentage)

        # Create quote data
        quote_data = {
            "name": quote_name,
            "client": selected_client,
            "created_date": str(created_date),
            "valid_until": str(valid_until),
            "items": [{"name": item, "quantity": quantity} for item, quantity in item_quantities.items()],
            "total_amount": total_amount,
            "vat": vat,
            "total_amount_vat": total_amount_vat,
            "discount": discount,
            "discount_description": discount_description,
            "currency": currency,
            "notes": notes,
            "terms": terms
        }

        if st.button("Create"):
            st.warning("WIP")
            st.write(quote_data)
        # create_new_quote(quote_data)










if page == pages[5]: # Invoices
    st.title(page_names[st.session_state.lang][5])

if page == pages[6]: # Settings
    st.title(page_names[st.session_state.lang][6])