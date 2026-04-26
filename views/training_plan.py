import streamlit as st
from utils.exercise_data import EXERCISES

st.title("🏋️ Trainingsplan")

ziel = st.selectbox(
    "Was ist dein Ziel?",
    ["Muskelaufbau", "Abnehmen", "Fitness verbessern"]
)

level = st.selectbox(
    "Was ist dein Fitnesslevel?",
    ["Anfänger", "Fortgeschritten"]
)

st.subheader("Dein Trainingsplan")

# Trainingsplan je nach Ziel
if ziel == "Muskelaufbau":
    st.write("Fokus: Krafttraining und Muskelaufbau")

    trainingsplan = {
        "Montag: Rücken & Arme": ["Rücken", "Arme"],
        "Dienstag: Pause": [],
        "Mittwoch: Beine & Po": ["Beine", "Po"],
        "Donnerstag: Pause": [],
        "Freitag: Bauch & Ganzkörper": ["Bauch", "Beine", "Rücken"],
        "Samstag: Optional Cardio": [],
        "Sonntag: Pause": []
    }

elif ziel == "Abnehmen":
    st.write("Fokus: Ganzkörpertraining und Kalorienverbrauch")

    trainingsplan = {
        "Montag: Beine & Bauch": ["Beine", "Bauch"],
        "Dienstag: Cardio": [],
        "Mittwoch: Rücken & Po": ["Rücken", "Po"],
        "Donnerstag: Pause": [],
        "Freitag: Ganzkörper": ["Beine", "Rücken", "Bauch", "Po"],
        "Samstag: Cardio": [],
        "Sonntag: Pause": []
    }

else:
    st.write("Fokus: allgemeine Fitness")

    trainingsplan = {
        "Montag: Oberkörper": ["Rücken", "Arme"],
        "Dienstag: Pause": [],
        "Mittwoch: Unterkörper": ["Beine", "Po"],
        "Donnerstag: Mobility": [],
        "Freitag: Core": ["Bauch", "Beine"],
        "Samstag: Optional Bewegung": [],
        "Sonntag: Pause": []
    }

# Anzeige
for tag, muskelgruppen in trainingsplan.items():
    st.markdown(f"### {tag}")

    if not muskelgruppen:
        st.write("Ruhetag / Erholung")
        continue

    passende_uebungen = [
        ex for ex in EXERCISES
        if ex["muskelgruppe"] in muskelgruppen and ex["level"] == level
    ]

    for ex in passende_uebungen[:5]:
        st.markdown(
            f"- **{ex['name']}** ({ex['muskelgruppe']}) – "
            f"{ex['saetze']} Sätze x {ex['wiederholungen']}"
        )