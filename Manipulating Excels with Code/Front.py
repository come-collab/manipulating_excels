import streamlit as st
import openpyxl
from openpyxl import load_workbook
import os
import pandas as pd
from collections import Counter
from datetime import datetime
#Adding the credential for every member of the BDF



# Define a directory to store the uploaded Excel file globally
EXCEL_FILE_PATH = "shared_excel.xlsx"
PLAYER_LIST_FILE_PATH = "List_of_Player.xlsx"
#Membre de la bdf + Session Invité
USER_CREDENTIALS = {
    #Add to didier la possibilité de dire qui l'a kill aussi en super user
    "Didier" : "",
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


# Function to load the Excel file and return a DataFrame
def load_excel_to_dataframe(file_path):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path, engine='openpyxl')  # Load the Excel file into a DataFrame
        return df
    return None


def load_excel_to_dataframe_2(file_path):
    try:
        df = pd.read_excel(file_path,skiprows=[0])
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None
    

def save_dataframe_to_excel(file_path, df, top_row_text="BDF Edition 9 "):
    try:
        # First, save the DataFrame to Excel
        df.to_excel(file_path, index=False)

        # Now, open the workbook and add the top row
        wb = load_workbook(file_path)
        ws = wb.active
        
        # Insert a new row at the top
        ws.insert_rows(1)
        
        # Add the text to cell A1 of the new row
        ws['A1'] = top_row_text

        # Save the modified workbook
        wb.save(file_path)
        
        st.success("Excel file saved successfully with top row inserted.")
    except Exception as e:
        st.error(f"Error saving Excel file: {e}")
def update_points(elimination_df):    
    # Define point allocation
    points = {1: 10, 2: 6, 3: 4, 4 : 2}
    
    # Update Points column
    elimination_df['Points'] = elimination_df['Classement'].map(lambda x: points.get(x, 0))
    
    return elimination_df


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
   # Upload the second file (list of players)
    uploaded_file_list_player = st.file_uploader("Upload la liste des joueurs", type=["xlsx"], key="player_list_upload")
    if uploaded_file_list_player is not None:
        st.session_state['uploaded_file_list_player'] = uploaded_file_list_player
        if st.button("Submit Player List"):
            with open(PLAYER_LIST_FILE_PATH, "wb") as f:
                f.write(st.session_state['uploaded_file_list_player'].getbuffer())
            st.success("List of players file uploaded and saved globally!")
            
            # Load the player list and the shared Excel file
            player_df = load_excel_to_dataframe(PLAYER_LIST_FILE_PATH)
            shared_df = load_excel_to_dataframe_2(EXCEL_FILE_PATH)
            
            if player_df is not None and shared_df is not None:
                # Get the number of players
                num_players = len(player_df)
                
                # Update the Classement column
                shared_df['Classement'] = range(1, num_players + 1)
                
                # Save the updated shared Excel file
                save_dataframe_to_excel(EXCEL_FILE_PATH, shared_df)
                
                st.success(f"Classement column updated with numbers 1 to {num_players}")
            else:
                st.error("Failed to load player list or shared Excel file")
    else:
        st.info("Please upload the list of players file.")
            # Add a new section for Didier to specify his elimination
    st.subheader("Gestion de votre élimination")

    # Check if the PLAYER_LIST file exists
    if not os.path.exists(PLAYER_LIST_FILE_PATH):
        st.error("No PLAYER_LIST Excel file uploaded yet.")
    else:
        player_df = load_excel_to_dataframe(PLAYER_LIST_FILE_PATH)
        
        if player_df is not None and "Joueur" in player_df.columns:
            players = player_df["Joueur"].dropna().unique()
            
            # Display a selectbox for Didier to select the player who eliminated him
            selected_player = st.selectbox("Qui vous a éliminé ?", players)

            if st.button("Confirmer votre élimination"):
                elimination_df = load_excel_to_dataframe_2(EXCEL_FILE_PATH)

                if elimination_df is not None:
                    last_empty_row = elimination_df['Joueur'].isna()[::-1].idxmax()
                    new_classement = elimination_df.loc[last_empty_row, 'Classement']
                    current_time = datetime.now().strftime("%H:%M")

                    new_row = pd.DataFrame({
                        "Classement": [new_classement],
                        "Joueur": ["Didier"],
                        "Heure": [current_time],
                        "Killer": [selected_player],
                        "Points": [None]
                    })

                    for column in new_row.columns:
                        elimination_df.at[last_empty_row, column] = new_row.at[0, column]

                    save_dataframe_to_excel(EXCEL_FILE_PATH, elimination_df)

                    st.success(f"Didier a bien mis à jour son élimination (Classement: {new_classement}, Heure: {current_time})")
                else:
                    st.error("Failed to load the elimination Excel file.")
        else:
            st.error("Failed to load the PLAYER_LIST Excel file or 'Joueur' column is missing.")
# Function to display a general page for other users
def general_page():
    st.title(f"Salut, {st.session_state['username']}!")
    st.write("Gestion des kills")
    
    # Check if the PLAYER_LIST file exists
    if not os.path.exists(PLAYER_LIST_FILE_PATH):
        st.error("No PLAYER_LIST Excel file uploaded by the admin yet.")
        return

    # Load the PLAYER_LIST Excel file to display the list of players
    player_df = load_excel_to_dataframe(PLAYER_LIST_FILE_PATH)
    
    if player_df is None:
        st.error("Failed to load the PLAYER_LIST Excel file.")
        return
    
    # Check if the "Joueur" column exists in PLAYER_LIST
    if "Joueur" not in player_df.columns:
        st.error("The PLAYER_LIST file does not contain a 'Joueur' column.")
        return
    
    # Extract the list of players from the "Joueur" column in PLAYER_LIST
    players = player_df["Joueur"].dropna().unique()  # Remove any NaN values and get unique player names
    # Count the number of players
    number_of_players = Counter(players)

    # Display a selectbox for the user to select the player who eliminated them
    selected_player = st.selectbox("Qui vous a éliminé ?", players)

    # Get the current user from session state
    current_user = st.session_state['username']

    # Load the EXCEL_FILE_PATH which will be updated with elimination information
    if not os.path.exists(EXCEL_FILE_PATH):
        st.error("No elimination Excel file found.")
        return

    elimination_df = load_excel_to_dataframe_2(EXCEL_FILE_PATH)


    if elimination_df is None:
        st.error("Failed to load the elimination Excel file.")
        return
     # Normalize column names by stripping whitespace
    elimination_df.columns = elimination_df.columns.str.strip()
    
    # Check if the necessary columns exist in the elimination Excel file
    required_columns = ["Classement", "Joueur", "Heure", "Killer", "Points"]
    if not all(column in elimination_df.columns for column in required_columns):
        st.error(f"The elimination Excel file does not contain the necessary columns: {required_columns}")
        st.write(f"Found columns: {elimination_df.columns.tolist()}")
        return

    # Handle user elimination logic
    if st.button("Confirmer l'élimination"):
        # Load the current elimination data
        elimination_df = load_excel_to_dataframe_2(EXCEL_FILE_PATH)

        if elimination_df is None:
            st.error("Failed to load the elimination Excel file.")
            return

        # Find the last empty row (where 'Joueur' is NaN)
        last_empty_row = elimination_df['Joueur'].isna()[::-1].idxmax()

        # Find the corresponding Classement value for this position
        new_classement = elimination_df.loc[last_empty_row, 'Classement']

        # Get the current time
        current_time = datetime.now().strftime("%H:%M")

        # Prepare the new row with the current user's information
        new_row = pd.DataFrame({
            "Classement": [new_classement],
            "Joueur": [current_user],
            "Heure": [current_time],
            "Killer": [selected_player],
            "Points": [None]  # Add 'Points' value if needed, otherwise keep it as None
        })

        # Replace the following line:
        # elimination_df.loc[last_empty_row] = new_row.iloc[0]
        
        # With these lines:
        for column in new_row.columns:
            elimination_df.at[last_empty_row, column] = new_row.at[0, column]

        print("new_row", new_row)
        updated_df = update_points(elimination_df)
        print("elimination_df", elimination_df)

        # Save the updated DataFrame back to the elimination Excel file
        save_dataframe_to_excel(EXCEL_FILE_PATH, updated_df)

        st.success(f"{current_user} a bien mis à jour son élimination (Classement: {new_classement}, Heure: {current_time})")


def invited_user_page():
    st.title("Page Invités")
    st.write("Sélectionnez votre nom et indiquez qui vous a éliminé")

    # Load the player list
    player_df = load_excel_to_dataframe(PLAYER_LIST_FILE_PATH)
    
    if player_df is None or "Joueur" not in player_df.columns:
        st.error("Impossible de charger la liste des joueurs.")
        return
    
    all_players = player_df["Joueur"].dropna().unique()
    invited_players = [player for player in all_players if player not in USER_CREDENTIALS]

    if not invited_players:
        st.error("Aucun joueur invité disponible.")
        return

    # Let the invited user select their name
    selected_name = st.selectbox("Sélectionnez votre nom", invited_players)

    # Let the user select who eliminated them (from all players)
    selected_killer = st.selectbox("Qui vous a éliminé ?", all_players)

    if st.button("Confirmer l'élimination"):
        elimination_df = load_excel_to_dataframe_2(EXCEL_FILE_PATH)

        if elimination_df is None:
            st.error("Impossible de charger le fichier d'élimination.")
            return

        last_empty_row = elimination_df['Joueur'].isna()[::-1].idxmax()
        new_classement = elimination_df.loc[last_empty_row, 'Classement']
        current_time = datetime.now().strftime("%H:%M")

        new_row = pd.DataFrame({
            "Classement": [new_classement],
            "Joueur": [selected_name],
            "Heure": [current_time],
            "Killer": [selected_killer],
            "Points": [None]
        })

        for column in new_row.columns:
            elimination_df.at[last_empty_row, column] = new_row.at[0, column]

        save_dataframe_to_excel(EXCEL_FILE_PATH, elimination_df)

        st.success(f"{selected_name} a bien mis à jour son élimination (Classement: {new_classement}, Heure: {current_time})")

# Logout function
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None

# Page selection (authenticated content)
def page_selector():
    # Check if the logged-in user is user1 or another user
    if st.session_state['username'] == "Didier":
        user1_page()  # Show specific content for user1
    elif st.session_state['username'] == "Invités":
        invited_user_page()
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