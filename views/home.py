 import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.progress_manager import ProgressManager

st.title("🏠 FitPlan Dashboard")

data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Informatik_2_App"
)

progress_manager = ProgressManager()

st.write("Willkommen zurück! Hier siehst du deine wichtigsten Fitness- und Ernährungsdaten auf einen Blick.")

# Profil laden
profile_df = data_manager.load_user_data(
    "profile.csv",
    initial_value=pd.DataFrame()
)

# Ernährung laden
nutrition_df = data_manager.load_user_data(
    "data.csv",
    initial_value=pd.DataFrame()
)

# Fortschritt laden
try:
    progress_df = progress_manager.load_progress()
except Exception:
    progress_df = pd.DataFrame(columns=[
        "timestamp", "goal", "level", "training_days", "day_name", "completed"
    ])

st.divider()

# Profilübersicht
st.subheader("👤 Profilübersicht")

if not profile_df.empty:
    profile = profile_df.iloc[-1]

    name = profile["Name"]
    ziel = profile["Ziel"]
    level = profile["Fitnesslevel"]
    trainingstage = profile["Trainingstage"]
    gewicht = profile["Gewicht"]
    groesse = profile["Größe"]

    bmi = gewicht / ((groesse / 100) ** 2)

    col1, col2, col3 = st.columns(3)

    col1.metric("🎯 Ziel", ziel)
    col2.metric("🏋️ Level", level)
    col3.metric("📅 Trainingstage", f"{trainingstage}/Woche")

    col4, col5 = st.columns(2)
    col4.metric("⚖️ Gewicht", f"{gewicht} kg")
    col5.metric("🧠 BMI", f"{bmi:.1f}")

    if bmi < 18.5:
        st.warning("BMI-Bewertung: Untergewicht")
    elif bmi < 25:
        st.success("BMI-Bewertung: Normalgewicht")
    elif bmi < 30:
        st.info("BMI-Bewertung: Übergewicht")
    else:
        st.warning("BMI-Bewertung: starkes Übergewicht")

else:
    st.info("Noch kein Profil gespeichert. Bitte zuerst unter „Mein Profil“ ausfüllen.")

st.divider()

# Trainingsfortschritt
st.subheader("🏋️ Trainingsfortschritt")

if not progress_df.empty and "completed" in progress_df.columns:
    erledigt_df = progress_df[progress_df["completed"] == True]
    erledigte_trainings = len(erledigt_df)
    alle_eintraege = len(progress_df)

    col1, col2 = st.columns(2)

    col1.metric("✅ Erledigte Trainings", erledigte_trainings)
    col2.metric("📌 Gespeicherte Einträge", alle_eintraege)

    if erledigte_trainings < 5:
        user_level = "Anfänger"
    elif erledigte_trainings < 15:
        user_level = "Mittelstufe"
    else:
        user_level = "Fortgeschritten"

    st.metric("🏅 Trainings-Level", user_level)

    chart_data = (
        erledigt_df.groupby("goal")
        .size()
        .reset_index(name="Erledigte Trainings")
        .rename(columns={"goal": "Ziel"})
    )

    if not chart_data.empty:
        st.subheader("📈 Trainings nach Ziel")
        st.bar_chart(chart_data, x="Ziel", y="Erledigte Trainings")
else:
    st.info("Noch keine Trainingsfortschritte gespeichert.")

st.divider()

# Ernährung
st.subheader("🥗 Ernährungsübersicht")

if not nutrition_df.empty and "Kalorien" in nutrition_df.columns:
    total_kcal = nutrition_df["Kalorien"].sum()
    avg_kcal = nutrition_df["Kalorien"].mean()
    avg_protein = nutrition_df["Protein"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("🔥 Gesamt Kalorien", f"{total_kcal:.0f} kcal")
    col2.metric("📊 Ø Kalorien", f"{avg_kcal:.0f} kcal")
    col3.metric("💪 Ø Protein", f"{avg_protein:.1f} g")

    letzte_mahlzeit = nutrition_df.iloc[-1]

    st.info(
        f"Letzte Mahlzeit: **{letzte_mahlzeit['Name']}** "
        f"mit **{letzte_mahlzeit['Kalorien']:.0f} kcal** "
        f"und **{letzte_mahlzeit['Protein']:.1f} g Protein**."
    )

else:
    st.info("Noch keine Mahlzeiten gespeichert.")

st.divider()

# Motivation
st.subheader("🔥 Motivation")

if not profile_df.empty:
    if not progress_df.empty and len(progress_df[progress_df["completed"] == True]) > 0:
        st.success("Stark! Du hast bereits Fortschritte gespeichert. Bleib dran 💪")
    else:
        st.warning("Starte dein erstes Training und speichere deinen Fortschritt.")
else:
    st.info("Fülle zuerst dein Profil aus, damit dein Dashboard personalisiert wird.")