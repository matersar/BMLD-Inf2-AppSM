Reflexion – FitPlan App
Projektidee

Unser Ziel war es, eine interaktive Fitness- und Ernährungs-App zu entwickeln, welche Training, Ernährung und Fortschrittsanalyse in einer Anwendung kombiniert.

Die App sollte Benutzer:innen dabei unterstützen:

ihre Ernährung besser zu verstehen,
Trainingsziele festzulegen,
Fortschritte sichtbar zu machen,
und langfristig motiviert zu bleiben.

Dabei wollten wir nicht nur einfache Berechnungen anzeigen, sondern eine moderne und personalisierte Anwendung entwickeln, welche Daten analysiert und verständliche Rückmeldungen gibt.

Zusätzlich war es uns wichtig, die Anwendung möglichst anfängerfreundlich zu gestalten. Deshalb legten wir grossen Wert auf verständliche Trainingspläne, klare Strukturen und einfache Bedienung.

Umsetzung der App

Die Anwendung wurde mit Python und Streamlit umgesetzt. Zusätzlich nutzten wir pandas für die Datenanalyse und CSV-Dateien zur Speicherung der Benutzerdaten.

Die App besteht aus mehreren Bereichen:

Dashboard

Das Dashboard dient als zentrale Startseite der App und bietet einen schnellen Überblick über die wichtigsten Funktionen.

Es enthält:

eine persönliche Begrüssung,
eine kurze Einführung in die App,
eine Übersicht der wichtigsten Bereiche,
sowie eine Schnellübersicht über Ziele, Trainings und Mahlzeiten.

Nährwertrechner 

Im Nährwertrechner können Benutzer:innen Mahlzeiten eingeben und die Nährwerte automatisch berechnen lassen.

Zusätzlich werden:

Kalorien,
Protein,
Fett,
Zucker,
Kohlenhydrate,
und Ballaststoffe

analysiert und bewertet.

Die App erstellt ausserdem persönliche Tagesziele basierend auf Gewicht, Ziel und Trainingshäufigkeit.

Zusätzlich wurde die Verbindung zwischen Ernährung und Training erweitert. Die Anwendung analysiert automatisch, ob Protein- und Kalorienwerte zum gewählten Trainingsziel passen und gibt entsprechende Rückmeldungen und Empfehlungen.

Trainingsplan

Im Trainingsbereich kann ein individueller Trainingsplan erstellt werden.

Die Trainingspläne passen sich an:

Fitnesslevel,
Ziel,
Anzahl Trainingstage,
und Trainingsort

an.

Benutzer:innen können auswählen, ob sie zuhause oder im Gym trainieren möchten. Dadurch werden automatisch passende Übungen angezeigt.

Zusätzlich werden passende Übungen automatisch aus einer gespeicherten Übungsdatenbank geladen.

Um die App anfängerfreundlicher zu gestalten, integrierten wir zusätzlich:

Übungsbilder,
kurze Übungsbeschreibungen,
sowie Tipps zur korrekten Ausführung.

Dadurch können Benutzer:innen die Übungen besser verstehen und korrekt ausführen.

Ausserdem wurden die Trainingspläne realistischer gestaltet, indem unterschiedliche Intensitäten, Trainingsumfänge und Gewichtsempfehlungen berücksichtigt werden, je nach Fitnesslevel.

Analyse

Die Analyse-Seite wertet die gespeicherten Daten aus und zeigt:

Diagramme,
Durchschnittswerte,
Protein- und Kalorienanalysen,
sowie automatische Empfehlungen.

Dadurch können Benutzer:innen ihre Entwicklung besser nachvollziehen.

Herausforderungen und Probleme

Während der Entwicklung traten verschiedene Probleme auf.

Ein grösseres Problem war die Speicherung der Daten. Anfangs wurden CSV-Dateien teilweise leer gespeichert oder nicht korrekt geladen. Wir mussten deshalb unsere DataManager- und ProgressManager-Klassen mehrfach anpassen.

Auch bei den Diagrammen gab es Schwierigkeiten. Teilweise wurden keine Linien angezeigt, obwohl Daten vorhanden waren. Das Problem lag an der Darstellung der Datenachsen und daran, dass die Daten zuerst korrekt numerisch verarbeitet werden mussten.

Zusätzlich hatten wir Probleme mit:

Streamlit Session State,
GitHub Pushes,
Einrückungsfehlern in Python,
Bildpfaden und Dateistrukturen,
sowie Fehlern beim Deployment auf Streamlit Cloud.

Durch Debugging und schrittweises Testen konnten wir diese Probleme jedoch lösen.

Eine weitere Herausforderung war die Erstellung und Auswahl der Übungsbilder. Da alle Übungsbilder mithilfe von KI generiert wurden, mussten die Beschreibungen sehr präzise formuliert werden. Häufig unterschieden sich Körperhaltung, Farben, Hintergrund oder Bildaufbau zwischen den einzelnen Bildern, obwohl dieselbe Übung dargestellt werden sollte. Deshalb waren mehrere Anpassungen und Überarbeitungen notwendig, bis ein einheitlicher und verständlicher Stil erreicht werden konnte.

Technische Entscheidungen

Wir entschieden uns bewusst für Streamlit, weil damit schnell interaktive Anwendungen entwickelt werden können.

CSV-Dateien wurden statt einer Datenbank verwendet, da:

die Anwendung dadurch einfacher bleibt,
keine externe Datenbank benötigt wird,
und die Daten lokal beziehungsweise über WebDAV gespeichert werden können.

Die Aufteilung in mehrere Seiten war ebenfalls eine wichtige Entscheidung, damit die App übersichtlich bleibt.

Zusätzlich entschieden wir uns für eine strukturierte Übungsdatenbank mit Bildern, Beschreibungen und Tipps, damit die Trainingsansicht dynamisch erweitert werden kann.

Zusammenarbeit im Team

Die Arbeit im Team funktionierte insgesamt gut.

Wir tauschten Ideen aus, testeten Funktionen gegenseitig und halfen uns bei Problemen. Besonders wichtig war die Kommunikation bei Fehlern und beim Zusammenführen der verschiedenen Funktionen.

Auch Nutzerfeedback spielte eine wichtige Rolle. Nach ersten Rückmeldungen erweiterten wir die App um Übungsbilder, Erklärungen und eine bessere Auswahl zwischen Home- und Gym-Training.

Die Aufgaben wurden untereinander verteilt, beispielsweise:

Dashboard,
Trainingsbereich,
Dokumentation,
Analysefunktionen,
oder Gestaltung der Übungsbilder.

Dadurch konnten wir effizienter arbeiten.

Was wir gelernt haben

Durch dieses Projekt konnten wir unser Wissen in Python deutlich erweitern.

Wir lernten unter anderem:

mit pandas Daten auszuwerten,
interaktive Streamlit-Apps zu entwickeln,
GitHub zu verwenden,
Dateien automatisch zu speichern,
Diagramme zu erstellen,
Bilder und dynamische Inhalte einzubinden,
und Fehler systematisch zu beheben.

Zusätzlich verbesserten wir unser Verständnis für:

Benutzerfreundlichkeit,
Strukturierung von Code,
Planung grösserer Anwendungen,
sowie die Verarbeitung und Darstellung von Daten.
Verbesserungsmöglichkeiten

In Zukunft könnte die App noch erweitert werden.

Mögliche Verbesserungen wären:

Login-System mit Benutzerkonten,
echte Datenbank statt CSV-Dateien,
Kalorientracker über mehrere Tage,
genauere Ernährungsanalysen,
Fortschrittsgrafiken mit mehr Optionen,
Suchfunktion für Übungen,
oder Trainingsvideos zu Übungen.

Auch die Benutzeroberfläche könnte zukünftig weiter optimiert und für mobile Geräte erweitert werden.

Fazit

Insgesamt war das Projekt eine sehr wertvolle Erfahrung.

Wir konnten theoretisches Wissen praktisch anwenden und lernten, wie viel Planung, Testen und Problemlösung hinter einer funktionierenden Anwendung steckt.

Besonders spannend war es zu sehen, wie aus einer einfachen Idee Schritt für Schritt eine vollständige Fitness- und Ernährungs-App entstand.

Durch zusätzliche Funktionen wie Übungsbilder, Trainingsanalysen und personalisierte Trainingspläne wurde die Anwendung im Verlauf des Projekts immer benutzerfreundlicher und realistischer.

Das Projekt half uns nicht nur unsere Programmierkenntnisse zu verbessern, sondern auch unsere Fähigkeiten in Teamarbeit, Problemlösung und Projektorganisation weiterzuentwickeln.