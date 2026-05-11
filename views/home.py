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
# DATEN VORBEREITEN
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
else:
    name = ""
    ziel = "Noch kein Ziel"
    level = "Noch kein Level"
    trainingstage = 0
    gewicht = 0
    groesse = 0
    bmi = None

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
total_kcal = 0
avg_kcal = 0
avg_protein = 0

if not nutrition_df.empty and "Kalorien" in nutrition_df.columns:
    meals_count = len(nutrition_df)
    total_kcal = nutrition_df["Kalorien"].sum()
    avg_kcal = nutrition_df["Kalorien"].mean()
    avg_protein = nutrition_df["Protein"].mean()

# =========================
# HERO
# =========================

if not profile_df.empty:
    st.success(f"Hallo **{name}** 👋 Schön, dass du wieder da bist!")
else:
    st.info("Willkommen bei FitPlan! Fülle zuerst dein Profil aus, damit deine App personalisiert wird.")

st.markdown("""
## Dein persönlicher Fitness- und Ernährungsbegleiter 💪

**FitPlan** hilft dir dabei, Training, Ernährung und Fortschritt an einem Ort zu verbinden.  
Die App ist dafür gedacht, deine Ziele sichtbarer, strukturierter und motivierender zu machen.

Mit FitPlan kannst du deine Mahlzeiten speichern, passende Trainingspläne nutzen, deinen Fortschritt verfolgen und erkennen, ob deine Ernährung zu deinem Ziel passt.

### Was du mit FitPlan erreichen kannst

- mehr Überblick über deine Ernährung
- mehr Struktur im Training
- bessere Einschätzung deiner Fortschritte
- mehr Motivation durch Badges und Streaks
- bessere Verbindung zwischen Ernährung und Trainingsziel

Egal ob du **Muskeln aufbauen**, **abnehmen** oder einfach **gesünder und fitter werden** möchtest:  
FitPlan unterstützt dich dabei, kleine Schritte regelmässig umzusetzen und langfristig dranzubleiben.
""")

st.divider()

# =========================
# FEATURE ÜBERSICHT
# =========================

st.subheader("✨ Was bietet FitPlan?")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.info("""
    **👤 Profil**
    
    Speichere dein Ziel, Fitnesslevel, Gewicht und Trainingstage.
    
    Diese Angaben werden für Trainings- und Ernährungsempfehlungen verwendet.
    """)

with col_f2:
    st.info("""
    **🥗 Ernährung**
    
    Berechne Kalorien, Protein und weitere Nährwerte deiner Mahlzeiten.
    
    So erkennst du, ob deine Ernährung zu deinem Ziel passt.
    """)

with col_f3:
    st.info("""
    **🏋️ Training**
    
    Nutze einen Trainingsplan passend zu Ziel und Fitnesslevel.
    
    Fortschritte können gespeichert und ausgewertet werden.
    """)

col_f4, col_f5 = st.columns(2)

with col_f4:
    st.info("""
    **📊 Analyse**
    
    Die App wertet deine gespeicherten Daten aus.
    
    Diagramme, Zielwerte und Empfehlungen machen deine Entwicklung sichtbar.
    """)

with col_f5:
    st.info("""
    **🔥 Motivation**
    
    Badges, Streaks und Fortschrittsanzeigen helfen dir, konsequent zu bleiben.
    
    Jeder gespeicherte Fortschritt zählt.
    """)

st.divider()

# =========================
# SCHNELLÜBERSICHT
# =========================

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

st.subheader("👤 Profilübersicht")

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

st.subheader("🏋️ Trainingsübersicht")

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

st.subheader("🥗 Ernährungsübersicht")

if not nutrition_df.empty and "Kalorien" in nutrition_df.columns:
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
            "Deine gespeicherten Daten helfen dir, deine Entwicklung besser zu verstehen. "
            "Bleib konsequent – kleine Schritte führen langfristig zu grossen Ergebnissen 💪"
        )
    elif erledigte_trainings > 0:
        st.info(
            "Du hast bereits Trainingsfortschritte gespeichert. "
            "Ergänze jetzt noch deine Ernährung, damit die App deine Entwicklung noch besser analysieren kann."
        )
    elif meals_count > 0:
        st.info(
            "Du hast bereits Mahlzeiten gespeichert. "
            "Speichere jetzt auch Trainingsfortschritte, um Ernährung und Training gemeinsam auszuwerten."
        )
    else:
        st.warning(
            "Starte mit einer Mahlzeit oder einem Training. "
            "Jeder gespeicherte Eintrag ist ein Schritt in Richtung deines Ziels."
        )
else:
    st.info("Fülle zuerst dein Profil aus, damit dein Dashboard personalisiert wird.")