import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.progress_manager import ProgressManager

st.title("📊 Analyse")

data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Informatik_2_App"
)

progress_manager = ProgressManager()

st.write("""
Hier werden deine gespeicherten Ernährungs- und Trainingsdaten ausgewertet.
So erkennst du Trends und siehst, ob du deinem Ziel näher kommst.
""")

nutrition_df = data_manager.load_user_data("data.csv", initial_value=pd.DataFrame())

try:
    progress_df = progress_manager.load_progress()
except Exception:
    progress_df = pd.DataFrame(columns=[
        "timestamp", "goal", "level", "training_days", "day_name", "completed"
    ])

st.divider()

st.subheader("🥗 Ernährungsanalyse")

if not nutrition_df.empty and "Kalorien" in nutrition_df.columns:
    df = nutrition_df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df = df.sort_values("timestamp")
    df["Eintrag Nr."] = range(1, len(df) + 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("🍽️ Mahlzeiten", len(df))
    col2.metric("🔥 Ø Kalorien", f"{df['Kalorien'].mean():.0f} kcal")
    col3.metric("💪 Ø Protein", f"{df['Protein'].mean():.1f} g")

    st.subheader("📈 Kalorienverlauf")
    st.line_chart(df, x="Eintrag Nr.", y="Kalorien")

    st.subheader("📈 Proteinverlauf")
    st.line_chart(df, x="Eintrag Nr.", y="Protein")

    st.subheader("🏆 Top-Mahlzeiten")

    top_protein = df.loc[df["Protein"].idxmax()]
    top_calories = df.loc[df["Kalorien"].idxmax()]

    st.info(f"Proteinreichste Mahlzeit: **{top_protein['Name']}** mit **{top_protein['Protein']} g Protein**")
    st.info(f"Kalorienreichste Mahlzeit: **{top_calories['Name']}** mit **{top_calories['Kalorien']} kcal**")
else:
    st.info("Noch keine Ernährungsdaten vorhanden.")

st.divider()

st.subheader("🏋️ Trainingsanalyse")

if not progress_df.empty and "completed" in progress_df.columns:
    df_train = progress_df.copy()
    df_train["timestamp"] = pd.to_datetime(df_train["timestamp"], errors="coerce")
    df_train = df_train.dropna(subset=["timestamp"])
    df_train = df_train.sort_values("timestamp")

    erledigt_df = df_train[df_train["completed"] == True].copy()

    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Alle Einträge", len(df_train))
    col2.metric("✅ Erledigte Trainings", len(erledigt_df))
    col3.metric("❌ Nicht erledigt", len(df_train) - len(erledigt_df))

    if not erledigt_df.empty:
        erledigt_df["Training Nr."] = range(1, len(erledigt_df) + 1)
        erledigt_df["Kumulierte Trainings"] = range(1, len(erledigt_df) + 1)

        st.subheader("📈 Trainingsfortschritt")
        st.line_chart(erledigt_df, x="Training Nr.", y="Kumulierte Trainings")

        st.subheader("🎯 Trainings nach Ziel")

        ziel_chart = (
            erledigt_df.groupby("goal")
            .size()
            .reset_index(name="Anzahl")
            .rename(columns={"goal": "Ziel"})
        )

        st.bar_chart(ziel_chart, x="Ziel", y="Anzahl")

        st.subheader("📋 Letzte Trainings")
        display_df = erledigt_df.tail(5).rename(columns={
            "timestamp": "Datum",
            "goal": "Ziel",
            "level": "Fitnesslevel",
            "training_days": "Trainingstage",
            "day_name": "Trainingstag",
            "completed": "Erledigt"
        })

        display_df["Erledigt"] = display_df["Erledigt"].map({True: "Ja", False: "Nein"})
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("Noch keine erledigten Trainings vorhanden.")
else:
    st.info("Noch keine Trainingsdaten vorhanden.")

st.divider()

st.subheader("🧠 Automatische Auswertung")

if not nutrition_df.empty and not progress_df.empty:
    tips = []

    if "Protein" in nutrition_df.columns:
        avg_protein = nutrition_df["Protein"].mean()
        if avg_protein < 20:
            tips.append("Dein durchschnittliches Protein ist eher niedrig. Mehr proteinreiche Lebensmittel könnten helfen.")
        else:
            tips.append("Deine Proteinwerte sehen gut aus. Das unterstützt Training und Regeneration.")

    if "Kalorien" in nutrition_df.columns:
        avg_kcal = nutrition_df["Kalorien"].mean()
        if avg_kcal < 400:
            tips.append("Deine Mahlzeiten sind durchschnittlich eher kalorienarm.")
        elif avg_kcal > 800:
            tips.append("Deine Mahlzeiten sind durchschnittlich eher kalorienreich.")
        else:
            tips.append("Deine durchschnittlichen Kalorien pro Mahlzeit liegen in einem ausgewogenen Bereich.")

    if "completed" in progress_df.columns:
        completed_count = len(progress_df[progress_df["completed"] == True])
        if completed_count < 3:
            tips.append("Du hast erst wenige Trainings gespeichert. Regelmäßigkeit wäre der nächste Schritt.")
        else:
            tips.append("Du hast bereits mehrere Trainings gespeichert. Gute Grundlage für Fortschritt.")

    for tip in tips:
        st.info(tip)
else:
    st.info("Speichere zuerst Mahlzeiten und Trainings, damit die App automatische Empfehlungen geben kann.")