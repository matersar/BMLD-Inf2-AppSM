# 💪 FitPlan – Fitness & Ernährungs App

## Leistungsnachweis – Informatik 2 (BMLD/ZHAW), FS26

FitPlan ist eine interaktive Streamlit-App, welche Training, Ernährung, Analyse und Fortschritt in einer Anwendung verbindet.

Die App unterstützt Benutzer:innen dabei, ihre persönlichen Fitness- und Ernährungsziele besser zu verfolgen, Mahlzeiten auszuwerten, Trainingsfortschritte zu speichern und Entwicklungen langfristig sichtbar zu machen.

---

## 🌐 Streamlit App

[Zur Streamlit App](https://bmld-inf2-appsm-jxzz7pmeirrag6tclp7xhu.streamlit.app/)

---

## 📖 Nutzung der App

1. Profil ausfüllen
2. Trainingsziel, Fitnesslevel und Trainingstage festlegen
3. Trainingsplan nutzen und Fortschritte speichern
4. Mahlzeiten im Nährwertrechner erfassen
5. Ernährungs- und Trainingsdaten analysieren
6. Fortschritte und Ziele verfolgen

---

## 🚀 Hauptfunktionen

### 👤 Persönliches Profil

- Speicherung persönlicher Daten
- Fitnesslevel auswählen
- Trainingsziel definieren
- Anzahl Trainingstage pro Woche festlegen
- BMI Berechnung und Bewertung

---

### 🥗 Nährwert Rechner

- Berechnung von Kalorien und Makronährstoffen pro Portion
- Protein-, Fett-, Kohlenhydrat-, Zucker- und Ballaststoffanalyse
- Persönliche Tagesziele für Kalorien, Protein und Wasser werden anhand von Gewicht, Trainingstagen und Trainingsziel berechnet
- Bewertung der Mahlzeiten passend zum Trainingsziel
- Speicherung von Mahlzeiten
- CSV Export der gespeicherten Daten

---

### 🏋️ Trainingsplan

- Automatisch generierte Trainingspläne
- Unterschiedliche Trainingsziele:
  - Muskelaufbau
  - Abnehmen
  - Gesünder & fitter werden
- Trainingspläne für Anfänger, Mittelstufe und Fortgeschrittene
- Übungen nach Muskelgruppen
- Wochenfortschritt speichern
- Motivation, Badges und Streak-System
- Übungen mit visuellen Anleitungen
- Start- und Endpositionen der Übungen
- Anatomische Muskelmarkierungen
- Home- und Gym-Modus mit automatisch angepassten Übungen
- Individuelle Gewichtsempfehlungen für Gym-Übungen
- Bewertung der Trainingsgewichte (zu leicht, passend oder zu schwer) mit Anpassungsempfehlungen

---

### 📊 Analyse

- Transparente Darstellung der verwendeten Berechnungen und Zielwerte
- Auswertung gespeicherter Ernährungsdaten
- Durchschnittliche Kalorien- und Proteinwerte
- Trainingsanalyse
- Automatische Empfehlungen und Bewertungen
- Übersicht über Fortschritte und Entwicklung

---

### 🏠 Dashboard

- Persönliche Begrüssung für den Benutzer
- Übersichtliche Einführung in die App und ihre Funktionen
- Erklärung der wichtigsten Bereiche wie Profil, Ernährung, Training, Analyse und Motivation
- Schnellübersicht über persönliche Ziele, absolvierte Trainings und gespeicherte Mahlzeiten
- Zentrale Startseite für einen schnellen Überblick über die wichtigsten Informationen

---

### ❓ Help & Support

- FAQ Bereich
- Hilfe zur Nutzung der App
- Feedbackformular
- Unterstützung für neue Benutzer:innen

---

## 🛠️ Verwendete Technologien

- Python
- Streamlit
- Pandas
- Altair
- CSV Datenspeicherung
- WebDAV über SWITCH Drive

---

## 💾 Datenspeicherung

Die Daten werden automatisch gespeichert:

- Profilinformationen
- Mahlzeiten
- Trainingsfortschritte

Die Speicherung erfolgt über WebDAV auf dem persönlichen SWITCH Drive.

---

## 🎯 Ziel der App

Die App soll Benutzer:innen motivieren:

- gesünder zu essen
- regelmäßiger zu trainieren
- Fortschritte sichtbar zu machen
- persönliche Fitnessziele langfristig zu erreichen

---

## 📚 Learnings & Reflexion

Während der Entwicklung von FitPlan lernten wir:

- Arbeiten mit Streamlit
- Datenverwaltung mit Pandas
- Speicherung über WebDAV
- Strukturierung grösserer Python-Projekte
- Entwicklung einer benutzerfreundlichen Oberfläche
- Verbindung von Trainings- und Ernährungsdaten

Eine besondere Herausforderung war die stabile Datenspeicherung sowie die Verknüpfung von Training, Ernährung und Fortschrittsanalyse innerhalb einer gemeinsamen Anwendung.

Zusätzlich konnten wir unsere Kenntnisse im Bereich UI-Design, Datenanalyse und Projektstrukturierung erweitern.

---

## 👥 Team

- Sarah Matera (matersar@students.zhaw.ch)
- Jelena Radic (radicjel@students.zhaw.ch)
- Jovana Pavlovic (pavlojov@students.zhaw.ch)