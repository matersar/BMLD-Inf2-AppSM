# Reflexion – FitPlan App

## Projektidee

Unser Ziel war es, eine interaktive Fitness- und Ernährungs-App zu entwickeln, welche Training, Ernährung und Fortschrittsanalyse in einer Anwendung kombiniert.

Die App sollte Benutzer:innen dabei unterstützen:

- ihre Ernährung besser zu verstehen,
- Trainingsziele festzulegen,
- Fortschritte sichtbar zu machen,
- und langfristig motiviert zu bleiben.

Dabei wollten wir nicht nur einfache Berechnungen anzeigen, sondern eine moderne und personalisierte Anwendung entwickeln, welche Daten analysiert und verständliche Rückmeldungen gibt.

---

## Umsetzung der App

Die Anwendung wurde mit Python und Streamlit umgesetzt. Zusätzlich nutzten wir pandas für die Datenanalyse und CSV-Dateien zur Speicherung der Benutzerdaten.

Die App besteht aus mehreren Bereichen:

### Dashboard

Das Dashboard zeigt die wichtigsten Informationen auf einen Blick:

- Profilübersicht
- BMI
- Trainingsfortschritt
- Ernährungsübersicht
- Motivation und Zusammenfassungen

### Nährwertrechner

Im Nährwertrechner können Benutzer:innen Mahlzeiten eingeben und die Nährwerte automatisch berechnen lassen.

Zusätzlich werden:

- Kalorien,
- Protein,
- Fett,
- Zucker,
- Kohlenhydrate,
- und Ballaststoffe

analysiert und bewertet.

Die App erstellt ausserdem persönliche Tagesziele basierend auf Gewicht, Ziel und Trainingshäufigkeit.

### Trainingsplan

Im Trainingsbereich kann ein individueller Trainingsplan erstellt werden.

Die Trainingspläne passen sich an:

- Fitnesslevel,
- Ziel,
- und Anzahl Trainingstage

an.

Zusätzlich werden passende Übungen automatisch aus einer gespeicherten Übungsdatenbank angezeigt.

### Analyse

Die Analyse-Seite wertet die gespeicherten Daten aus und zeigt:

- Diagramme,
- Durchschnittswerte,
- Protein- und Kalorienanalysen,
- sowie automatische Empfehlungen.

Dadurch können Benutzer:innen ihre Entwicklung besser nachvollziehen.

---

## Herausforderungen und Probleme

Während der Entwicklung traten verschiedene Probleme auf.

Ein grösseres Problem war die Speicherung der Daten. Anfangs wurden CSV-Dateien teilweise leer gespeichert oder nicht korrekt geladen. Wir mussten deshalb unsere DataManager- und ProgressManager-Klassen mehrfach anpassen.

Auch bei den Diagrammen gab es Schwierigkeiten. Teilweise wurden keine Linien angezeigt, obwohl Daten vorhanden waren. Das Problem lag an der Darstellung der Datenachsen und daran, dass die Daten zuerst korrekt numerisch verarbeitet werden mussten.

Zusätzlich hatten wir Probleme mit:

- Streamlit Session State,
- GitHub Pushes,
- Einrückungsfehlern in Python,
- sowie Fehlern beim Deployment auf Streamlit Cloud.

Durch Debugging und schrittweises Testen konnten wir diese Probleme jedoch lösen.

---

## Technische Entscheidungen

Wir entschieden uns bewusst für Streamlit, weil damit schnell interaktive Anwendungen entwickelt werden können.

CSV-Dateien wurden statt einer Datenbank verwendet, da:

- die Anwendung dadurch einfacher bleibt,
- keine externe Datenbank benötigt wird,
- und die Daten lokal beziehungsweise über WebDAV gespeichert werden können.

Die Aufteilung in mehrere Seiten war ebenfalls eine wichtige Entscheidung, damit die App übersichtlich bleibt.

---

## Zusammenarbeit im Team

Die Arbeit im Team funktionierte insgesamt gut.

Wir tauschten Ideen aus, testeten Funktionen gegenseitig und halfen uns bei Problemen. Besonders wichtig war die Kommunikation bei Fehlern und beim Zusammenführen der verschiedenen Funktionen.

Die Aufgaben wurden untereinander verteilt, beispielsweise:

- Dashboard,
- Trainingsbereich,
- Dokumentation,
- oder Analysefunktionen.

Dadurch konnten wir effizienter arbeiten.

---

## Was wir gelernt haben

Durch dieses Projekt konnten wir unser Wissen in Python deutlich erweitern.

Wir lernten unter anderem:

- mit pandas Daten auszuwerten,
- interaktive Streamlit-Apps zu entwickeln,
- GitHub zu verwenden,
- Dateien automatisch zu speichern,
- Diagramme zu erstellen,
- und Fehler systematisch zu beheben.

Zusätzlich verbesserten wir unser Verständnis für:

- Benutzerfreundlichkeit,
- Strukturierung von Code,
- und die Planung grösserer Anwendungen.

---

## Verbesserungsmöglichkeiten

In Zukunft könnte die App noch erweitert werden.

Mögliche Verbesserungen wären:

- Login-System mit Benutzerkonten,
- echte Datenbank statt CSV-Dateien,
- Kalorientracker über mehrere Tage,
- genauere Ernährungsanalysen,
- Fortschrittsgrafiken mit mehr Optionen,
- oder Trainingsvideos zu Übungen.

Auch das Design könnte weiter verbessert und noch moderner gestaltet werden.

---

## Fazit

Insgesamt war das Projekt eine sehr wertvolle Erfahrung.

Wir konnten theoretisches Wissen praktisch anwenden und lernten, wie viel Planung, Testen und Problemlösung hinter einer funktionierenden Anwendung steckt.

Besonders spannend war es zu sehen, wie aus einer einfachen Idee Schritt für Schritt eine vollständige Fitness- und Ernährungs-App entstand.

Das Projekt half uns nicht nur unsere Programmierkenntnisse zu verbessern, sondern auch unsere Fähigkeiten in Teamarbeit, Problemlösung und Projektorganisation weiterzuentwickeln.
