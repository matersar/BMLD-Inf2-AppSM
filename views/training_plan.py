import streamlit as st
import pandas as pd
from utils.exercise_data import EXERCISES
from utils.progress_manager import ProgressManager
from utils.data_manager import DataManager

st.title("🏋️ Trainingsplan")

progress_manager = ProgressManager()
data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Informatik_2_App"
)

ziel = st.selectbox("Was ist dein Ziel?", ["Muskelaufbau", "Abnehmen", "Fitness verbessern"])
level = st.selectbox("Was ist dein Fitnesslevel?", ["Anfänger", "Fortgeschritten"])
trainingstage_anzahl = st.selectbox("Wie viele Trainingstage pro Woche möchtest du?", [3, 4, 5])

st.subheader("Dein Trainingsplan")

if ziel == "Muskelaufbau":
    fokus_text = "Fokus: Krafttraining und Muskelaufbau"
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
    fokus_text = "Fokus: Ganzkörpertraining und Kalorienverbrauch"
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
    fokus_text = "Fokus: allgemeine Fitness"
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

st.write(fokus_text)

if "checkbox_states" not in st.session_state:
    st.session_state["checkbox_states"] = {}

st.subheader("Fortschritt diese Woche")

current_keys = []

for tag in trainingsplan:
    key = f"{ziel}_{level}_{trainingstage_anzahl}_{tag}"
    current_keys.append(key)

    if key not in st.session_state["checkbox_states"]:
        st.session_state["checkbox_states"][key] = False

    st.session_state["checkbox_states"][key] = st.checkbox(
        f"{tag} erledigt",
        value=st.session_state["checkbox_states"][key],
        key=key
    )

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

erledigt_count = sum(1 for key in current_keys if st.session_state["checkbox_states"][key])
gesamt = len(trainingsplan)
prozent = round((erledigt_count / gesamt) * 100)

st.progress(erledigt_count / gesamt)
st.write(f"Du hast **{erledigt_count} von {gesamt} Trainingstagen** geschafft.")
st.metric("📈 Wochenfortschritt", f"{prozent}%")

st.divider()

st.subheader("🥗 Ernährung & Training Analyse")

nutrition_df = data_manager.load_user_data("data.csv", initial_value=pd.DataFrame())

if not nutrition_df.empty and "Protein" in nutrition_df.columns:

    avg_protein = nutrition_df["Protein"].mean()
    avg_calories = nutrition_df["Kalorien"].mean()

    st.subheader("📊 Deine durchschnittliche Ernährung")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💪 Ø Protein pro Mahlzeit",
            f"{avg_protein:.1f} g",
            "gut für Muskelaufbau" if avg_protein >= 25 else "könnte höher sein"
        )

    with col2:
        st.metric(
            "🔥 Ø Kalorien pro Mahlzeit",
            f"{avg_calories:.0f} kcal",
            "im Zielbereich" if 400 <= avg_calories <= 800 else "abweichend"
        )

    protein_score = min(avg_protein / 30, 1.0) * 100

    if ziel == "Muskelaufbau":
        calorie_score = min(avg_calories / 650, 1.0) * 100
    elif ziel == "Abnehmen":
        calorie_score = max(0, min((800 - avg_calories) / 400, 1.0)) * 100
    else:
        calorie_score = max(0, 100 - abs(avg_calories - 600) / 6)

    gesamt_score = round((protein_score + calorie_score) / 2)

    if gesamt_score >= 80:
        label = "Sehr gut"
    elif gesamt_score >= 60:
        label = "Gut"
    else:
        label = "Verbesserbar"

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("💪 Protein-Score", f"{protein_score:.0f}%")
    col_b.metric("🔥 Kalorien-Score", f"{calorie_score:.0f}%")
    col_c.metric("🎯 Gesamtbewertung", f"{gesamt_score}%", label)

    st.progress(gesamt_score / 100)

    st.subheader("🎯 Bewertung passend zu deinem Ziel")

    if gesamt_score >= 80:
        st.success("Sehr gut! Deine Ernährung passt stark zu deinem Trainingsziel 💪")
    elif gesamt_score >= 50:
        st.info("Solide Grundlage. Mit kleinen Anpassungen wird es noch besser.")
    else:
        st.warning("Deine Ernährung passt noch nicht optimal zu deinem Ziel.")

else:
    st.info("Noch keine Ernährungsdaten vorhanden.")