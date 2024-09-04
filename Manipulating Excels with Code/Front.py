import streamlit as st


#Adding the credential for every member of the BDF

USER_CREDENTIALS = {
    "Didier" : "BDF123",
    "Côme": "",
    "Baptiste":"",
}

def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    # Check login credentials
    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Login successful")
            st.rerun() 
        else:
            st.error("Invalid username or password")

# Function to display a specific page for user1
def user1_page():
    st.title("Bonjour, Didier")
    st.write("This is your personalized dashboard.")
    # Add user-specific content here
    st.write("You can access exclusive features as Didier.")

# Function to display a general page for other users
def general_page():
    st.title(f"Welcome, {st.session_state['username']}!")
    st.write("This is the general dashboard.")
    # Add general content for other users
    st.write("You have access to standard features.")

# Logout function
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None

# Page selection (authenticated content)
def page_selector():
    # Check if the logged-in user is user1 or another user
    if st.session_state['username'] == "Didier":
        user1_page()  # Show specific content for user1
    else:
        general_page()  # Show general content for all other users

# Main app
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    st.sidebar.title("Navigation")
    page_selector()  # Show user-specific pages based on the logged-in user
    if st.sidebar.button("Logout"):
        logout()
else:
    login()