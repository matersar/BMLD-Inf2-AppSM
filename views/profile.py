import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.title("👤 Mein Profil")

data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Informatik_2_App"
)

# Profil laden
profile_df = data_manager.load_user_data(
    "profile.csv",
    initial_value=pd.DataFrame(columns=[
        "Name",
        "Alter",
        "Geschlecht",
        "Größe",
        "Gewicht",
        "Ziel",
        "Fitnesslevel",
        "Trainingstage"
    ])
)

# Falls schon Daten vorhanden → vorausfüllen
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

st.subheader("📋 Persönliche Daten")

with st.form("profile_form"):

    name = st.text_input("Name", value=default_name)

    age = st.number_input(
        "Alter",
        min_value=10,
        max_value=100,
        value=default_age
    )

    gender = st.selectbox(
        "Geschlecht",
        ["Weiblich", "Männlich", "Divers"],
        index=["Weiblich", "Männlich", "Divers"].index(default_gender)
    )

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

    goal = st.selectbox(
        "Ziel",
        ["Muskelaufbau", "Abnehmen", "Fitness verbessern"],
        index=["Muskelaufbau", "Abnehmen", "Fitness verbessern"].index(default_goal)
    )

    level = st.selectbox(
        "Fitnesslevel",
        ["Anfänger", "Fortgeschritten"],
        index=["Anfänger", "Fortgeschritten"].index(default_level)
    )

    training_days = st.selectbox(
        "Trainingstage pro Woche",
        [3, 4, 5],
        index=[3, 4, 5].index(default_trainingdays)
    )

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

# Profil anzeigen
if not profile_df.empty:

    st.divider()

    st.subheader("📊 Dein aktuelles Profil")

    latest = profile_df.iloc[-1]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("👤 Name", latest["Name"])
        st.metric("🎂 Alter", f"{latest['Alter']} Jahre")
        st.metric("⚖️ Gewicht", f"{latest['Gewicht']} kg")

    with col2:
        st.metric("📏 Größe", f"{latest['Größe']} cm")
        st.metric("🎯 Ziel", latest["Ziel"])
        st.metric("🏋️ Fitnesslevel", latest["Fitnesslevel"])

    bmi = latest["Gewicht"] / ((latest["Größe"] / 100) ** 2)

    st.subheader("🧠 BMI Analyse")

    st.metric("BMI", f"{bmi:.1f}")

    if bmi < 18.5:
        st.warning("Untergewicht")
    elif bmi < 25:
        st.success("Normalgewicht")
    elif bmi < 30:
        st.info("Übergewicht")
    else:
        st.warning("Starkes Übergewicht")