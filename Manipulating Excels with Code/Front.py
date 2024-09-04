import streamlit as st
import openpyxl
import os
#Adding the credential for every member of the BDF



# Define a directory to store the uploaded Excel file globally
EXCEL_FILE_PATH = "shared_excel.xlsx"
PLAYER_LIST_FILE_PATH = "List_of_Player.xlsx"
#Membre de la bdf + Session Invité
USER_CREDENTIALS = {
    #Add to didier la possibilité de dire qui l'a kill aussi en super user
    "Didier" : "BDF123",
    "Côme": "",
    "Baptiste":"",
    "Steve":"",
    "Nico":"",
    "Béa":"",
    "Chris":"",
    "Issam":"",
    "Marco":"",
    "Fanny":"",
    "Guigui":"",
    "Gégé":"",
    "Lucas":"",
    "Pat":"",
    "Dylan":"",
    "Maxime":"",
    "Hugo W":"",
    "Marine":"",
    "Yohan":"",
    "Sylvie P":"",
    "Tony":"",
    "Gérard":"",
    "Chloé":"",
    "Pierrot":"",
    "Come":"",
    "Baptiste":"",
    "Flo":"",
    "Sylvie B":"",
    "Gaby":"",
    "Greg":"",
    #Session invité particuliere, tu choisis ton nom
    "Invités":"",

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


def modify_excel(workbook, sheet_name, cell, value):
    if workbook and sheet_name in workbook.sheetnames:
        worksheet = workbook[sheet_name]
        worksheet[cell] = value
    return workbook
# Function to save the workbook globally
def save_excel(workbook, file_path):
    workbook.save(file_path)

# Function to load the Excel file using openpyxl
def load_excel_with_openpyxl(file_url=None):
    if os.path.exists(file_url):
        workbook = openpyxl.load_workbook(file_url)
        return workbook
    return None
    

# Function to display a specific page for user1
def user1_page(): 
    st.title("Panneau Admin Didier")
    st.write("Dashboard personnalisé")

    # Upload the first file (Excel to modify)
    uploaded_file = st.file_uploader("Charge l'excel à compléter", type=["xlsx"], key="excel_upload")
    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file  # Store in session state temporarily
        if st.button("Submit Excel File"):  # Submit button for the Excel file
            with open(EXCEL_FILE_PATH, "wb") as f:
                f.write(st.session_state['uploaded_file'].getbuffer())  # Save the Excel file
            st.success("Excel file uploaded and saved globally!")
    else:
        st.info("Please upload the Excel file to be modified.")
    
    # Upload the second file (list of players)
    uploaded_file_list_player = st.file_uploader("Upload la liste des joueurs", type=["xlsx"], key="player_list_upload")
    if uploaded_file_list_player is not None:
        st.session_state['uploaded_file_list_player'] = uploaded_file_list_player  # Store in session state temporarily
        if st.button("Submit Player List"):  # Submit button for the Player List
            with open(PLAYER_LIST_FILE_PATH, "wb") as f:
                f.write(st.session_state['uploaded_file_list_player'].getbuffer())  # Save the List of Players file
            st.success("List of players file uploaded and saved globally!")
    else:
        st.info("Please upload the list of players file.")

# Function to display a general page for other users
def general_page():
    st.title(f"Welcome, {st.session_state['username']}!")
    st.write("Gestion des kills")
    if not os.path.exists(EXCEL_FILE_PATH):
        st.error("No Excel file uploaded by the special user yet.")
        return
    
    # Load the workbook from the shared file path
    workbook = load_excel_with_openpyxl(EXCEL_FILE_PATH)
    
    if workbook is None:
        st.error("There was an issue loading the Excel file.")
        return

    # Let the user choose the sheet and cell to update
    sheet_names = workbook.sheetnames
    selected_sheet = st.selectbox("Select the sheet to modify", sheet_names)
    
    cell = st.text_input("Enter the cell to modify (e.g., A1):")
    new_value = st.text_input("Enter the new value:")

    if st.button("Apply Changes"):
        if cell and new_value:
            workbook = modify_excel(workbook, selected_sheet, cell, new_value)
            save_excel(workbook, EXCEL_FILE_PATH)
            st.success(f"Cell {cell} updated successfully with '{new_value}'!")

    # Provide a download button for the modified Excel file
    with open(EXCEL_FILE_PATH, "rb") as f:
        st.download_button(
            label="Download Updated Excel",
            data=f,
            file_name="modified_excel.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
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