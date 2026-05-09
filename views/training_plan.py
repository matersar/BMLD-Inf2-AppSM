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

GOAL_OPTIONS = ["Muskelaufbau", "Abnehmen", "Gesünder & fitter werden"]
LEVEL_OPTIONS = ["Anfänger", "Mittelstufe", "Fortgeschritten"]
TRAININGDAY_OPTIONS = [3, 4, 5]

profile_df = data_manager.load_user_data(
    "profile.csv",
    initial_value=pd.DataFrame()
)

if not profile_df.empty:
    latest_profile = profile_df.iloc[-1]
    default_ziel = latest_profile.get("Ziel", "Muskelaufbau")
    default_level = latest_profile.get("Fitnesslevel", "Anfänger")
    default_trainingstage = int(latest_profile.get("Trainingstage", 3))
    st.success("Profil wurde geladen ✅")
else:
    default_ziel = "Muskelaufbau"
    default_level = "Anfänger"
    default_trainingstage = 3
    st.info("Noch kein Profil gespeichert. Du kannst trotzdem einen Trainingsplan erstellen.")

if default_ziel not in GOAL_OPTIONS:
    default_ziel = "Muskelaufbau"

if default_level not in LEVEL_OPTIONS:
    default_level = "Anfänger"

if default_trainingstage not in TRAININGDAY_OPTIONS:
    default_trainingstage = 3

ziel = st.selectbox(
    "Was ist dein Ziel?",
    GOAL_OPTIONS,
    index=GOAL_OPTIONS.index(default_ziel)
)

level = st.selectbox(
    "Was ist dein Fitnesslevel?",
    LEVEL_OPTIONS,
    index=LEVEL_OPTIONS.index(default_level)
)

if level == "Anfänger":
    st.info("🏁 Anfänger: 0–1 Training pro Woche • Fokus auf Grundlagen und Einstieg")
elif level == "Mittelstufe":
    st.info("⚡ Mittelstufe: 2–3 Trainings pro Woche • Regelmäßiger Sport und erste Erfahrung")
else:
    st.info("🔥 Fortgeschritten: 4–6 Trainings pro Woche • Intensives und konstantes Training")

trainingstage_anzahl = st.selectbox(
    "Wie viele Trainingstage pro Woche möchtest du?",
    TRAININGDAY_OPTIONS,
    index=TRAININGDAY_OPTIONS.index(default_trainingstage)
)

st.subheader("Dein Trainingsplan")

if ziel == "Muskelaufbau":
    fokus_text = "Fokus: Krafttraining und Muskelaufbau"
    zielwerte = {"protein_min": 25, "protein_max": 50, "kalorien_min": 600, "kalorien_max": 900}

    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Rücken & Arme": ["Rücken", "Arme"],
            "Dienstag: Pause": [],
            "Mittwoch: Beine & Po": ["Beine", "Po"],
            "Donnerstag: Pause": [],
            "Freitag: Bauch & Ganzkörper": ["Bauch", "Beine", "Rücken"],
            "Samstag: Optional Cardio": [],
            "Sonntag: Pause": [],
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine & Po": ["Beine", "Po"],
            "Mittwoch: Pause": [],
            "Donnerstag: Arme & Bauch": ["Arme", "Bauch"],
            "Freitag: Pause": [],
            "Samstag: Ganzkörper": ["Beine", "Rücken", "Po"],
            "Sonntag: Pause": [],
        }
    else:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine": ["Beine"],
            "Mittwoch: Arme & Bauch": ["Arme", "Bauch"],
            "Donnerstag: Po": ["Po"],
            "Freitag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Samstag: Pause": [],
            "Sonntag: Pause": [],
        }

elif ziel == "Abnehmen":
    fokus_text = "Fokus: Ganzkörpertraining und Kalorienverbrauch"
    zielwerte = {"protein_min": 20, "protein_max": 40, "kalorien_min": 350, "kalorien_max": 650}

    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Beine & Bauch": ["Beine", "Bauch"],
            "Dienstag: Cardio": [],
            "Mittwoch: Rücken & Po": ["Rücken", "Po"],
            "Donnerstag: Pause": [],
            "Freitag: Ganzkörper": ["Beine", "Rücken", "Bauch", "Po"],
            "Samstag: Cardio": [],
            "Sonntag: Pause": [],
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Dienstag: Cardio": [],
            "Mittwoch: Beine & Po": ["Beine", "Po"],
            "Donnerstag: Pause": [],
            "Freitag: Bauch & Rücken": ["Bauch", "Rücken"],
            "Samstag: Ganzkörper": ["Beine", "Po", "Bauch"],
            "Sonntag: Pause": [],
        }
    else:
        trainingsplan = {
            "Montag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Dienstag: Beine & Po": ["Beine", "Po"],
            "Mittwoch: Cardio": [],
            "Donnerstag: Rücken & Bauch": ["Rücken", "Bauch"],
            "Freitag: Ganzkörper": ["Beine", "Po", "Arme"],
            "Samstag: Optional Cardio": [],
            "Sonntag: Pause": [],
        }

else:
    fokus_text = "Fokus: gesünder werden und allgemeine Fitness verbessern"
    zielwerte = {"protein_min": 20, "protein_max": 45, "kalorien_min": 450, "kalorien_max": 750}

    if trainingstage_anzahl == 3:
        trainingsplan = {
            "Montag: Oberkörper": ["Rücken", "Arme"],
            "Dienstag: Pause": [],
            "Mittwoch: Unterkörper": ["Beine", "Po"],
            "Donnerstag: Mobility": [],
            "Freitag: Core": ["Bauch", "Beine"],
            "Samstag: Optional Bewegung": [],
            "Sonntag: Pause": [],
        }
    elif trainingstage_anzahl == 4:
        trainingsplan = {
            "Montag: Oberkörper": ["Rücken", "Arme"],
            "Dienstag: Unterkörper": ["Beine", "Po"],
            "Mittwoch: Pause": [],
            "Donnerstag: Core": ["Bauch"],
            "Freitag: Pause": [],
            "Samstag: Ganzkörper": ["Beine", "Rücken", "Bauch"],
            "Sonntag: Pause": [],
        }
    else:
        trainingsplan = {
            "Montag: Rücken": ["Rücken"],
            "Dienstag: Beine": ["Beine"],
            "Mittwoch: Bauch": ["Bauch"],
            "Donnerstag: Arme": ["Arme"],
            "Freitag: Ganzkörper": ["Po", "Beine", "Rücken"],
            "Samstag: Pause": [],
            "Sonntag: Pause": [],
        }

st.write(fokus_text)

trainingstage = {
    tag: muskelgruppen
    for tag, muskelgruppen in trainingsplan.items()
    if muskelgruppen
}

if "checkbox_states" not in st.session_state:
    st.session_state["checkbox_states"] = {}

st.subheader("Fortschritt diese Woche")

current_keys = []

for tag in trainingstage:
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
    for tag in trainingstage:
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
gesamt = len(trainingstage)
prozent = round((erledigt_count / gesamt) * 100) if gesamt > 0 else 0

st.progress(erledigt_count / gesamt if gesamt > 0 else 0)
st.write(f"Du hast **{erledigt_count} von {gesamt} Trainingstagen** geschafft.")
st.metric("📈 Wochenfortschritt", f"{prozent}%")

st.divider()

st.subheader("🏅 Motivation & Badges")

try:
    df_for_badges = progress_manager.load_progress()
except Exception:
    df_for_badges = pd.DataFrame(columns=[
        "timestamp",
        "goal",
        "level",
        "training_days",
        "day_name",
        "completed"
    ])

if not df_for_badges.empty and "completed" in df_for_badges.columns:
    erledigt_badges_df = df_for_badges[df_for_badges["completed"] == True].copy()
    erledigte_gesamt = len(erledigt_badges_df)

    if erledigte_gesamt == 0:
        badge = "Noch kein Badge"
        motivation = "Starte mit deinem ersten Training und speichere deinen Fortschritt."
    elif erledigte_gesamt < 5:
        badge = "🏁 Starter"
        motivation = "Sehr guter Anfang! Bleib dran und sammle weitere Trainings."
    elif erledigte_gesamt < 15:
        badge = "🔥 Dranbleiber"
        motivation = "Stark! Du trainierst bereits regelmäßig."
    else:
        badge = "💪 Trainingsmaschine"
        motivation = "Mega! Du hast schon viele Trainings geschafft."

    streak = 0

    try:
        erledigt_badges_df["timestamp"] = pd.to_datetime(erledigt_badges_df["timestamp"])
        erledigt_badges_df["datum"] = erledigt_badges_df["timestamp"].dt.date

        einzigartige_tage = sorted(
            erledigt_badges_df["datum"].unique(),
            reverse=True
        )

        if len(einzigartige_tage) > 0:
            streak = 1

            for i in range(1, len(einzigartige_tage)):
                differenz = (einzigartige_tage[i - 1] - einzigartige_tage[i]).days

                if differenz == 1:
                    streak += 1
                else:
                    break

    except Exception:
        streak = 0

    col_b1, col_b2, col_b3 = st.columns(3)
    col_b1.metric("✅ Trainings insgesamt", erledigte_gesamt)
    col_b2.metric("🏅 Badge", badge)
    col_b3.metric("🔥 Streak", f"{streak} Tage")

    st.info(motivation)

    if streak >= 7:
        st.success("🔥 Unglaublich! Du trainierst seit 7 Tagen oder mehr in Folge!")
    elif streak >= 3:
        st.success(f"🔥 Stark! Du bist seit {streak} Tagen aktiv.")
    elif streak >= 1:
        st.info("💪 Gute Arbeit! Halte deine Trainingsroutine aufrecht.")

    if erledigt_count == gesamt and gesamt > 0:
        st.success("🎉 Wochenziel erreicht! Alle geplanten Trainings geschafft.")
    elif erledigt_count > 0:
        st.info("Du bist diese Woche schon aktiv gewesen. Mach weiter so 🔥")
    else:
        st.warning("Noch kein Training diese Woche abgehakt. Heute ist ein guter Start!")
else:
    st.info("Noch keine Trainingsdaten vorhanden. Speichere dein erstes Training, um Badges zu sammeln.")

st.divider()

st.subheader("🥗 Ernährung & Training Analyse")

nutrition_df = data_manager.load_user_data("data.csv", initial_value=pd.DataFrame())

if not nutrition_df.empty and "Protein" in nutrition_df.columns and "Kalorien" in nutrition_df.columns:
    avg_protein = nutrition_df["Protein"].mean()
    avg_calories = nutrition_df["Kalorien"].mean()

    st.subheader("🎯 Zielbereiche pro Mahlzeit")

    zielbereich_df = pd.DataFrame([{
        "Ziel": ziel,
        "Protein-Zielbereich": f"{zielwerte['protein_min']}–{zielwerte['protein_max']} g",
        "Kalorien-Zielbereich": f"{zielwerte['kalorien_min']}–{zielwerte['kalorien_max']} kcal",
    }])

    st.dataframe(zielbereich_df, use_container_width=True, hide_index=True)

    st.subheader("📊 Deine durchschnittliche Ernährung")

    def bewertung_wert(wert, minimum, maximum):
        if wert < minimum:
            return "zu niedrig"
        if wert > maximum:
            return "zu hoch"
        return "im Zielbereich"

    protein_status = bewertung_wert(avg_protein, zielwerte["protein_min"], zielwerte["protein_max"])
    kalorien_status = bewertung_wert(avg_calories, zielwerte["kalorien_min"], zielwerte["kalorien_max"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💪 Ø Protein pro Mahlzeit", f"{avg_protein:.1f} g", protein_status)

    with col2:
        st.metric("🔥 Ø Kalorien pro Mahlzeit", f"{avg_calories:.0f} kcal", kalorien_status)

    def berechne_score(wert, minimum, maximum):
        mitte = (minimum + maximum) / 2
        toleranz = (maximum - minimum) / 2

        if minimum <= wert <= maximum:
            return 100

        abstand = abs(wert - mitte)
        score = max(0, 100 - ((abstand - toleranz) / toleranz) * 50)
        return min(score, 100)

    protein_score = berechne_score(avg_protein, zielwerte["protein_min"], zielwerte["protein_max"])
    kalorien_score = berechne_score(avg_calories, zielwerte["kalorien_min"], zielwerte["kalorien_max"])
    gesamt_score = round((protein_score + kalorien_score) / 2)

    if gesamt_score >= 80:
        label = "Sehr gut"
    elif gesamt_score >= 60:
        label = "Gut"
    else:
        label = "Verbesserbar"

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("💪 Protein-Score", f"{protein_score:.0f}%")
    col_b.metric("🔥 Kalorien-Score", f"{kalorien_score:.0f}%")
    col_c.metric("🎯 Gesamtbewertung", f"{gesamt_score}%", label)

    st.progress(gesamt_score / 100)

    st.subheader("🎯 Bewertung passend zu deinem Ziel")

    if protein_status == "im Zielbereich" and kalorien_status == "im Zielbereich":
        st.success("Sehr gut! Protein und Kalorien liegen passend zu deinem Trainingsziel im Zielbereich 💪")
    elif protein_status == "zu niedrig":
        st.warning("Dein Proteinwert ist für dieses Ziel zu niedrig. Ergänze proteinreiche Lebensmittel.")
    elif kalorien_status == "zu niedrig":
        st.warning("Deine Kalorien sind für dieses Ziel zu niedrig. Eine größere oder energiereichere Mahlzeit wäre sinnvoll.")
    elif kalorien_status == "zu hoch":
        st.warning("Deine Kalorien sind für dieses Ziel zu hoch. Eine kleinere Portion wäre sinnvoll.")
    else:
        st.info("Deine Ernährung ist solide, kann aber noch genauer an dein Ziel angepasst werden.")
else:
    st.info("Noch keine Ernährungsdaten vorhanden.")

st.divider()

st.subheader("📊 Gespeicherte Trainingsfortschritte")

try:
    df = progress_manager.load_progress()
except Exception:
    st.warning("Trainingsfortschritte konnten gerade nicht geladen werden. Bitte Seite neu laden.")
    df = pd.DataFrame(columns=[
        "timestamp",
        "goal",
        "level",
        "training_days",
        "day_name",
        "completed"
    ])

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
        user_level = "Mittelstufe"
    else:
        user_level = "Fortgeschritten"

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Erledigte Trainings", erledigte_anzahl)
    col2.metric("📌 Alle Einträge", len(df))
    col3.metric("🏅 Dein Level", user_level)

    st.subheader("📈 Trainingsfortschritt über Zeit")

    erledigt_chart_df = df[df["completed"] == True].copy()

    if not erledigt_chart_df.empty:
        erledigt_chart_df = erledigt_chart_df.reset_index(drop=True)

        erledigt_chart_df["Training Nr."] = range(1, len(erledigt_chart_df) + 1)
        erledigt_chart_df["Kumulierte Trainings"] = range(1, len(erledigt_chart_df) + 1)

        chart_df = erledigt_chart_df[["Training Nr.", "Kumulierte Trainings"]]

        st.line_chart(
            chart_df,
            x="Training Nr.",
            y="Kumulierte Trainings"
        )

        st.caption("Die Linie zeigt deine insgesamt erledigten Trainings im Zeitverlauf.")
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