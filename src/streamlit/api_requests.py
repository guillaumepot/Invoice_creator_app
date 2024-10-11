import requests
import streamlit as st


# API URL & PORT
api_url = "localhost"
api_port = 5000



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



def request_logout():
    url = f"http://{api_url}:{api_port}/logout"
    response = st.session_state.session.post(url)
    if response.status_code == 200:
        st.session_state.api_key = False
        st.rerun()



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



def fetch_clients():
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



def create_new_client(client_data):
    url = f"http://{api_url}:{api_port}/clients"
    response = st.session_state.session.post(url, json=client_data)
    if response.status_code == 200:
        st.success("Client created successfully.")
    else:
        st.error("Failed to create client.")
        st.error(response.text)



def fetch_items():
    url = f"http://{api_url}:{api_port}/items"
    response = st.session_state.session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch items.")
        st.error(response.text)
        return {}
    


def update_item(item_data):
    st.write(item_data)
    url = f"http://{api_url}:{api_port}/items"
    response = st.session_state.session.put(url, json=item_data)
    if response.status_code == 200:
        st.success("Item updated successfully.")
    else:
        st.error("Failed to update item.")



def delete_item(item_data):
    url = f"http://{api_url}:{api_port}/items"
    response = st.session_state.session.delete(url, json={"_id": item_data})
    if response.status_code == 200:
        st.success("Item deleted successfully.")
    else:
        st.error("Failed to delete item.")
        st.error(response.text)


def create_new_item(item_data):
    url = f"http://{api_url}:{api_port}/items"
    response = st.session_state.session.post(url, json=item_data)
    if response.status_code == 200:
        st.success("Item created successfully.")
    else:
        st.error("Failed to create item.")
        st.error(response.text)



def fetch_quotes():
    url = f"http://{api_url}:{api_port}/quotes"
    response = st.session_state.session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch quotes.")
        st.error(response.text)
        return {}
    

def update_quote(quote_data):
    st.write(quote_data)
    url = f"http://{api_url}:{api_port}/quotes"
    response = st.session_state.session.put(url, json=quote_data)
    if response.status_code == 200:
        st.success("Item updated successfully.")
    else:
        st.error("Failed to update item.")



def delete_quote(quote_data):
    url = f"http://{api_url}:{api_port}/quotes"
    response = st.session_state.session.delete(url, json={"_id": quote_data})
    if response.status_code == 200:
        st.success("Item deleted successfully.")
    else:
        st.error("Failed to delete item.")
        st.error(response.text)

    

def create_new_quote(quote_data):
    url = f"http://{api_url}:{api_port}/quotes"
    response = st.session_state.session.post(url, json=quote_data)
    if response.status_code == 200:
        st.success("Quote created successfully.")
    else:
        st.error("Failed to create quote.")
        st.error(response.text)










