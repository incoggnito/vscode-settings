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

Handbuch (Alt): P:\B\BGP\9_Methodenentwicklung\08_Software-Programmierung\Datenbank\02_Versuchsdatenbank

APP: P:\B\BGP\9_Methodenentwicklung\08_Software-Programmierung\Datenbank\Beantragung_AppID

</div>

---

### Grundfunktionen der NVHBrake

---

Powerpint Bildschirmaufnahme
Bugfix
Neue Funktion

---

<!-- _class: left  -->

### NVHBrake Database

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

1. Senior Python Dev -> Styleguide und Integration ins produktive System
2. Laie und Ingeniuere aus dem Fachbereich -> Testen und Entwicklen von Prototypen an einem Tag

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

:arrow_forward: **Was nicht gut genug ist, kommt nicht ins GIT** :no_entry:

</div>

---

### SQL Datenmodell

<!-- _class: left  -->

OOP Einstieg mit Beispiel
- Alebmic ...


---

### Beispiel UML



---

![width:1100px](img/UML1.svg)

---

![width:1200px](img/UML2.svg)


---

![width:850px](img/UML3.svg)

---
### REST-Schnittschnelle

- Swagger GUI
- Endpoints

---

<!-- _class: left  -->

![bg opacity:0.3](img/bg.png)

### Python Webframeworks

<div class="row">

<div class="column-6">

## FastAPI
+ unordered list 2
    + nested item 1
    + nested item 2

</div>

<div class="column-6">

## Django
1. ordered list 1
2. ordered list 2
    1. nested item 1
    2. nested item 2

</div>
</div>

---

### Beispiel BI-Berechnung

Schematische Darstellung
Bereitstellung Code

---

![width:850px](img/UML3.svg)

---

```python
class BrakeStopCalcSI:
    Si: int = 0
    def calc_BI(self, brake_stop:BrakeStop) -> int:
      # ...
      return self.si

class CycleCalcBI:
    BI_H: int = 0
    BI_L: int = 0

    def calc_BI(self, l_brake_stops: List) -> int:
        # ...
        return self.BI_L, self.BI_H

class TestRunBI:
    BI: int = 0

    def calc_BI(self, cycles: Dict) -> int:
        # ...
        return self.BI

```

---

```python
class BrakeStop:
    Si: int = 0
    def calc_BI(self, bs_bi_calculator: BrakeStopCalcSI):
        self.Si = bs_bi_calculator.calc_BI()

class TestCycle:

    BI_L: int = 0
    BI_H: int = 0

    def calc_BI(
        self, bs_bi_calculator: BrakeStopCalcSI, 
        cc_bi_calculator: CycleCalcBI
    ):
        self.BI_L, self.BI_H = cc_bi_calculator.calc_BI()

```

---

```python
class BrakeNoiseTestRun:
    BI: int = 0

    def calc_BI(
        self,
        bs_bi_calculator: BrakeStopCalcSI,
        cc_bi_calculator: CycleCalcBI,
        tr_bi_calculator: TestRunBI,
    ):
        self.BI = tr_bi_calculator.calc_BI()

```