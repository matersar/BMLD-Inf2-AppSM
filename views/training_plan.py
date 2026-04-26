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

if ziel == "Muskelaufbau":
    st.write("Fokus: Krafttraining und Muskelaufbau")
    trainingsplan = {
        "Tag 1: Rücken & Arme": ["Rücken", "Arme"],
        "Tag 2: Beine & Po": ["Beine", "Po"],
        "Tag 3: Bauch & Ganzkörper": ["Bauch", "Beine", "Rücken"]
    }

elif ziel == "Abnehmen":
    st.write("Fokus: Ganzkörpertraining und hoher Kalorienverbrauch")
    trainingsplan = {
        "Tag 1: Beine & Bauch": ["Beine", "Bauch"],
        "Tag 2: Rücken & Po": ["Rücken", "Po"],
        "Tag 3: Ganzkörper": ["Beine", "Rücken", "Bauch", "Po"]
    }

else:
    st.write("Fokus: allgemeine Fitness")
    trainingsplan = {
        "Tag 1: Oberkörper": ["Rücken", "Arme"],
        "Tag 2: Unterkörper": ["Beine", "Po"],
        "Tag 3: Core": ["Bauch", "Beine"]
    }

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