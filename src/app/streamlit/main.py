"""
### STREAMLIT APP - Main file ###
"""

# LIBS
import requests
import streamlit as st


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


# API URL & PORT
api_url = "localhost"
api_port = 5000



### SIDEBAR ###

# Navigation
st.sidebar.title("My company companion app")


# Authentication panel
st.sidebar.subheader("Authentication")
if st.session_state.api_key == False:

    # Display error message if not logged in on the main page
    st.error("Please Log In to access the app.")

    def request_check_api_key(api_key):
        url = f"http://{api_url}:{api_port}/login"
        response = st.session_state.session.post(url, data={'api_key': api_key})

        if response.status_code == 200:
            st.session_state.api_key = True
            st.session_state.status = "Logged In"
            st.success("Successfully logged in!")
        else:
            st.session_state.api_key = False
            st.session_state.status = "Login Failed"
            st.error("Failed to log in. Please check your API key.")

    api_key_field_value = st.sidebar.text_input("API Key", type="password")
    st.sidebar.button("Log In", on_click=request_check_api_key, args=(api_key_field_value,))
    st.stop()



else:
    # Logout button

    def request_logout():
        url = f"http://{api_url}:{api_port}/logout"
        response = st.session_state.session.post(url)
        if response.status_code == 200:
            st.session_state.api_key = False
            st.rerun()


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
    def fetch_my_company_informations():
        url = f"http://{api_url}:{api_port}/company/informations"
        response = st.session_state.session.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch company informations.")
            st.error(response.text)


    def update_my_company(updated_data):
        url = f"http://{api_url}:{api_port}/company/informations"
        response = st.session_state.session.put(url, json=updated_data)
        if response.status_code == 200:
            st.success("Company information updated successfully.")
        else:
            st.error("Failed to update company informations.")
            st.error(response.text)


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
        st.title(page_names[st.session_state.lang][2])

        def fetch_my_clients():
            url = f"http://{api_url}:{api_port}/clients"
            response = st.session_state.session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                st.error("Failed to fetch clients.")
                st.error(response.text)
                return {}
            
        def update_client(client_data):
            url = f"http://{api_url}:{api_port}/clients"
            response = st.session_state.session.put(url, json=client_data)
            st.write("Update request sent with data:", client_data)  # Debug statement
            if response.status_code == 200:
                st.success("Client updated successfully.")
            else:
                st.error("Failed to update client.")

        def delete_client(client_id):
            url = f"http://{api_url}:{api_port}/clients"
            response = st.session_state.session.delete(url, json={"_id": client_id})
            if response.status_code == 200:
                st.success("Client deleted successfully.")
            else:
                st.error("Failed to delete client.")
                st.error(response.text)

        data = fetch_my_clients()
        
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
        st.title(subpages_name[st.session_state.lang][0])

        def create_new_client(client_data):
            url = f"http://{api_url}:{api_port}/clients"
            response = st.session_state.session.post(url, json=client_data)
            if response.status_code == 200:
                st.success("Client created successfully.")
            else:
                st.error("Failed to create client.")
                st.error(response.text)

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
    st.title(page_names[st.session_state.lang][3])

if page == pages[4]: # Quotes
    st.title(page_names[st.session_state.lang][4])

if page == pages[5]: # Invoices
    st.title(page_names[st.session_state.lang][5])

if page == pages[6]: # Settings
    st.title(page_names[st.session_state.lang][6])