import streamlit as st


#Adding the credential for every member of the BDF

USER_CREDENTIAL = {
    "Didier" : "BDF123",
    "Côme" : "",
    "Baptiste" : "",
}

def login(): 
    st.title("Page de Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    #Check the login credentials
    if login_button:
        if username in USER_CREDENTIAL and USER_CREDENTIAL[username] == password:
            st.session_state['logged_in'] = True
            st.succces("Vous etes connecté")
        else: 
            st.error("Identifiant incorrect")

def autheticated_page():
    st.title("Welcome to the Dashboard")
    st.write("You are logged in ")


def logout():
    st.session_state['logged_in'] = False

#Main app 
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    autheticated_page()
    st.button("Logout",on_click=logout)
else:
    login()