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

if prozent == 100:
    st.success("Stark! Du hast alle geplanten Trainings geschafft 💪")
elif prozent >= 50:
    st.info("Guter Fortschritt! Bleib dran 🔥")
else:
    st.warning("Noch Luft nach oben – starte mit deinem nächsten Training!")

st.divider()

st.subheader("📊 Gespeicherte Trainingsfortschritte")

df = progress_manager.load_progress()

if not df.empty:
    df_display = df.rename(columns={
        "timestamp": "Datum",
        "goal": "Ziel",
        "level": "Fitnesslevel",
        "training_days": "Trainingstage",
        "day_name": "Trainingstag",
        "completed": "Erledigt"
    })

    df_display["Erledigt"] = df_display["Erledigt"].map({True: "Ja", False: "Nein"})

    st.dataframe(df_display, use_container_width=True)

    erledigt_df = df[df["completed"] == True]
    erledigte_anzahl = len(erledigt_df)

    if erledigte_anzahl < 5:
        user_level = "Anfänger"
    elif erledigte_anzahl < 15:
        user_level = "Fortgeschritten"
    else:
        user_level = "Pro"

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Erledigte Trainings", erledigte_anzahl)
    col2.metric("📌 Alle Einträge", len(df))
    col3.metric("🏅 Dein Level", user_level)

    st.subheader("📈 Fortschritt nach Ziel")

    chart_data = (
        df.groupby(["goal", "completed"])
        .size()
        .reset_index(name="Anzahl")
    )

    chart_data = chart_data[chart_data["completed"] == True]
    chart_data = chart_data.rename(columns={"goal": "Ziel"})

    if not chart_data.empty:
        st.bar_chart(chart_data, x="Ziel", y="Anzahl")
    else:
        st.info("Noch keine erledigten Trainings vorhanden.")

    csv = df_display.to_csv(index=False)

    st.download_button(
        "Trainingsfortschritt als CSV exportieren",
        csv,
        "trainingsfortschritt.csv",
        "text/csv"
    )

    if st.button("🗑 Fortschritt löschen"):
        progress_manager.save_progress(pd.DataFrame(columns=[
            "timestamp",
            "goal",
            "level",
            "training_days",
            "day_name",
            "completed"
        ]))
        st.rerun()

else:
    st.info("Noch keine Daten vorhanden.")

st.divider()

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

st.divider()
st.subheader("🥗 Ernährung & Training Analyse")

nutrition_df = data_manager.load_user_data(
    "data.csv",
    initial_value=pd.DataFrame()
)

if not nutrition_df.empty and "Protein" in nutrition_df.columns and "Kalorien" in nutrition_df.columns:
    avg_protein = nutrition_df["Protein"].mean()
    avg_calories = nutrition_df["Kalorien"].mean()

    st.write(f"Durchschnitt Protein: **{avg_protein:.1f} g**")
    st.write(f"Durchschnitt Kalorien: **{avg_calories:.0f} kcal**")

    protein_score = min(avg_protein / 30, 1.0) * 100

    if ziel == "Muskelaufbau":
        calorie_score = min(avg_calories / 650, 1.0) * 100
    elif ziel == "Abnehmen":
        calorie_score = max(0, min((800 - avg_calories) / 400, 1.0)) * 100
    else:
        calorie_score = max(0, 100 - abs(avg_calories - 600) / 6)

    gesamt_score = round((protein_score + calorie_score) / 2)

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("💪 Protein-Score", f"{protein_score:.0f}%")
    col_b.metric("🔥 Kalorien-Score", f"{calorie_score:.0f}%")
    col_c.metric("🎯 Gesamtbewertung", f"{gesamt_score}%")

    st.progress(gesamt_score / 100)

    st.subheader("🎯 Bewertung passend zu deinem Ziel")

    if gesamt_score >= 80:
        st.success("Sehr gut! Deine Ernährung passt stark zu deinem Trainingsziel 💪")
    elif gesamt_score >= 50:
        st.info("Solide Grundlage. Mit kleinen Anpassungen passt deine Ernährung noch besser.")
    else:
        st.warning("Deine Ernährung passt noch nicht optimal zu deinem Trainingsziel.")

    if ziel == "Muskelaufbau":
        st.write("Empfehlung: Achte auf ausreichend Protein und genug Kalorien für Muskelaufbau.")
    elif ziel == "Abnehmen":
        st.write("Empfehlung: Achte auf moderate Kalorien und genügend Protein, damit du satt bleibst.")
    else:
        st.write("Empfehlung: Achte auf eine ausgewogene Mahlzeit mit Protein, Kohlenhydraten und Fett.")

else:
    st.info("Noch keine Ernährungsdaten vorhanden.")