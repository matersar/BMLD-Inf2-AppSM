import streamlit as st
import pandas as pd
import io

st.title("🥗 Nährwert Rechner")

st.write("""
Mit diesem Rechner kannst du die Nährwerte deiner Mahlzeit berechnen.
Gib Lebensmittelmengen ein und berechne Kalorien, Protein, Zucker und Fett.
""")

# Session State vorbereiten
if "meals" not in st.session_state:
    st.session_state.meals = []

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

    meal_type = st.selectbox("Mahlzeit Typ", ["Frühstück","Mittagessen","Abendessen","Snack"])
    goal = st.radio("Ziel", ["Abnehmen","Halten","Zunehmen"])
    tasty = st.slider("Wie lecker ist es? 😋",1,10,7)

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

    # Werte speichern
    st.session_state.calories = calories
    st.session_state.protein = protein
    st.session_state.fat = fat
    st.session_state.carbs = carbs
    st.session_state.sugar = sugar
    st.session_state.fiber = fiber
    st.session_state.meal_name = meal_name
    st.session_state.meal_type = meal_type
    st.session_state.goal = goal

    st.subheader(f"📊 Ergebnis: {meal_name}")
    st.write(f"Mahlzeit-Typ: {meal_type} | Ziel: {goal} | Lecker-Score: {tasty}/10")

    col1,col2,col3 = st.columns(3)

    col1.metric("Kalorien", f"{calories:.0f} kcal")
    col2.metric("Protein", f"{protein:.1f} g")
    col3.metric("Fett", f"{fat:.1f} g")

    col4,col5,col6 = st.columns(3)

    col4.metric("Zucker", f"{sugar:.1f} g")
    col5.metric("Kohlenhydrate", f"{carbs:.1f} g")
    col6.metric("Ballaststoffe", f"{fiber:.1f} g")

    st.subheader("📈 Makros als Diagramm")

    chart_data = {
        "Makro":["Protein","Fett","Kohlenhydrate","Zucker","Ballaststoffe"],
        "Gramm":[protein,fat,carbs,sugar,fiber]
    }

    st.bar_chart(chart_data,x="Makro",y="Gramm")

    # Plausibilitätscheck
    if calories > 2000:
        st.warning("⚠️ Sehr viele Kalorien für eine Portion")

    if sugar > 50:
        st.warning("⚠️ Sehr viel Zucker")

    if protein > 100:
        st.info("💪 Extrem proteinreiche Mahlzeit")

    # Bewertung
    st.subheader("🔥 Kalorienbewertung")

    if calories < 400:
        st.success("Leichte Mahlzeit")
    elif calories < 800:
        st.info("Normale Mahlzeit")
    else:
        st.warning("Sehr kalorienreich")

    # Einschätzung
    st.subheader("🧠 Kurze Einschätzung")

    if protein >= 25 and sugar <= 15:
        st.success("Proteinreich und wenig Zucker")
    elif sugar > 30:
        st.warning("Viel Zucker")
    else:
        st.info("Sieht okay aus")

# Mahlzeit speichern
st.subheader("💾 Mahlzeiten speichern")

if st.button("➕ Mahlzeit speichern", key="save_btn"):

    st.session_state.meals.append({
        "Name": st.session_state.meal_name,
        "Kalorien": round(st.session_state.calories,0),
        "Protein": round(st.session_state.protein,1),
        "Fett": round(st.session_state.fat,1),
        "Kohlenhydrate": round(st.session_state.carbs,1),
        "Zucker": round(st.session_state.sugar,1),
        "Ballaststoffe": round(st.session_state.fiber,1),
        "Mahlzeit-Typ": st.session_state.meal_type,
        "Ziel": st.session_state.goal
    })

    st.success("Mahlzeit gespeichert!")

if st.session_state.meals:

    st.subheader("📊 Gespeicherte Mahlzeiten")

    df = pd.DataFrame(st.session_state.meals)

    st.dataframe(df)

    total_kcal = df["Kalorien"].sum()
    avg_kcal = df["Kalorien"].mean()

    st.metric("🔥 Gesamt Kalorien", f"{total_kcal:.0f} kcal")
    st.metric("📊 Durchschnitt Kalorien", f"{avg_kcal:.0f} kcal")

    top_protein = df.loc[df["Protein"].idxmax()]
    st.info(f"🏆 Proteinreichste Mahlzeit: {top_protein['Name']} ({top_protein['Protein']} g Protein)")

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Liste leeren"):
            st.session_state.meals = []
            st.rerun()

    with col2:

        csv = df.to_csv(index=False)

        st.download_button(
            "CSV exportieren",
            csv,
            "mahlzeiten.csv",
            "text/csv"
        )