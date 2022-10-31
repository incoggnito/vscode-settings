---
breaks: true
title: INTEUM 1. Zwischenbericht
tags: Inteum, Zwischenbericht
robots: noindex, nofollow
lang: de
date: 2022-10-11

---

## Einleitung

## Wiss. tech. Ergebnisse

### Anforderungen

:::info
schriftliche Spezifikation als FlowChart:
-> Was muss passieren, damit Acoustic Emission anwendbar ist?
Beispiel am konkreten Einsatzfall
Review bzgl. Stand der Technik
:::

#### Produkt

- Allg. Generelle Produktqulität an industriellen Fertigungsanlagen
- Allg. Einsetzbarkeit von Acoustic Emission Sensoren
- Erkennen von Störungen (Impulshaftig, Kontinuierlich)
- Qualitätskennwerte von Scherdel:
  - geometrische Kennwerte (Performance Indices, von ihrer Kamera): nio_rad, nio_ang
  - weitere Kennwerte (Funktionstest, ...)

#### Werkzeug

- Werkzeugverschleiss <-> Acoustic Emission
- Typische Auswerteverfahren und Features, die im Einsatz sind
- Kennwerte des eingesetzten Werkzeugs: Laufzeit, Counter des Werkzeugeinsatzes oder Tausch bei Ausfall, Produkt N.i.o (Zähler, wie viele n.i.o Teile, hat dieses Werkzeug produziert)

#### Testumgebung

Anforderungen an die Maschinen aus Sicht der AE

- erster Test HQ-Maschine weil langsamer als Einstieg -> Perfomancetest Massenfertigung (höhere Echtzeitanforderung da kürzere Taktzeit)
- Schematische Darstellung des Produktionsablaufs (Diagramm)
- Ermittlung konkreter Störgrößen (Produktionsfehler, Werkzeugverschleiss)
- Verwendete Messtechnik (Kamera, Kistler, AE-Sensoren, Sensor-Beacons)
- Laufender Prozess oder provozierte Fehler

#### Definition Demonstrator

- Echtzeitanforderungen festlegen (Rechenzeiten, ...)
- Zugriff auf Daten, Visualisierung der Ergebnisse
- Ausfallsicherheit und Fehlererkennungsrate
- Modularisierungsgrad -> Updatefähigkeit (wie aufwendig, wie zeitaufwändig)
- Zustandsüberwachung auf Basis von Messdaten
- Abgleich unser Zustandsüberwachungsergebniss mit dem der Inline-Qualitätskontrolle von Scherdel
  - Werte für die Übereinstimmung

#### Rollen und Rechte

- Review Trennung IOT-Device (Updates, externe Cloud...)
- Review Gewährleistung der IT-Sicherheit
- Datenbedarfe (aus unserer Sicht: Zeitrohdaten aus Messungen, Messingenieur: Zeitrohdaten, unsere Features, Qualitätsbeurteilung von Scherdel,)
- Rollen (Ext-Messing, Ext-AI-Spezialist, Ext-Projekt, Ext-IT)

#### Evaluierung der Ergebnisse

- Review Arten der Evaluierung
- Funktionstest, Integrationstest
- Festlegung von Scores
- Am Beispiel Stanzen und Ultraschall

### Rapid Protyping

#### Entwurf Hard- und Softwarearchitektur

- Schnittstellenidentifikation (MQTT, CSV, ...) und Aufwandsabschätzung
- Konvention -> Datenformat zur Weiterverarbeitung
- Prototyp Docker (MQTT)
- Trennung der Netzwerke und der Aufgabenbereiche
- Rechenoperationen auf Basis der Zugriffsrechte
- Zusammenführung der Daten durch Abgleich der Zeitstempel (siehe Härtl)
- Integration der Hardware -> Zusammenstellung der Hardware

#### Analyse Sensorpositionierung für Ortung

- Review zur Ortung generell und durch Autoencoder
- generelle Untersuchung anhand des Bauraums der Maschine, wo Sensoren appliziert werden können
- zwei Sensorpositionen (diagonal in einer Ebene)

#### Methode zur Speicherung der Daten

- Review zu Datenbanken für Zeitreihen
- Berechnung der Features und Speicherung bei SCH
- Flexibles Austauschformat (Json)

### Entwicklungsplattform

- VPN Zugriff für unsere Entwicklung
- Eigener Netzwerkbereich für den Remote Zugriff von Konsortialpartnern
- Proxmox und Docker Maschinen -> Virtualisierung LXC
- Getrennte Plattformen zur Entwicklung
- lokaler Zugriff MQTT, bzw CSV

#### Überführung prototypischer Architektur

- Testmessungen an weiterer Maschine
- Beispiel aus AP1 und AP2 mit neuem UseCase Ultraschallschweißen
- Aufzeigen der Unterschiede und der weiteren Entwicklungsaufwände

### Architektur und Design

#### Systemarchitektur

- Darstellung der Bausteine und Schnittstellen
- Auswahl und Dimensionierung der Bausteine

![](https://hedgedoc.amitronics.net/uploads/178341ce-a9c7-438c-822d-109e5e570b0b.png)

#### Systemdesign

- Daten und Informationsfluss
- Darstellung der Datenbedarfe und Verantwortung
- Verfügbarkeitsbewertung des Gesamtsystems
  - Herausgabe der Featurematrix
  - Skalierung
  - Features -> Komplexität beim Messdienstleister (Ordnung: log/lin)

#### Referenzmodell

- hoher Abstraktionsgrad des Modells aus Systemdesign und Architektur

![](<https://hedgedoc.amitronics.net/uploads/a472febc-c44b-4279-b275-ac90b50bfe2d.png> =300x400)

### Komponentenentwicklung

#### Signalverarbeitung und Features

- Review visuelles Feature-Engineering
- Grundsätzliche Vorgehensweise und exemplarisches Beispiel
- Datenvorverarbeitung:
  - Prozess- und Taktzerlegung
  - Skalierung der Features
  - Featureauswahl

#### Blinde Quellentrennung

- Recherche Stand und konzeptionelle Vorgehensweise

#### Lokalisierung SEO

- Recherche Stand und konzeptionelle Vorgehensweise

#### Steuerungs- und Kommunikationskomponenten

->Diskussion

#### Logging Schnittstelle

- Recherche
- Konzept für Logging Sammelstelle
- Herausgabe von Log-Files (Loguru, Prometheus, Grafana)
