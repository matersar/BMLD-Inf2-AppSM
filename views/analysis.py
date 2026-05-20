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
profile_df = data_manager.load_user_data("profile.csv", initial_value=pd.DataFrame())

try:
    progress_df = progress_manager.load_progress()
except Exception:
    progress_df = pd.DataFrame(columns=[
        "timestamp", "goal", "level", "training_days", "day_name", "completed"
    ])

st.divider()

# =========================
# ZIELWERTE AUS PROFIL
# =========================

st.subheader("🎯 Berechnete Zielwerte aus deinem Profil")

if not profile_df.empty:
    profile = profile_df.iloc[-1]

    profil_ziel = profile.get("Ziel", "Muskelaufbau")
    profil_gewicht = float(profile.get("Gewicht", 70))
    profil_trainingstage = int(profile.get("Trainingstage", 3))
    profil_name = profile.get("Name", "")

    if profil_ziel == "Muskelaufbau":
        ernährungsziel = "Zunehmen / Muskelaufbau"
        kalorien_faktor = 36
        protein_faktor = 1.8
    elif profil_ziel == "Abnehmen":
        ernährungsziel = "Abnehmen"
        kalorien_faktor = 28
        protein_faktor = 1.6
    else:
        ernährungsziel = "Halten / gesünder & fitter werden"
        kalorien_faktor = 32
        protein_faktor = 1.5

    kalorien_ziel_basis = profil_gewicht * kalorien_faktor
    trainings_bonus = profil_trainingstage * 50
    kalorien_ziel = kalorien_ziel_basis + trainings_bonus

    protein_ziel = profil_gewicht * protein_faktor
    wasser_ziel = profil_gewicht * 35 / 1000

    st.write(
        f"Die Zielwerte werden automatisch aus deinem Profil berechnet. "
        f"Dafür nutzt die App dein Gewicht, dein Ziel und deine Trainingstage pro Woche."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Kalorienziel", f"{kalorien_ziel:.0f} kcal/Tag")
    col2.metric("💪 Proteinziel", f"{protein_ziel:.0f} g/Tag")
    col3.metric("💧 Wasserziel", f"{wasser_ziel:.1f} L/Tag")

    st.subheader("🧮 Verwendete Berechnung")

    berechnung_df = pd.DataFrame([
        {
            "Bereich": "Profilbasis",
            "Berechnung": "Gewicht, Ziel und Trainingstage aus dem Profil",
            "Ergebnis": f"{profil_gewicht:.1f} kg, {profil_ziel}, {profil_trainingstage} Trainingstage/Woche"
        },
        {
            "Bereich": "Kalorien",
            "Berechnung": f"{profil_gewicht:.1f} kg × {kalorien_faktor} + ({profil_trainingstage} × 50 kcal)",
            "Ergebnis": f"{kalorien_ziel:.0f} kcal/Tag"
        },
        {
            "Bereich": "Protein",
            "Berechnung": f"{profil_gewicht:.1f} kg × {protein_faktor}",
            "Ergebnis": f"{protein_ziel:.0f} g/Tag"
        },
        {
            "Bereich": "Wasser",
            "Berechnung": f"{profil_gewicht:.1f} kg × 35 ml ÷ 1000",
            "Ergebnis": f"{wasser_ziel:.1f} L/Tag"
        }
    ])

    st.dataframe(berechnung_df, use_container_width=True, hide_index=True)

    st.caption(
        "Die Werte sind einfache Fitness-Richtwerte und dienen als Orientierung. "
        "Sie ersetzen keine medizinische oder ernährungswissenschaftliche Beratung."
    )

else:
    st.info("Noch kein Profil gespeichert. Speichere zuerst dein Profil, damit Zielwerte berechnet werden können.")

st.divider()

# =========================
# ERNÄHRUNGSANALYSE
# =========================

st.subheader("🥗 Ernährungsanalyse")

if not nutrition_df.empty and "Kalorien" in nutrition_df.columns and "Protein" in nutrition_df.columns:
    df = nutrition_df.copy()
    df["Kalorien"] = pd.to_numeric(df["Kalorien"], errors="coerce")
    df["Protein"] = pd.to_numeric(df["Protein"], errors="coerce")
    df = df.dropna(subset=["Kalorien", "Protein"])
    df = df.reset_index(drop=True)

    df["Eintrag"] = range(1, len(df) + 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("🍽️ Mahlzeiten", len(df))
    col2.metric("🔥 Ø Kalorien", f"{df['Kalorien'].mean():.0f} kcal")
    col3.metric("💪 Ø Protein", f"{df['Protein'].mean():.1f} g")

    if len(df) >= 2:
        st.subheader("📈 Kalorienverlauf")

        kalorien_chart = df[["Eintrag", "Kalorien"]]

        st.line_chart(
            kalorien_chart,
            x="Eintrag",
            y="Kalorien"
        )

        st.caption("X-Achse = gespeicherte Mahlzeiten in Reihenfolge.")

        st.subheader("📈 Proteinverlauf")

        protein_chart = df[["Eintrag", "Protein"]]

        st.line_chart(
            protein_chart,
            x="Eintrag",
            y="Protein"
        )

        st.caption("X-Achse = gespeicherte Mahlzeiten in Reihenfolge.")
    else:
        st.info("Für eine Linie brauchst du mindestens 2 gespeicherte Mahlzeiten.")

    st.subheader("🏆 Top-Mahlzeiten")

    top_protein = df.loc[df["Protein"].idxmax()]
    top_calories = df.loc[df["Kalorien"].idxmax()]

    st.info(
        f"Proteinreichste Mahlzeit: **{top_protein['Name']}** "
        f"mit **{top_protein['Protein']} g Protein**"
    )

    st.info(
        f"Kalorienreichste Mahlzeit: **{top_calories['Name']}** "
        f"mit **{top_calories['Kalorien']} kcal**"
    )
else:
    st.info("Noch keine Ernährungsdaten vorhanden.")

st.divider()

# =========================
# TRAININGSANALYSE
# =========================

st.subheader("🏋️ Trainingsanalyse")

if not progress_df.empty and "completed" in progress_df.columns:
    df_train = progress_df.copy()

    df_train["completed"] = df_train["completed"].astype(bool)

    erledigt_df = df_train[df_train["completed"] == True].copy()
    erledigt_df = erledigt_df.reset_index(drop=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Alle Einträge", len(df_train))
    col2.metric("✅ Erledigte Trainings", len(erledigt_df))
    col3.metric("❌ Nicht erledigt", len(df_train) - len(erledigt_df))

    if not erledigt_df.empty:
        erledigt_df["timestamp"] = pd.to_datetime(
            erledigt_df["timestamp"],
            errors="coerce"
        )

        erledigt_df = erledigt_df.dropna(subset=["timestamp"])
        erledigt_df["Datum"] = erledigt_df["timestamp"].dt.date

        # Diagramm 1: Erledigte Trainings pro Datum
        st.subheader("📈 Trainingsfortschritt")

        training_chart = (
            erledigt_df.groupby("Datum")
            .size()
            .reset_index(name="Erledigte Trainings")
        )

        if len(training_chart) >= 1:
            st.line_chart(
                training_chart,
                x="Datum",
                y="Erledigte Trainings"
            )

            st.caption("X-Achse = Datum, Y-Achse = Anzahl erledigte Trainings pro Tag.")
        else:
            st.info("Noch nicht genug Trainingsdaten für ein Diagramm vorhanden.")

        # Diagramm 2: Wochenziel-Fortschritt
        st.subheader("🎯 Wochenziel-Fortschritt")

        if not profile_df.empty:
            geplante_trainings = int(profile_df.iloc[-1].get("Trainingstage", 3))
        else:
            geplante_trainings = 3

        erledigte_trainings = len(erledigt_df)
        wochenfortschritt = min(
            round((erledigte_trainings / geplante_trainings) * 100),
            100
        )

        col_w1, col_w2, col_w3 = st.columns(3)
        col_w1.metric("Geplante Trainings", geplante_trainings)
        col_w2.metric("Erledigte Trainings", erledigte_trainings)
        col_w3.metric("Wochenziel", f"{wochenfortschritt}%")

        st.progress(wochenfortschritt / 100)

        if wochenfortschritt >= 100:
            st.success("Wochenziel erreicht! 🎉")
        elif wochenfortschritt >= 50:
            st.info("Du bist gut unterwegs. Mach weiter so!")
        else:
            st.warning("Du hast dein Wochenziel noch nicht erreicht.")

        st.subheader("📋 Letzte Trainings")

        display_df = erledigt_df.tail(5).rename(columns={
            "timestamp": "Datum",
            "goal": "Ziel",
            "level": "Fitnesslevel",
            "training_days": "Trainingstage",
            "day_name": "Trainingstag",
            "completed": "Erledigt"
        })

        display_df = display_df.loc[:, ~display_df.columns.duplicated()]

        display_df["Datum"] = pd.to_datetime(
            display_df["Datum"],
            errors="coerce"
        ).dt.strftime("%d.%m.%Y %H:%M")

        display_df["Erledigt"] = display_df["Erledigt"].map({True: "Ja", False: "Nein"})

        sichtbare_spalten = [
            "Datum",
            "Ziel",
            "Fitnesslevel",
            "Trainingstage",
            "Trainingstag",
            "Erledigt"
        ]

        display_df = display_df[
            [col for col in sichtbare_spalten if col in display_df.columns]
        ]

        st.dataframe(display_df, use_container_width=True)

    else:
        st.info("Noch keine erledigten Trainings vorhanden.")

else:
    st.info("Noch keine Trainingsdaten vorhanden.")

st.divider()

# =========================
# AUTOMATISCHE AUSWERTUNG
# =========================

st.subheader("🧠 Automatische Auswertung")

if not nutrition_df.empty or not progress_df.empty:
    tips = []

    if not nutrition_df.empty and "Protein" in nutrition_df.columns:
        protein_series = pd.to_numeric(nutrition_df["Protein"], errors="coerce").dropna()

        if not protein_series.empty:
            avg_protein = protein_series.mean()

            if avg_protein < 20:
                tips.append("Dein durchschnittliches Protein ist eher niedrig. Mehr proteinreiche Lebensmittel könnten helfen.")
            else:
                tips.append("Deine Proteinwerte sehen gut aus. Das unterstützt Training und Regeneration.")

    if not nutrition_df.empty and "Kalorien" in nutrition_df.columns:
        kalorien_series = pd.to_numeric(nutrition_df["Kalorien"], errors="coerce").dropna()

        if not kalorien_series.empty:
            avg_kcal = kalorien_series.mean()

            if avg_kcal < 400:
                tips.append("Deine Mahlzeiten sind durchschnittlich eher kalorienarm.")
            elif avg_kcal > 800:
                tips.append("Deine Mahlzeiten sind durchschnittlich eher kalorienreich.")
            else:
                tips.append("Deine durchschnittlichen Kalorien pro Mahlzeit liegen in einem ausgewogenen Bereich.")

    if not progress_df.empty and "completed" in progress_df.columns:
        completed_count = len(progress_df[progress_df["completed"] == True])

        if completed_count < 3:
            tips.append("Du hast erst wenige Trainings gespeichert. Regelmäßigkeit wäre der nächste Schritt.")
        else:
            tips.append("Du hast bereits mehrere Trainings gespeichert. Gute Grundlage für Fortschritt.")

    if tips:
        for tip in tips:
            st.info(tip)
    else:
        st.info("Noch nicht genug auswertbare Daten vorhanden.")
else:
    st.info("Speichere zuerst Mahlzeiten und Trainings, damit die App automatische Empfehlungen geben kann.")