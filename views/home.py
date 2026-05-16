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

# PROFIL LADEN
profile_df = data_manager.load_user_data(
    "profile.csv",
    initial_value=pd.DataFrame()
)

# WICHTIG: NICHT erneut über WebDAV laden
# Stattdessen die bereits geladenen Daten aus session_state verwenden
nutrition_df = st.session_state.get("data_df", pd.DataFrame())

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
avg_kcal = 0
avg_protein = 0
avg_fett = 0

if not nutrition_df.empty:
    kcal_col = None
    protein_col = None
    fett_col = None

    for col in nutrition_df.columns:
        if col.lower() in ["kalorien", "calories"]:
            kcal_col = col
        if col.lower() == "protein":
            protein_col = col
        if col.lower() in ["fett", "fat"]:
            fett_col = col

    meals_count = len(nutrition_df)

    if kcal_col:
        avg_kcal = nutrition_df[kcal_col].mean()

    if protein_col:
        avg_protein = nutrition_df[protein_col].mean()

    if fett_col:
        avg_fett = nutrition_df[fett_col].mean()

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