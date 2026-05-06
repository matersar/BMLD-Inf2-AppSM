import streamlit as st
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

if ziel == "Muskelaufbau":
    st.write("Fokus: Krafttraining und Muskelaufbau")

    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Rücken & Arme": ["Rücken", "Arme"],
            "Dienstag: Pause": [],
            "Mittwoch: Beine & Po": ["Beine", "Po"],
            "Donnerstag: Pause": [],
            "Freitag: Bauch & Ganzkörper": ["Bauch", "Beine", "Rücken"],
            "Samstag: Optional Cardio": [],
            "Sonntag: Pause": []
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine & Po": ["Beine", "Po"],
            "Mittwoch: Pause": [],
            "Donnerstag: Arme & Bauch": ["Arme", "Bauch"],
            "Freitag: Pause": [],
            "Samstag: Ganzkörper": ["Beine", "Rücken", "Po"],
            "Sonntag: Pause": []
        }
    else:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine": ["Beine"],
            "Mittwoch: Arme & Bauch": ["Arme", "Bauch"],
            "Donnerstag: Po": ["Po"],
            "Freitag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Samstag: Pause": [],
            "Sonntag: Pause": []
        }

elif ziel == "Abnehmen":
    st.write("Fokus: Ganzkörpertraining und Kalorienverbrauch")

    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Beine & Bauch": ["Beine", "Bauch"],
            "Dienstag: Cardio": [],
            "Mittwoch: Rücken & Po": ["Rücken", "Po"],
            "Donnerstag: Pause": [],
            "Freitag: Ganzkörper": ["Beine", "Rücken", "Bauch", "Po"],
            "Samstag: Cardio": [],
            "Sonntag: Pause": []
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Dienstag: Cardio": [],
            "Mittwoch: Beine & Po": ["Beine", "Po"],
            "Donnerstag: Pause": [],
            "Freitag: Bauch & Rücken": ["Bauch", "Rücken"],
            "Samstag: Ganzkörper": ["Beine", "Po", "Bauch"],
            "Sonntag: Pause": []
        }
    else:
        trainingsplan = {
            "Montag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Dienstag: Beine & Po": ["Beine", "Po"],
            "Mittwoch: Cardio": [],
            "Donnerstag: Rücken & Bauch": ["Rücken", "Bauch"],
            "Freitag: Ganzkörper": ["Beine", "Po", "Arme"],
            "Samstag: Optional Cardio": [],
            "Sonntag: Pause": []
        }

else:
    st.write("Fokus: allgemeine Fitness")

    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Oberkörper": ["Rücken", "Arme"],
            "Dienstag: Pause": [],
            "Mittwoch: Unterkörper": ["Beine", "Po"],
            "Donnerstag: Mobility": [],
            "Freitag: Core": ["Bauch", "Beine"],
            "Samstag: Optional Bewegung": [],
            "Sonntag: Pause": []
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Oberkörper": ["Rücken", "Arme"],
            "Dienstag: Unterkörper": ["Beine", "Po"],
            "Mittwoch: Pause": [],
            "Donnerstag: Core": ["Bauch"],
            "Freitag: Pause": [],
            "Samstag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Sonntag: Pause": []
        }
    else:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine": ["Beine"],
            "Mittwoch: Bauch": ["Bauch"],
            "Donnerstag: Arme": ["Arme"],
            "Freitag: Po & Ganzkörper": ["Po", "Beine", "Rücken"],
            "Samstag: Pause": [],
            "Sonntag: Pause": []
        }

trainingstage = {
    tag: muskelgruppen
    for tag, muskelgruppen in trainingsplan.items()
    if muskelgruppen
}

erledigt_count = 0

st.subheader("Fortschritt diese Woche")

for tag in trainingstage:
    gespeicherter_status = progress_manager.get_latest_status(
        ziel,
        level,
        trainingstage_anzahl,
        tag
    )

    erledigt = st.checkbox(
        f"{tag} erledigt",
        value=gespeicherter_status,
        key=f"{ziel}_{level}_{trainingstage_anzahl}_{tag}"
    )

    if erledigt != gespeicherter_status:
        progress_manager.update_day(
            ziel,
            level,
            trainingstage_anzahl,
            tag,
            erledigt
        )

    if erledigt:
        erledigt_count += 1

gesamt = len(trainingstage)

st.progress(erledigt_count / gesamt)
st.write(f"Du hast **{erledigt_count} von {gesamt} Trainingstagen** geschafft.")

st.divider()

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