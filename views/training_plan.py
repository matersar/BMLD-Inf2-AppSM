import streamlit as st
import pandas as pd
from utils.exercise_data import EXERCISES
from utils.progress_manager import ProgressManager

st.title("🏋️ Trainingsplan")

progress_manager = ProgressManager()

ziel = st.selectbox(
    "Was ist dein Ziel?",
    ["Muskelaufbau", "Abnehmen", "Fitness verbessern"]
)

level = st.selectbox(
    "Was ist dein Fitnesslevel?",
    ["Anfänger", "Fortgeschritten"]
)

trainingstage_anzahl = st.selectbox(
    "Wie viele Trainingstage pro Woche möchtest du?",
    [3, 4, 5]
)

st.subheader("Dein Trainingsplan")

# Trainingspläne
if ziel == "Muskelaufbau":
    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Rücken & Arme": ["Rücken", "Arme"],
            "Mittwoch: Beine & Po": ["Beine", "Po"],
            "Freitag: Bauch & Ganzkörper": ["Bauch", "Beine", "Rücken"],
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine & Po": ["Beine", "Po"],
            "Donnerstag: Arme & Bauch": ["Arme", "Bauch"],
            "Samstag: Ganzkörper": ["Beine", "Rücken", "Po"],
        }
    else:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine": ["Beine"],
            "Mittwoch: Arme & Bauch": ["Arme", "Bauch"],
            "Donnerstag: Po": ["Po"],
            "Freitag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
        }

elif ziel == "Abnehmen":
    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Beine & Bauch": ["Beine", "Bauch"],
            "Mittwoch: Rücken & Po": ["Rücken", "Po"],
            "Freitag: Ganzkörper": ["Beine", "Rücken", "Bauch", "Po"],
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Mittwoch: Beine & Po": ["Beine", "Po"],
            "Freitag: Bauch & Rücken": ["Bauch", "Rücken"],
            "Samstag: Ganzkörper": ["Beine", "Po", "Bauch"],
        }
    else:
        trainingsplan = {
            "Montag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Dienstag: Beine & Po": ["Beine", "Po"],
            "Donnerstag: Rücken & Bauch": ["Rücken", "Bauch"],
            "Freitag: Ganzkörper": ["Beine", "Po", "Arme"],
        }

else:
    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Oberkörper": ["Rücken", "Arme"],
            "Mittwoch: Unterkörper": ["Beine", "Po"],
            "Freitag: Core": ["Bauch", "Beine"],
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Oberkörper": ["Rücken", "Arme"],
            "Dienstag: Unterkörper": ["Beine", "Po"],
            "Donnerstag: Core": ["Bauch"],
            "Samstag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
        }
    else:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine": ["Beine"],
            "Mittwoch: Bauch": ["Bauch"],
            "Donnerstag: Arme": ["Arme"],
            "Freitag: Ganzkörper": ["Po", "Beine", "Rücken"],
        }

# Session-State für Checkboxen
if "checkbox_states" not in st.session_state:
    st.session_state["checkbox_states"] = {}

st.subheader("Fortschritt diese Woche")

for tag in trainingsplan:
    key = f"{ziel}_{level}_{trainingstage_anzahl}_{tag}"

    if key not in st.session_state["checkbox_states"]:
        st.session_state["checkbox_states"][key] = False

    st.session_state["checkbox_states"][key] = st.checkbox(
        f"{tag} erledigt",
        value=st.session_state["checkbox_states"][key]
    )

# BUTTON zum Speichern
if st.button("💾 Fortschritt speichern"):
    for tag in trainingsplan:
        key = f"{ziel}_{level}_{trainingstage_anzahl}_{tag}"
        erledigt = st.session_state["checkbox_states"][key]

        progress_manager.update_day(
            ziel,
            level,
            trainingstage_anzahl,
            tag,
            erledigt
        )

    st.success("Fortschritt gespeichert! ✅")

# Fortschritt anzeigen
erledigt_count = sum(st.session_state["checkbox_states"].values())
gesamt = len(trainingsplan)

st.progress(erledigt_count / gesamt)
st.write(f"Du hast **{erledigt_count} von {gesamt} Trainingstagen** geschafft.")

# Tabelle anzeigen
st.subheader("📊 Gespeicherte Trainingsfortschritte")

df = progress_manager.load_progress()

if not df.empty:
    df = df.rename(columns={
        "timestamp": "Datum",
        "goal": "Ziel",
        "level": "Fitnesslevel",
        "training_days": "Trainingstage",
        "day_name": "Trainingstag",
        "completed": "Erledigt"
    })

    df["Erledigt"] = df["Erledigt"].map({True: "Ja", False: "Nein"})

    st.dataframe(df, use_container_width=True)

    st.metric("Gespeicherte Trainings", len(df))

    if st.button("🗑 Fortschritt löschen"):
        progress_manager.save_progress(pd.DataFrame())
        st.rerun()

else:
    st.info("Noch keine Daten vorhanden.")

st.divider()

# Trainingsplan anzeigen
st.subheader("📅 Wochenplan")

for tag, muskelgruppen in trainingsplan.items():
    st.markdown(f"### {tag}")

    passende_uebungen = [
        ex for ex in EXERCISES
        if ex["muskelgruppe"] in muskelgruppen and ex["level"] == level
    ]

    for ex in passende_uebungen[:5]:
        st.markdown(
            f"- **{ex['name']}** ({ex['muskelgruppe']}) – "
            f"{ex['saetze']} Sätze x {ex['wiederholungen']}"
        )