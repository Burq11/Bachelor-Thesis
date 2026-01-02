# CNC Sensor Data Platform (DuckDB + API)

Dieses Projekt entwickelt ein modulares System zur Verarbeitung und Bereitstellung von **Sensordaten aus CNC-Fräsmaschinen**.

Ziel ist es, große Mengen an Maschinen- und Sensordaten effizient aufzubereiten, zentral zu speichern und für Analysen kontrolliert bereitzustellen.

---

##Projektidee

Das System besteht aus drei klar getrennten Schichten:

1. **Datenaufbereitung (nicht Teil dieses Repositories, separat umgesetzt)**
   - Rohdaten aus CNC-Maschinen (HighFrequency-, LowFrequency- und Sensorsignale)
   - Bereinigung, Vereinheitlichung und Anreicherung der Daten
   - Vorbereitung für Analyse und Visualisierung

2. **Datenspeicherung(nicht Teil dieses Repositories, separat umgesetzt)**
   - Speicherung der aufbereiteten Daten in einer **DuckDB-Datenbank**
   - Optimiert für große, tabellarische Zeitreihendaten
   - Einheitliches Schema für reproduzierbare Analysen

3. **Datenzugriff (API-Maske)**
   - Zugriff auf die Daten über eine **Python-basierte REST-API**
   - Daten werden effizient an Clients ausgeliefert

---

## Nutzung

- Die API läuft auf einem Server mit Zugriff auf die DuckDB-Datenbank
- Analyse-Notebooks greifen per HTTP-Requests auf die API zu
- Die Notebooks erhalten die Daten als Pandas DataFrames für:
  - Visualisierung
  - Feature Engineering
  - Modellierung (Chatter Detection)

---

## Motivation

- Trennung von **Datenhaltung** und **Analyse**
- Skalierbarer Zugriff auf große Sensordaten
- Einheitliche Datenbasis für mehrere Nutzer
- Reproduzierbare Forschung und Experimente

---

## Status

Work in progress  
Das Projekt entsteht im Rahmen einer Bachelorarbeit und wird schrittweise erweitert.

---

![DataFlow](https://github.com/user-attachments/assets/c9b18885-4af8-415f-91d5-f3a6ecdeb356)


