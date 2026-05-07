import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.progress_manager import ProgressManager

st.set_page_config(page_title="FitPlan Dashboard", page_icon="🏠")

st.title("🏠 FitPlan Dashboard")

data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Informatik_2_App"
)

progress_manager = ProgressManager()

st.markdown("""
### Willkommen bei **FitPlan** 💪

FitPlan verbindet **Profil, Ernährung, Training und Fortschritt** in einer App.  
Du kannst dein persönliches Ziel festlegen, Mahlzeiten speichern, Trainingspläne nutzen und deine Entwicklung verfolgen.

**Dein Ziel:** kleine Schritte, regelmäßig dranbleiben und langfristig fitter werden. 🔥
""")

profile_df = data_manager.load_user_data("profile.csv", initial_value=pd.DataFrame())
nutrition_df = data_manager.load_user_data("data.csv", initial_value=pd.DataFrame())

try:
    progress_df = progress_manager.load_progress()
except Exception:
    progress_df = pd.DataFrame(columns=[
        "timestamp", "goal", "level", "training_days", "day_name", "completed"
    ])

st.divider()

# =========================
# PROFIL
# =========================

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

    st.success(f"Hallo **{name}** 👋 Schön, dass du wieder da bist!")

    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 Ziel", ziel)
    col2.metric("🏋️ Fitnesslevel", level)
    col3.metric("📅 Trainingsplan", f"{trainingstage} Tage/Woche")

    col4, col5, col6 = st.columns(3)
    col4.metric("⚖️ Gewicht", f"{gewicht} kg")
    col5.metric("📏 Größe", f"{groesse} cm")
    col6.metric("🧠 BMI", f"{bmi:.1f}")

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

# =========================
# TRAINING
# =========================

st.subheader("🏋️ Trainingsfortschritt")

if not progress_df.empty and "completed" in progress_df.columns:
    erledigt_df = progress_df[progress_df["completed"] == True].copy()
    erledigte_trainings = len(erledigt_df)
    alle_eintraege = len(progress_df)

    if erledigte_trainings < 5:
        user_level = "Anfänger"
        badge = "🏁 Starter"
    elif erledigte_trainings < 15:
        user_level = "Mittelstufe"
        badge = "🔥 Dranbleiber"
    else:
        user_level = "Fortgeschritten"
        badge = "💪 Trainingsmaschine"

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Erledigte Trainings", erledigte_trainings)
    col2.metric("📌 Gespeicherte Einträge", alle_eintraege)
    col3.metric("🏅 Badge", badge)

    st.metric("📈 Trainings-Level", user_level)

    if not erledigt_df.empty and "timestamp" in erledigt_df.columns:
        erledigt_df["timestamp"] = pd.to_datetime(erledigt_df["timestamp"], errors="coerce")
        erledigt_df = erledigt_df.dropna(subset=["timestamp"])
        erledigt_df = erledigt_df.sort_values("timestamp")
        erledigt_df["Training Nr."] = range(1, len(erledigt_df) + 1)

        line_data = erledigt_df[["Training Nr."]].copy()
        line_data["Erledigte Trainings"] = range(1, len(erledigt_df) + 1)

        st.subheader("📈 Trainingsentwicklung")
        st.line_chart(line_data, x="Training Nr.", y="Erledigte Trainings")
        st.caption("Die X-Achse nummeriert deine gespeicherten erledigten Trainings.")

    if not erledigt_df.empty:
        st.subheader("📋 Letzte Trainingseinträge")

        letzte_trainings = erledigt_df.tail(5).copy()
        letzte_trainings = letzte_trainings.rename(columns={
            "timestamp": "Datum",
            "goal": "Ziel",
            "level": "Fitnesslevel",
            "training_days": "Trainingstage",
            "day_name": "Trainingstag",
            "completed": "Erledigt"
        })

        letzte_trainings["Erledigt"] = letzte_trainings["Erledigt"].map({True: "Ja", False: "Nein"})

        st.dataframe(letzte_trainings, use_container_width=True)
else:
    st.info("Noch keine Trainingsfortschritte gespeichert.")

st.divider()

# =========================
# ERNÄHRUNG
# =========================

st.subheader("🥗 Ernährungsübersicht")

if not nutrition_df.empty and "Kalorien" in nutrition_df.columns:
    total_kcal = nutrition_df["Kalorien"].sum()
    avg_kcal = nutrition_df["Kalorien"].mean()
    avg_protein = nutrition_df["Protein"].mean()
    meals_count = len(nutrition_df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🍽️ Mahlzeiten", meals_count)
    col2.metric("🔥 Gesamt Kalorien", f"{total_kcal:.0f} kcal")
    col3.metric("📊 Ø Kalorien", f"{avg_kcal:.0f} kcal")
    col4.metric("💪 Ø Protein", f"{avg_protein:.1f} g")

    letzte_mahlzeit = nutrition_df.iloc[-1]

    st.info(
        f"Letzte Mahlzeit: **{letzte_mahlzeit['Name']}** "
        f"mit **{letzte_mahlzeit['Kalorien']:.0f} kcal** "
        f"und **{letzte_mahlzeit['Protein']:.1f} g Protein**."
    )

    if "timestamp" in nutrition_df.columns:
        nutrition_chart = nutrition_df.copy()
        nutrition_chart["timestamp"] = pd.to_datetime(nutrition_chart["timestamp"], errors="coerce")
        nutrition_chart = nutrition_chart.dropna(subset=["timestamp"])
        nutrition_chart = nutrition_chart.sort_values("timestamp")
        nutrition_chart["Mahlzeit Nr."] = range(1, len(nutrition_chart) + 1)

        st.subheader("📈 Kalorienverlauf")
        st.line_chart(nutrition_chart, x="Mahlzeit Nr.", y="Kalorien")
        st.caption("Die X-Achse nummeriert deine gespeicherten Mahlzeiten.")
else:
    st.info("Noch keine Mahlzeiten gespeichert.")

st.divider()

# =========================
# MOTIVATION
# =========================

st.subheader("🔥 Motivation")

if not profile_df.empty:
    if not progress_df.empty and len(progress_df[progress_df["completed"] == True]) > 0:
        st.success(
            "Stark! Du hast bereits Fortschritte gespeichert. "
            "Bleib konsequent – kleine Schritte führen langfristig zu großen Ergebnissen 💪"
        )
    else:
        st.warning("Starte dein erstes Training und speichere deinen Fortschritt. Heute ist ein guter Anfang!")
else:
    st.info("Fülle zuerst dein Profil aus, damit dein Dashboard personalisiert wird.")