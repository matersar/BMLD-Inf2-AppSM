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

profile_df = data_manager.load_user_data("profile.csv", initial_value=pd.DataFrame())
nutrition_df = data_manager.load_user_data("data.csv", initial_value=pd.DataFrame())

try:
    progress_df = progress_manager.load_progress()
except Exception:
    progress_df = pd.DataFrame(columns=[
        "timestamp", "goal", "level", "training_days", "day_name", "completed"
    ])

# =========================
# START / HERO
# =========================

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

else:
    name = ""
    ziel = "Noch kein Ziel"
    level = "Noch kein Level"
    trainingstage = 0
    gewicht = 0
    groesse = 0
    bmi = None

    st.info("Willkommen bei FitPlan! Fülle zuerst dein Profil aus, damit deine App personalisiert wird.")

st.markdown("""
### Dein persönlicher Fitness-Überblick 💪

Willkommen bei **FitPlan** – deiner persönlichen Fitness- und Ernährungs-App.  
Die App unterstützt dich dabei, deine Ziele Schritt für Schritt strukturierter, motivierter und übersichtlicher zu erreichen.

Mit FitPlan kannst du:

✅ dein persönliches Fitnessprofil erstellen  
✅ individuelle Trainingspläne nutzen  
✅ deine Mahlzeiten und Makros speichern  
✅ deinen Fortschritt analysieren  
✅ Motivation durch Badges und Streaks erhalten  
✅ deine Entwicklung langfristig verfolgen  

Egal ob dein Ziel **Muskelaufbau**, **Abnehmen** oder einfach ein gesünderer Lebensstil ist –  
FitPlan hilft dir dabei, deine Gewohnheiten sichtbar zu machen und konsequent dranzubleiben.

Durch die Kombination aus **Training**, **Ernährung**, **Analyse** und **Fortschrittskontrolle** bekommst du einen klaren Überblick darüber:

🔥 wie regelmäßig du trainierst  
🥗 ob deine Ernährung zu deinem Ziel passt  
📈 wie sich dein Fortschritt entwickelt  
🏅 welche Erfolge du bereits erreicht hast  

Kleine Schritte führen langfristig zu großen Ergebnissen.  
Bleib konsequent, sammle Fortschritte und arbeite jeden Tag an der besten Version von dir selbst 🚀
""")

st.divider()

# =========================
# TOP KPI ÜBERSICHT
# =========================

erledigt_df = pd.DataFrame()
erledigte_trainings = 0
alle_eintraege = 0
badge = "Noch kein Badge"

if not progress_df.empty and "completed" in progress_df.columns:
    erledigt_df = progress_df[progress_df["completed"] == True].copy()
    erledigte_trainings = len(erledigt_df)
    alle_eintraege = len(progress_df)

    if erledigte_trainings == 0:
        badge = "Noch kein Badge"
    elif erledigte_trainings < 5:
        badge = "🏁 Starter"
    elif erledigte_trainings < 15:
        badge = "🔥 Dranbleiber"
    else:
        badge = "💪 Trainingsmaschine"

meals_count = 0
avg_kcal = 0
avg_protein = 0

if not nutrition_df.empty and "Kalorien" in nutrition_df.columns:
    meals_count = len(nutrition_df)
    avg_kcal = nutrition_df["Kalorien"].mean()
    avg_protein = nutrition_df["Protein"].mean()

st.subheader("📌 Schnellübersicht")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎯 Ziel", ziel)
col2.metric("✅ Trainings", erledigte_trainings)
col3.metric("🍽️ Mahlzeiten", meals_count)
col4.metric("🏅 Badge", badge)

st.divider()

# =========================
# PROFIL
# =========================

st.subheader("👤 Profil")

if not profile_df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("🏋️ Fitnesslevel", level)
    col2.metric("📅 Trainingsplan", f"{trainingstage} Tage/Woche")
    col3.metric("🧠 BMI", f"{bmi:.1f}")

    col4, col5 = st.columns(2)
    col4.metric("⚖️ Gewicht", f"{gewicht} kg")
    col5.metric("📏 Größe", f"{groesse} cm")

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

st.subheader("🏋️ Training")

if not progress_df.empty and "completed" in progress_df.columns:
    if erledigte_trainings < 5:
        user_level = "Anfänger"
    elif erledigte_trainings < 15:
        user_level = "Mittelstufe"
    else:
        user_level = "Fortgeschritten"

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Erledigte Trainings", erledigte_trainings)
    col2.metric("📌 Gespeicherte Einträge", alle_eintraege)
    col3.metric("📈 Trainings-Level", user_level)

    if not erledigt_df.empty and "timestamp" in erledigt_df.columns:
        erledigt_df["timestamp"] = pd.to_datetime(erledigt_df["timestamp"], errors="coerce")
        erledigt_df = erledigt_df.dropna(subset=["timestamp"])
        erledigt_df = erledigt_df.sort_values("timestamp")
        erledigt_df["Training Nr."] = range(1, len(erledigt_df) + 1)

        line_data = erledigt_df[["Training Nr."]].copy()
        line_data["Erledigte Trainings"] = range(1, len(erledigt_df) + 1)

        if len(line_data) >= 2:
            st.subheader("📈 Trainingsentwicklung")
            st.line_chart(line_data, x="Training Nr.", y="Erledigte Trainings")
            st.caption("Die X-Achse nummeriert deine gespeicherten erledigten Trainings.")
        else:
            st.info("Für eine sichtbare Trainingslinie brauchst du mindestens 2 erledigte Trainings.")

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

        letzte_trainings["Datum"] = pd.to_datetime(
            letzte_trainings["Datum"],
            errors="coerce"
        ).dt.strftime("%d.%m.%Y %H:%M")

        letzte_trainings["Erledigt"] = letzte_trainings["Erledigt"].map({True: "Ja", False: "Nein"})

        spalten = ["Datum", "Ziel", "Fitnesslevel", "Trainingstage", "Trainingstag", "Erledigt"]
        letzte_trainings = letzte_trainings[[col for col in spalten if col in letzte_trainings.columns]]

        st.dataframe(letzte_trainings, use_container_width=True)
else:
    st.info("Noch keine Trainingsfortschritte gespeichert.")

st.divider()

# =========================
# ERNÄHRUNG
# =========================

st.subheader("🥗 Ernährung")

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

        if len(nutrition_chart) >= 2:
            st.subheader("📈 Kalorienverlauf")
            st.line_chart(nutrition_chart, x="Mahlzeit Nr.", y="Kalorien")
            st.caption("Die X-Achse nummeriert deine gespeicherten Mahlzeiten.")
        else:
            st.info("Für eine sichtbare Kalorienlinie brauchst du mindestens 2 gespeicherte Mahlzeiten.")
else:
    st.info("Noch keine Mahlzeiten gespeichert.")

st.divider()

# =========================
# MOTIVATION
# =========================

st.subheader("🔥 Motivation")

if not profile_df.empty:
    if erledigte_trainings > 0 and meals_count > 0:
        st.success(
            "Stark! Du nutzt bereits Training und Ernährung zusammen. "
            "Bleib konsequent – kleine Schritte führen langfristig zu großen Ergebnissen 💪"
        )
    elif erledigte_trainings > 0:
        st.info("Du hast Trainingsfortschritte gespeichert. Ergänze jetzt noch deine Ernährung für eine bessere Analyse.")
    elif meals_count > 0:
        st.info("Du hast Mahlzeiten gespeichert. Speichere jetzt auch Trainingsfortschritte, um deine Entwicklung besser zu sehen.")
    else:
        st.warning("Starte mit einer Mahlzeit oder einem Training. Heute ist ein guter Anfang!")
else:
    st.info("Fülle zuerst dein Profil aus, damit dein Dashboard personalisiert wird.")