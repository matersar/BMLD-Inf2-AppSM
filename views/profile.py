import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.title("👤 Mein Profil")

st.write("""
Hier speicherst du deine persönlichen Angaben.  
Diese Daten werden genutzt, um Trainingsplan, Ernährungsempfehlungen und Auswertungen besser an dein Ziel anzupassen.
""")

data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Informatik_2_App"
)

PROFILE_COLUMNS = [
    "Name",
    "Alter",
    "Geschlecht",
    "Größe",
    "Gewicht",
    "Ziel",
    "Fitnesslevel",
    "Trainingstage"
]

profile_df = data_manager.load_user_data(
    "profile.csv",
    initial_value=pd.DataFrame(columns=PROFILE_COLUMNS)
)

if not profile_df.empty:
    latest_profile = profile_df.iloc[-1]

    default_name = latest_profile["Name"]
    default_age = int(latest_profile["Alter"])
    default_gender = latest_profile["Geschlecht"]
    default_height = float(latest_profile["Größe"])
    default_weight = float(latest_profile["Gewicht"])
    default_goal = latest_profile["Ziel"]
    default_level = latest_profile["Fitnesslevel"]
    default_trainingdays = int(latest_profile["Trainingstage"])
else:
    default_name = ""
    default_age = 20
    default_gender = "Weiblich"
    default_height = 170.0
    default_weight = 70.0
    default_goal = "Muskelaufbau"
    default_level = "Anfänger"
    default_trainingdays = 3

gender_options = ["Weiblich", "Männlich"]
goal_options = ["Muskelaufbau", "Abnehmen", "Gesünder & fitter werden"]
level_options = ["Anfänger", "Mittelstufe", "Fortgeschritten"]
trainingday_options = [3, 4, 5]

if default_gender not in gender_options:
    default_gender = "Weiblich"

if default_goal not in goal_options:
    default_goal = "Muskelaufbau"

if default_level not in level_options:
    default_level = "Anfänger"

if default_trainingdays not in trainingday_options:
    default_trainingdays = 3

st.divider()

st.subheader("📋 Persönliche Daten eingeben")

with st.form("profile_form"):
    st.markdown("### Basisdaten")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name", value=default_name)

        age = st.number_input(
            "Alter",
            min_value=10,
            max_value=100,
            value=default_age
        )

        gender = st.selectbox(
            "Geschlecht",
            gender_options,
            index=gender_options.index(default_gender)
        )

    with col2:
        height = st.number_input(
            "Größe (cm)",
            min_value=100.0,
            max_value=250.0,
            value=default_height
        )

        weight = st.number_input(
            "Gewicht (kg)",
            min_value=30.0,
            max_value=250.0,
            value=default_weight
        )

    st.markdown("### Ziel & Training")

    col3, col4 = st.columns(2)

    with col3:
        goal = st.selectbox(
            "Ziel",
            goal_options,
            index=goal_options.index(default_goal)
        )

        training_days = st.selectbox(
            "Trainingstage pro Woche",
            trainingday_options,
            index=trainingday_options.index(default_trainingdays)
        )

    with col4:
        level = st.selectbox(
            "Fitnesslevel",
            level_options,
            index=level_options.index(default_level)
        )

        if level == "Anfänger":
            st.info("🏁 Anfänger: 0–1 Training pro Woche")
        elif level == "Mittelstufe":
            st.info("⚡ Mittelstufe: 2–3 Trainings pro Woche")
        else:
            st.info("🔥 Fortgeschritten: 4–6 Trainings pro Woche")

    submitted = st.form_submit_button("💾 Profil speichern")

if submitted:
    new_profile = pd.DataFrame([{
        "Name": name,
        "Alter": age,
        "Geschlecht": gender,
        "Größe": height,
        "Gewicht": weight,
        "Ziel": goal,
        "Fitnesslevel": level,
        "Trainingstage": training_days
    }])

    data_manager.save_user_data(new_profile, "profile.csv")
    st.success("Profil gespeichert! ✅")
    st.rerun()

profile_df = data_manager.load_user_data(
    "profile.csv",
    initial_value=pd.DataFrame(columns=PROFILE_COLUMNS)
)

if not profile_df.empty:
    st.divider()
    st.subheader("📊 Dein aktuelles Profil")

    latest = profile_df.iloc[-1]

    bmi = latest["Gewicht"] / ((latest["Größe"] / 100) ** 2)

    col1, col2, col3 = st.columns(3)

    col1.metric("👤 Name", latest["Name"])
    col2.metric("🎯 Ziel", latest["Ziel"])
    col3.metric("🏋️ Fitnesslevel", latest["Fitnesslevel"])

    col4, col5, col6 = st.columns(3)

    col4.metric("⚖️ Gewicht", f"{latest['Gewicht']} kg")
    col5.metric("📏 Größe", f"{latest['Größe']} cm")
    col6.metric("📅 Trainingstage", f"{latest['Trainingstage']} / Woche")

    st.subheader("🧠 BMI Analyse")

    col7, col8 = st.columns(2)

    with col7:
        st.metric("BMI", f"{bmi:.1f}")

    with col8:
        if bmi < 18.5:
            st.warning("BMI-Bewertung: Untergewicht")
        elif bmi < 25:
            st.success("BMI-Bewertung: Normalgewicht")
        elif bmi < 30:
            st.info("BMI-Bewertung: Übergewicht")
        else:
            st.warning("BMI-Bewertung: starkes Übergewicht")

    st.caption("Der BMI ist nur ein grober Richtwert und ersetzt keine medizinische Beurteilung.")
else:
    st.info("Noch kein Profil gespeichert.")