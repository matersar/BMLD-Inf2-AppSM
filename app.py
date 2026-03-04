import streamlit as st

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)

pg_second = st.Page(
    "views/unterseite_a.py",
    title="Unterseite A",
    icon=":material/dashboard:"
)

pg_nutrition = st.Page(
    "views/nutrition_calculator.py",
    title="Nährwert Rechner",
    icon=":material/restaurant:"
)

pg = st.navigation([pg_home, pg_second, pg_nutrition])

pg.run()
