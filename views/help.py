import streamlit as st

st.set_page_config(page_title="Help & Support", page_icon="❓", layout="wide")

st.title("Help & Support")
st.write("Hier findest du Hilfe zur Nutzung der FitPlan App.")

st.markdown("---")

st.header("So funktioniert die App")

st.write("""
1. **Profil ausfüllen**  
   Gib dein Ziel, dein Fitnesslevel, dein Gewicht und deine Trainingstage ein.

2. **Trainingsplan nutzen**  
   Wähle deinen Plan aus und schaue dir die passenden Übungen an.

3. **Übungen anschauen**  
   Jede Übung zeigt dir Startposition, Endposition und die belasteten Muskeln.

4. **Ernährung eintragen**  
   Im Nährwertrechner kannst du Mahlzeiten speichern und analysieren.

5. **Fortschritt kontrollieren**  
   In der Analyse siehst du Diagramme und Auswertungen zu Training und Ernährung.
""")

st.markdown("---")

st.header("Häufige Fragen")

with st.expander("Wie speichere ich mein Training?"):
    st.write("Markiere erledigte Übungen oder Trainingstage und klicke danach auf den Speicher-Button.")

with st.expander("Wie ändere ich mein Ziel?"):
    st.write("Gehe zur Profil-Seite und wähle dort dein neues Ziel aus, z.B. Muskelaufbau, Abnehmen oder Fitness verbessern.")

with st.expander("Wo sehe ich meine Fortschritte?"):
    st.write("Auf der Analyse-Seite findest du Diagramme und Kennzahlen zu Training und Ernährung.")

with st.expander("Warum werden mir bestimmte Übungen angezeigt?"):
    st.write("Die Übungen werden anhand deines Ziels, Fitnesslevels und deiner Trainingshäufigkeit ausgewählt.")

st.markdown("---")

st.header("Kontakt / Feedback")

name = st.text_input("Name")
email = st.text_input("E-Mail")
message = st.text_area("Dein Anliegen oder Feedback")

if st.button("Feedback senden"):
    if name and email and message:
        st.success("Danke für dein Feedback! Deine Nachricht wurde erfasst.")
    else:
        st.warning("Bitte fülle alle Felder aus.")