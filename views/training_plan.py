import streamlit as st
from utils.exercise_data import EXERCISES

st.title("🏋️ Trainingsplan")

st.write("""
Wähle dein Ziel und dein Fitnesslevel aus. 
Die App erstellt dir daraus einen einfachen Trainingsplan.
""")

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
    muskelgruppen = ["Beine", "Po", "Rücken", "Arme", "Bauch"]
    st.write("Fokus: Krafttraining und Muskelaufbau")

elif ziel == "Abnehmen":
    muskelgruppen = ["Beine", "Po", "Bauch", "Rücken"]
    st.write("Fokus: Ganzkörpertraining und hoher Kalorienverbrauch")

else:
    muskelgruppen = ["Beine", "Rücken", "Arme", "Bauch"]
    st.write("Fokus: allgemeine Fitness und regelmäßige Bewegung")

gefilterte_uebungen = [
    exercise for exercise in EXERCISES
    if exercise["muskelgruppe"] in muskelgruppen and exercise["level"] == level
]

for exercise in gefilterte_uebungen[:8]:
    st.markdown(f"- **{exercise['name']}** ({exercise['muskelgruppe']})")