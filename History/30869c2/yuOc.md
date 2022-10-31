---
marp: true
theme: custom
size: 16:9
paginate: true
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
footer: 'Andreas Hofer, den 15.09.2022'
---
<!-- _footer: "" -->

![width:150px](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/BMW_logo_%28gray%29.svg/600px-BMW_logo_%28gray%29.svg.png) ![width:300px](img/Amitronics.svg)

## NVHBrake Next

Full Stack Webdevelopment

<span style='font-size: 18px'>created by [@Andreas Hofer](https://github.com/incoggnito) </span>

---

<!-- _class: left  -->

### NVHBrake

<div class="text-xs">

Ausgangssiutation der aktuellen Anwendung

</div>

![](img/nvhbrake.svg)

<div class="text-xxs">

_Wiki: https://atc.bmwgroup.net/confluence/display/NVHBRAKE/%5BProduct%5D+Homepage_

Handbuch (Veraltet): P:\B\BGP\9_Methodenentwicklung\08_Software-Programmierung\Datenbank\02_Versuchsdatenbank

APPID: P:\B\BGP\9_Methodenentwicklung\08_Software-Programmierung\Datenbank\Beantragung_AppID

</div>

---

### Grundfunktionen NVHBrake

<div class="row">

<div class="column-30">

### Planung

- Prüfstands-tagesplanung
- Langzeitplanung
- Komponentenbeschaffung
- Verantwortlichkeiten
- Versuchsprogramme
- Bremsprojekte

</div>

<div class="column-30">

### Versuche

- Komponent-datenenerfassung
- Versuchshistorie
- Versuchsvergleich
- Ablageorte der Rohdaten
- Erzeugung der Excel-Auswertung
- Upload NVHCockpit

</div>

<div class="column-30">

### Achsen / KRP

- Fahrzeugnummer
- Achsnummer
- Montagezustände
- Achsversand

</div>

</div>

---

### NVHBrake MS-Access Frontend

<!-- _class: left -->

<div class="text-xs">
Die Grundstruktur einer MS-Access Anwendung lässt sich wie folgt zusammenfassen:

</div>

<div class = "m-1"></div>

<div class="text-xs">

- Tabellen, als Datenquelle mit einem SQL-Server verlinkt oder lokal
- Abfragen oder Views um die Daten zusammenzuführen
- Formulare zur Darstellung der Daten und der Funktionen
- VBA Quellcode Module zur Verknüpfung mit Formularkomponenten

</div>

---

<div class="text-xs">

### Neue Schaltfläche hinzufügen

<div class="text-xs">
Das Frontend der NVHBrake App wurde mit Microsoft Access erstellt.

</div>

<div class = "m-2"></div>

<div>

<video width="900" controls>
  <source src="img/NeuFunktion.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

</div>

---

<!-- _class: center -->

<div class="text-xs">

### Debug-Modus

<div>

<video width="900" controls>
  <source src="img/Debug.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

</div>

---

<!-- _class: left  -->

### NVHBrake SQL-Database Backend

<div class="text-xs">

Kerntabellen der SQL-Datenbank (3.Normalform)

</div>


![width:1200px](img/DatenbankBase.png)

---

### NVHBrake Next

<!-- _class: left  -->

<div class="row">

<div class="column-70">

![](img/nvhbrakenext.svg)

</div>

<div class="column-30">

- CAE-Bench Datenspeicher ersetzbar
- Lokale, schnelle Frontendentwicklung
- Logik-Entwicklung im Fachbereich
- Definierte Schnittstelle zum WebFrontend
- Nachhaltige Dokumentation

</div>
</div>

---

### Der Weg zum Ziel, oder das Wie:grey_question::grey_question:

<!-- _class: left  -->

<div class="text-s">

- Übersetzung gewachsener VBA-Tools in python Klassen und Rest-Endpoints
- Übergreifende Datenanalyse in der Cloud :mag::cloud:
- Programmierung mit aktuellem Qulitätsstandard und Messung
- Aufgabentrennung:
  - Flexible Backend-Entwicklung der Logiken im Fachbereich
  - Nachhaltige Frontend-Entwicklung durch externe Partner
- Quelloffenes GIT-Repository

</div>

---

### Entwicklungspremisse

<!-- _class: left  -->

<div class="row">

<div class="column-50">

### Senior Developer (BMW/AMI)

- Umsetzung Style Guide und Richtlinien
- Verwaltung des Git-Master-Branch
- Definition der Entwicklungsziele
- Erstellung der Testinfrastruktur
- Ansprechpartner für die Verwendung der Bibliotheken
- Integration in die Produktivumgebung

</div>

<div class="column-50">

### DevOps/ Juniors / Anwender

- Verwendung der Bibliotheken
- Dokumentation der Teilaspekte
- Anfrage von Pull-Requests beim Senior

</div>

</div>
<div class = "m-2"></div>

:arrow_forward: **Trennung Anwender und Kernentwickler**

---
### Style Guide und Richtlinien:exclamation:

<!-- _class: left  -->

<div class="text-s">

Python ist __die__ Programmiersprache im Backend!
Damit alle die selbe Sprache sprechen gibt es z.B. __PEP 8__
Solche Standards lassen sich prüfen:

- Linting _(Prüft Syntax_Fehler, PEP-Standard, Best practices)_
- Static Typing _(Datentypen, I/O Funktionen, Klassen)_
- Autoformatting _(Zeilenlänge, Leerzeilen, )_
- Helfer für Komplexitätsmaße, Sicherheit, Lizenzen
- Autodokumentation _(Docstrings und Readme im Web)_

<div class = "m-2"></div>

:arrow_forward: **Was nicht gut genug ist, kommt nicht ins GIT** :no_entry:

</div>

---

### SQL Datenmodell als UML

<!-- _class: left  -->

<div class="text-xs">
Abstraktion der bestehenden Datentabellen, zur Beschreibung der Prozesse im Umfeld der Bremsgeräuschentwicklung.
</div>

<div class = "m-1"></div>

<div class="text-xs">
Ein Klassendiagramm ist ein UML-Diagrammtyp, der ein System beschreibt, indem er die verschiedenen Objekttypen innerhalb eines Systems und die Arten der statischen Beziehungen, die zwischen ihnen bestehen, visualisiert. Sie veranschaulicht auch die Operationen und Attribute der Klassen.
</div>

---

<div class="text-xs">

Tabellenklassen vom SQL-Server:


</div>

![width:1100px](img/UML1.svg)


---

<!-- _class: left  -->

<div class="row">

<div class="column-50">

<div class="text-l">

Datenmodell zur BI-Berechnung:

</div>


</div>

<div class="column-50">

![width:500px](img/UML2.svg)

</div>
</div>


---

### Datenmodell zur BI-Berechnung

Schematische Darstellung


---

<div class="text-s">

Klassen zur Beschreibung einer EET-Datei


</div>
<!-- _class: right  -->

<div class="row">

<div class="column-30">

![width:250px](img/UML3.svg)


</div>

<div style="float: left;width: 70%;font-size: 12px">

- BrakeNoiseTestRun: beschreibt ein Testprogramm(GP01 oder GP02) und entspricht eine komplette EET-Datei
  - cycles: ein Dictionary von normalerweise sieben Lastkollektiven mit int von 1-7 als Keys.
  - calc_BI(): berechnet den BI-Wert eines Testprogrammes
    - TestRunBICalc: eine abstrakte Klasse als Input, deren Kindklassen unterschiedliche BI-Berechnungsverfahren eines kompletten Testprogrammes definiert.

<br/><br/>
- TestCycle: beschreibt eine Lastkollektive
  - brake_stops: eine Liste von BrakeStop-Objekts, aus denen eine Lastkollektive besteht.
  - calc_BI(): berechnet den BI-Wert einer Lastkollektive
    - CycleBICalc: eine abstrakte Klasse als Input, deren Kindklassen unterschiedliche BI-Berechnungsverfahren einer Lastkollektive definiert.

<br/><br/><br/><br/>
- BrakeStop: beschreibt eine Bremsung und entspricht eine Zeile der EET-Datei
  - calc_Si(): berechnet den Si-Wert einer Bremsung
    - BrakeStopSiCalc: eine abstrakte Klasse als Input, deren Kindklassen unterschiedliche Si-Berechnungsverfahren einer Bremsung definiert.

<br/><br/><br/><br/><br/><br/>
- Noise: beschreibt ein Geräusch von einer Bremsung




</div>
</div>


---

<div class="text-s">

### BI-Berechnung in Analysator Klasse


</div>

![width:1200px](img/BIRechner.png)

---

### Der Versuchszyklus

![width:900px](img/TestCycle.svg)

<div class="text-xs">

Jedes Lastkollektiv wird durch eine Vererbung von **TestCycle** beschrieben.

</div>


---

</div>
<span style="text-align: left;font-size:20px">
Cycle, EETName, SequCycle, tblBrakeStop, Dir und Test entsprechen der Tabellenstruktur in SQL-Server<Br/><Br/>
EETDataReader greifen die Daten vom SQL-Server ab und konvertieren sie zu den Klassen des BI-Berechnungsdatenmodells
</span>
</div>

---


### REST-Schnittschnelle

- Swagger GUI
- Endpoints

---

<!-- _class: left  -->

![bg opacity:0.3](img/bg.png)

### Python Webframeworks

<div class="row">

<div class="column-50">

## FastAPI
+ unordered list 2
    + nested item 1
    + nested item 2

</div>

<div class="column-50">

## Django
1. 