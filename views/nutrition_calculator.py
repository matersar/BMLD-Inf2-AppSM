import streamlit as st
import pandas as pd

from utils.data_manager import DataManager

data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Informatik_2_App"
)

STANDARD_COLUMNS = [
    "timestamp",
    "Name",
    "Portion (g)",
    "Kalorien",
    "Protein",
    "Fett",
    "Kohlenhydrate",
    "Zucker",
    "Ballaststoffe",
    "Mahlzeit-Typ",
    "Ziel",
    "Lecker-Score",
    "Notiz"
]

st.title("🥗 Nährwert Rechner")

st.write("""
Mit diesem Rechner kannst du die Nährwerte deiner Mahlzeit berechnen.
Zusätzlich nutzt die App dein gespeichertes Profil, um persönliche Empfehlungen
für Kalorien, Protein und Wasser zu geben.
""")

profile_df = data_manager.load_user_data(
    "profile.csv",
    initial_value=pd.DataFrame()
)

if not profile_df.empty:
    profile = profile_df.iloc[-1]

    profil_ziel = profile.get("Ziel", "Muskelaufbau")
    profil_gewicht = float(profile.get("Gewicht", 70))
    profil_trainingstage = int(profile.get("Trainingstage", 3))
    profil_name = profile.get("Name", "")

    st.success(f"Profil geladen ✅ {profil_name}")
else:
    profil_ziel = "Muskelaufbau"
    profil_gewicht = 70.0
    profil_trainingstage = 3
    st.info("Noch kein Profil gespeichert. Es werden Standardwerte genutzt.")

if profil_ziel == "Muskelaufbau":
    default_goal = "Zunehmen"
elif profil_ziel == "Abnehmen":
    default_goal = "Abnehmen"
else:
    default_goal = "Halten"

if default_goal == "Abnehmen":
    kalorien_ziel = profil_gewicht * 28
    protein_ziel = profil_gewicht * 1.6
elif default_goal == "Zunehmen":
    kalorien_ziel = profil_gewicht * 36
    protein_ziel = profil_gewicht * 1.8
else:
    kalorien_ziel = profil_gewicht * 32
    protein_ziel = profil_gewicht * 1.5

kalorien_ziel = kalorien_ziel + (profil_trainingstage * 50)
wasser_ziel = profil_gewicht * 35 / 1000

st.subheader("🎯 Persönliche Tagesziele")

col_z1, col_z2, col_z3 = st.columns(3)
col_z1.metric("🔥 Kalorienziel heute", f"{kalorien_ziel:.0f} kcal")
col_z2.metric("💪 Proteinziel heute", f"{protein_ziel:.0f} g")
col_z3.metric("💧 Wasserziel heute", f"{wasser_ziel:.1f} L")

st.caption("Die Werte sind einfache Richtwerte basierend auf Gewicht, Ziel und Trainingstagen.")

if "data_df" not in st.session_state:
    st.session_state["data_df"] = data_manager.load_user_data(
        "data.csv",
        initial_value=pd.DataFrame(columns=STANDARD_COLUMNS),
        parse_dates=["timestamp"]
    )

with st.form("nutrition_form"):
    st.subheader("Lebensmittel eingeben")

    meal_name = st.text_input("Name der Mahlzeit", value="Meine Mahlzeit")
    portion_g = st.number_input("Portionsgröße (g)", min_value=0.0, value=250.0)

    calories_100 = st.number_input("Kalorien pro 100g", value=200.0)
    protein_100 = st.number_input("Protein pro 100g", value=10.0)
    fat_100 = st.number_input("Fett pro 100g", value=8.0)
    sugar_100 = st.number_input("Zucker pro 100g", value=5.0)
    carbs_100 = st.number_input("Kohlenhydrate pro 100g", value=25.0)
    fiber_100 = st.number_input("Ballaststoffe pro 100g", value=3.0)

    meal_type = st.selectbox(
        "Mahlzeit-Typ",
        ["Frühstück", "Mittagessen", "Abendessen", "Snack"]
    )

    goal_options = ["Abnehmen", "Halten", "Zunehmen"]

    goal = st.radio(
        "Ernährungsziel",
        goal_options,
        index=goal_options.index(default_goal)
    )

    tasty = st.slider("Wie lecker ist es? 😋", 1, 10, 7)

    add_note = st.checkbox("Notiz hinzufügen")
    note = st.text_area("Notiz", disabled=not add_note)

    submitted = st.form_submit_button("✅ Nährwerte berechnen")

if submitted:
    factor = portion_g / 100

    calories = calories_100 * factor
    protein = protein_100 * factor
    fat = fat_100 * factor
    sugar = sugar_100 * factor
    carbs = carbs_100 * factor
    fiber = fiber_100 * factor

    st.session_state["last_meal"] = {
        "timestamp": pd.Timestamp.now(),
        "Name": meal_name,
        "Portion (g)": round(portion_g, 1),
        "Kalorien": round(calories, 0),
        "Protein": round(protein, 1),
        "Fett": round(fat, 1),
        "Kohlenhydrate": round(carbs, 1),
        "Zucker": round(sugar, 1),
        "Ballaststoffe": round(fiber, 1),
        "Mahlzeit-Typ": meal_type,
        "Ziel": goal,
        "Lecker-Score": tasty,
        "Notiz": note if add_note else ""
    }

    st.subheader(f"📊 Ergebnis: {meal_name}")
    st.write(f"Mahlzeit-Typ: {meal_type} | Ernährungsziel: {goal} | Lecker-Score: {tasty}/10")

    col1, col2, col3 = st.columns(3)
    col1.metric("Kalorien", f"{calories:.0f} kcal")
    col2.metric("Protein", f"{protein:.1f} g")
    col3.metric("Fett", f"{fat:.1f} g")

    col4, col5, col6 = st.columns(3)
    col4.metric("Zucker", f"{sugar:.1f} g")
    col5.metric("Kohlenhydrate", f"{carbs:.1f} g")
    col6.metric("Ballaststoffe", f"{fiber:.1f} g")

    st.subheader("📈 Nährwerte als Diagramm")

    chart_df = pd.DataFrame({
        "Nährwert": ["Protein", "Fett", "Kohlenhydrate", "Zucker", "Ballaststoffe"],
        "Gramm": [protein, fat, carbs, sugar, fiber]
    })

    st.bar_chart(chart_df, x="Nährwert", y="Gramm")

    st.subheader("🎯 Bewertung dieser Mahlzeit")

    kalorien_anteil = calories / kalorien_ziel
    protein_anteil = protein / protein_ziel

    col_a, col_b = st.columns(2)
    col_a.metric("🔥 Anteil am Tages-Kalorienziel", f"{kalorien_anteil * 100:.0f}%")
    col_b.metric("💪 Anteil am Tages-Proteinziel", f"{protein_anteil * 100:.0f}%")

    if goal == "Abnehmen":
        if calories <= kalorien_ziel / 3 and protein >= protein_ziel / 4:
            st.success("Diese Mahlzeit passt gut zum Abnehmen: moderate Kalorien und viel Protein.")
        elif calories > kalorien_ziel / 2:
            st.warning("Diese Mahlzeit ist für Abnehmen relativ kalorienreich.")
        else:
            st.info("Diese Mahlzeit ist okay fürs Abnehmen. Achte weiter auf genug Protein.")

    elif goal == "Zunehmen":
        if calories >= kalorien_ziel / 4 and protein >= protein_ziel / 4:
            st.success("Diese Mahlzeit passt gut zu Muskelaufbau/Zunehmen: genug Kalorien und Protein.")
        else:
            st.info("Für Muskelaufbau/Zunehmen könntest du mehr Kalorien oder Protein ergänzen.")

    else:
        if calories <= kalorien_ziel / 3:
            st.success("Diese Mahlzeit passt gut in deine Tagesbilanz.")
        else:
            st.info("Achte beim Halten auf deine gesamte Tagesbilanz.")

    st.subheader("🧠 Kurze Einschätzung")

    if protein >= 25 and sugar <= 15:
        st.success("Proteinreich und wenig Zucker.")
    elif sugar > 30:
        st.warning("Viel Zucker.")
    else:
        st.info("Sieht okay aus.")

st.subheader("💾 Mahlzeiten speichern")

if st.button("➕ Mahlzeit speichern", key="save_btn"):
    if "last_meal" not in st.session_state:
        st.error("Bitte zuerst die Nährwerte berechnen, bevor du die Mahlzeit speicherst.")
    else:
        new_row = st.session_state["last_meal"]

        st.session_state["data_df"] = pd.concat(
            [st.session_state["data_df"], pd.DataFrame([new_row])],
            ignore_index=True
        )

        data_manager.save_user_data(st.session_state["data_df"], "data.csv")
        st.success("Mahlzeit gespeichert! ✅")

df = st.session_state["data_df"]
df_anzeige = df[[col for col in STANDARD_COLUMNS if col in df.columns]].copy()

if not df_anzeige.empty:
    st.subheader("📊 Gespeicherte Mahlzeiten")

    df_tabelle = df_anzeige.copy()
    df_tabelle["timestamp"] = pd.to_datetime(df_tabelle["timestamp"], errors="coerce")
    df_tabelle["Datum"] = df_tabelle["timestamp"].dt.strftime("%d.%m.%Y %H:%M")

    df_tabelle = df_tabelle.rename(columns={
        "Kalorien": "Kalorien (kcal)",
        "Protein": "Protein (g)",
        "Fett": "Fett (g)",
        "Kohlenhydrate": "Kohlenhydrate (g)",
        "Zucker": "Zucker (g)",
        "Ballaststoffe": "Ballaststoffe (g)"
    })

    sichtbare_spalten = [
        "Datum",
        "Name",
        "Portion (g)",
        "Kalorien (kcal)",
        "Protein (g)",
        "Fett (g)",
        "Kohlenhydrate (g)",
        "Zucker (g)",
        "Ballaststoffe (g)",
        "Mahlzeit-Typ",
        "Ziel",
        "Lecker-Score",
        "Notiz"
    ]

    df_tabelle = df_tabelle[[col for col in sichtbare_spalten if col in df_tabelle.columns]]

    st.dataframe(df_tabelle, use_container_width=True)

    df_heute = df_anzeige.copy()
    df_heute["timestamp"] = pd.to_datetime(df_heute["timestamp"], errors="coerce")
    heute = pd.Timestamp.now().date()
    df_heute = df_heute[df_heute["timestamp"].dt.date == heute]

    st.subheader("📈 Heute gegessen vs. Tagesziel")

    if not df_heute.empty:
        heute_kcal = df_heute["Kalorien"].sum()
        heute_protein = df_heute["Protein"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("🔥 Heute Kalorien", f"{heute_kcal:.0f} kcal")
        col2.metric("💪 Heute Protein", f"{heute_protein:.1f} g")
        col3.metric("🍽️ Mahlzeiten heute", len(df_heute))

        kalorien_fortschritt = min(heute_kcal / kalorien_ziel, 1.0)
        protein_fortschritt = min(heute_protein / protein_ziel, 1.0)

        st.write(f"Kalorien heute: {heute_kcal:.0f} / {kalorien_ziel:.0f} kcal")
        st.progress(kalorien_fortschritt)

        st.write(f"Protein heute: {heute_protein:.1f} / {protein_ziel:.0f} g")
        st.progress(protein_fortschritt)

        st.subheader("💡 Empfehlung für heute")

        if heute_kcal > kalorien_ziel * 1.1:
            st.warning("Du liegst heute über deinem Kalorienziel. Achte bei weiteren Mahlzeiten auf leichtere Optionen.")
        elif heute_kcal < kalorien_ziel * 0.7:
            st.info("Du hast heute noch Kalorien offen. Eine ausgewogene weitere Mahlzeit wäre sinnvoll.")
        else:
            st.success("Deine Kalorien liegen heute gut im Zielbereich.")

        if heute_protein < protein_ziel * 0.7:
            st.info("Dein Protein ist heute noch eher niedrig. Proteinreiche Lebensmittel könnten helfen.")
        else:
            st.success("Dein Protein liegt heute gut im Bereich.")

    else:
        st.info("Für heute wurden noch keine Mahlzeiten gespeichert.")

    st.subheader("📊 Statistik aller gespeicherten Mahlzeiten")

    total_kcal = df_anzeige["Kalorien"].sum()
    avg_kcal = df_anzeige["Kalorien"].mean()
    total_protein = df_anzeige["Protein"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Gesamt Kalorien", f"{total_kcal:.0f} kcal")
    col2.metric("📊 Durchschnitt Kalorien", f"{avg_kcal:.0f} kcal")
    col3.metric("💪 Gesamt Protein", f"{total_protein:.1f} g")

    top_protein = df_anzeige.loc[df_anzeige["Protein"].idxmax()]
    st.info(
        f"🏆 Proteinreichste Mahlzeit: "
        f"{top_protein['Name']} ({top_protein['Protein']} g Protein)"
    )

    col3, col4 = st.columns(2)

    with col3:
        if st.button("Liste leeren"):
            st.session_state["data_df"] = pd.DataFrame(columns=STANDARD_COLUMNS)
            data_manager.save_user_data(st.session_state["data_df"], "data.csv")
            st.rerun()

    with col4:
        csv = df_tabelle.to_csv(index=False)

        st.download_button(
            "CSV exportieren",
            csv,
            "mahlzeiten.csv",
            "text/csv"
        )