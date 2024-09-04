import streamlit as st
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
import io
import requests
#Adding the credential for every member of the BDF

USER_CREDENTIALS = {
    "Didier" : "BDF123",
    "Côme": "",
    "Baptiste":"",
}

st.set_page_config(page_title='Le Site de la BDF',page_icon="../logo_bdf.png")
st.image('../logo_bdf.png')

def login():
    st.title("Login Page")
    username = st.text_input("Utilisateur")
    password = st.text_input("Mot de passe", type="password")
    login_button = st.button("Connexion")

    # Check login credentials
    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Login successful")
            st.rerun() 
        else:
            st.error("Invalid username or password")


def modify_excel_with_openpyxl(workbook):
    # Create a new sheet or modify an existing one
    if "Modified Sheet" not in workbook.sheetnames:
        worksheet = workbook.create_sheet(title="Modified Sheet")
    else:
        worksheet = workbook["Modified Sheet"]

    # Add some data into the new sheet (example modification)
    worksheet["A1"] = "New Data"
    worksheet["A2"] = "More Data"

    # Example of modifying an existing sheet (optional)
    if "Sheet1" in workbook.sheetnames:
        existing_sheet = workbook["Sheet1"]
        existing_sheet["B1"] = "Modified Value"
    
    return workbook

# Function to load the Excel file using openpyxl
def load_excel_with_openpyxl(uploaded_file=None, file_url=None):
    if uploaded_file:
        # Read uploaded file
        workbook = load_workbook(uploaded_file)
        return workbook
    elif file_url:
        # Download file from the provided URL
        response = requests.get(file_url)
        file_bytes = io.BytesIO(response.content)
        workbook = load_workbook(file_bytes)
        return workbook
    else:
        return None
    

# Function to display a specific page for user1
def user1_page():
    st.title("Panneau Admin Didier")
    st.write("Dashboard personnalisé")
    #Genere bdf 9, bdf 10 excel
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
    # Text input to allow users to provide a URL
    file_url = st.text_input("Or enter the link to your Excel file")

    # Load the Excel file using openpyxl
    workbook = load_excel_with_openpyxl(uploaded_file, file_url)

    if workbook is not None:
        st.write("Original Excel File Loaded Successfully")

        # Modify the Excel file using openpyxl
        modified_workbook = modify_excel_with_openpyxl(workbook)

        # Save modified workbook to BytesIO object
        output = io.BytesIO()
        modified_workbook.save(output)
        output.seek(0)  # Reset the pointer to the beginning of the stream

        # Download modified Excel file
        st.download_button(
            label="Download Modified Excel",
            data=output,
            file_name="modified_excel.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.write("Please upload an Excel file or provide a link.")


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