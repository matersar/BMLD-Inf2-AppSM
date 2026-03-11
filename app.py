import streamlit as st

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
