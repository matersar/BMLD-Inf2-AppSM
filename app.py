import streamlit as st

# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="BMLD_App_DB"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in
# --- END OF NEW CODE ---

# --- CODE UPDATE: load user data from data manager if not already present in session state --
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---

st.set_page_config(
    page_title="Meine App",
    page_icon=":material/home:"
)

# HOME PAGE
pg_home = st.Page(
    "views/home.py",
    title="Home",
    icon=":material/home:"
)

# NÄHRWERT RECHNER
pg_nutrition = st.Page(
    "views/nutrition_calculator.py",
    title="Nährwert Rechner",
    icon=":material/restaurant:"
)

# Navigation
pg = st.navigation([
    pg_home,
    pg_nutrition
])

pg.run()
