import streamlit as st
import pandas as pd

# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder="Informatik_2_App"
)

login_manager = LoginManager(data_manager)
login_manager.login_register()

# --- LOAD USER DATA ---
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',
        initial_value=pd.DataFrame(columns=[
            "timestamp",
            "meal_name",
            "portion_g",
            "calories",
            "protein",
            "carbs",
            "fat"
        ]),
        parse_dates=['timestamp']
    )

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

# TRAININGSPLAN
pg_training = st.Page(
    "views/training_plan.py",
    title="Trainingsplan",
    icon=":material/fitness_center:"
)

# PROFIL
pg_profile = st.Page(
    "views/profile.py",
    title="Mein Profil",
    icon=":material/person:"
)

# ANALYSE
pg_analysis = st.Page(
    "views/analysis.py",
    title="Analyse",
    icon=":material/analytics:"
)

# HELP
pg_help = st.Page(
    "views/help.py",
    title="Help",
    icon=":material/help:"
)

# Navigation
pg = st.navigation([
    pg_home,
    pg_profile,
    pg_nutrition,
    pg_training,
    pg_analysis,
    pg_help
])

pg.run()