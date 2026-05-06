import streamlit as st
import pandas as pd

from utils.data_manager import DataManager

data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Informatik_2_App"
)

st.title("🥗 Nährwert Rechner")

st.write("""
Mit diesem Rechner kannst du die Nährwerte deiner Mahlzeit berechnen.
Gib Lebensmittelmengen ein und berechne Kalorien, Protein, Zucker und Fett.
""")

# Falls data_df noch nicht existiert, vorbereiten
if "data_df" not in st.session_state:
    st.session_state["data_df"] = data_manager.load_user_data(
        "data.csv",
        initial_value=pd.DataFrame(columns=[
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
        ]),
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

    meal_type = st.selectbox("Mahlzeit Typ", ["Frühstück", "Mittagessen", "Abendessen", "Snack"])
    goal = st.radio("Ziel", ["Abnehmen", "Halten", "Zunehmen"])
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
    st.write(f"Mahlzeit-Typ: {meal_type} | Ziel: {goal} | Lecker-Score: {tasty}/10")

    col1, col2, col3 = st.columns(3)
    col1.metric("Kalorien", f"{calories:.0f} kcal")
    col2.metric("Protein", f"{protein:.1f} g")
    col3.metric("Fett", f"{fat:.1f} g")

    col4, col5, col6 = st.columns(3)
    col4.metric("Zucker", f"{sugar:.1f} g")
    col5.metric("Kohlenhydrate", f"{carbs:.1f} g")
    col6.metric("Ballaststoffe", f"{fiber:.1f} g")

    st.subheader("📈 Makros als Diagramm")

    chart_df = pd.DataFrame({
        "Makro": ["Protein", "Fett", "Kohlenhydrate", "Zucker", "Ballaststoffe"],
        "Gramm": [protein, fat, carbs, sugar, fiber]
    })

    st.bar_chart(chart_df, x="Makro", y="Gramm")

    st.subheader("🔥 Kalorienbewertung")

    if calories < 400:
        st.success("Leichte Mahlzeit")
    elif calories < 800:
        st.info("Normale Mahlzeit")
    else:
        st.warning("Sehr kalorienreich")

    st.subheader("🎯 Empfehlung passend zum Ziel")

    if goal == "Abnehmen":
        if calories <= 600 and protein >= 20:
            st.success("Gut fürs Abnehmen: moderate Kalorien und genug Protein.")
        elif calories > 800:
            st.warning("Für Abnehmen eher kalorienreich. Kleinere Portion oder mehr Gemüse wäre besser.")
        else:
            st.info("Für Abnehmen okay, achte aber auf genug Protein.")
    elif goal == "Zunehmen":
        if calories >= 600 and protein >= 25:
            st.success("Gut fürs Zunehmen/Muskelaufbau: viele Kalorien und gutes Protein.")
        else:
            st.info("Für Zunehmen könntest du mehr Kalorien oder Protein ergänzen.")
    else:
        if 400 <= calories <= 800:
            st.success("Gut zum Halten: normale Mahlzeit.")
        else:
            st.info("Achte beim Halten auf eine ausgewogene Tagesbilanz.")

    st.subheader("🧠 Kurze Einschätzung")

    if protein >= 25 and sugar <= 15:
        st.success("Proteinreich und wenig Zucker")
    elif sugar > 30:
        st.warning("Viel Zucker")
    else:
        st.info("Sieht okay aus")

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

if not st.session_state["data_df"].empty:
    st.subheader("📊 Gespeicherte Mahlzeiten")

    df = st.session_state["data_df"]

    st.dataframe(df)

    total_kcal = df["Kalorien"].sum()
    avg_kcal = df["Kalorien"].mean()

    col1, col2 = st.columns(2)
    col1.metric("🔥 Gesamt Kalorien", f"{total_kcal:.0f} kcal")
    col2.metric("📊 Durchschnitt Kalorien", f"{avg_kcal:.0f} kcal")

    if "Protein" in df.columns and not df["Protein"].empty:
        top_protein = df.loc[df["Protein"].idxmax()]
        st.info(f"🏆 Proteinreichste Mahlzeit: {top_protein['Name']} ({top_protein['Protein']} g Protein)")

    col3, col4 = st.columns(2)

    with col3:
        if st.button("Liste leeren"):
            st.session_state["data_df"] = pd.DataFrame(columns=df.columns)
            data_manager.save_user_data(st.session_state["data_df"], "data.csv")
            st.rerun()

    with col4:
        csv = df.to_csv(index=False)

        st.download_button(
            "CSV exportieren",
            csv,
            "mahlzeiten.csv",
            "text/csv"
        )