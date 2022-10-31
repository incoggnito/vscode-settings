## Einleitung

Aufgrund der stark instationären Eigenschaften des AE-Signals beim Laserstrahl-Auftragschweißen, das sich in der Regel aus mehreren Komponenten zusammensetzt (z. B. Umgebungsgeräusche, aperiodische Impulse und andere externe Signale), sind herkömmliche Methoden zur Lokalisierung von AE-Quellen in plattenförmigen Strukturen mit komplexen geometrischen Merkmalen, wie z. B. beim Laserstrahl-Auftragschweißen, im Allgemeinen schwierig zu lokalisieren und zu charakterisieren. [@liAcousticEmissionSources2022]

Beim EHLA-Verfahren werden die Pulverpartikel des Beschichtungswerkstoffes direkt im Laserstrahl aufgeschmolzen und nicht erst im Schmelzbad auf der Oberfläche des Bauteils. Da so flüssige Materialtropfen statt feste Pulverpartikel in das Schmelzbad gelangen, kann die Prozessgeschwindigkeit von bisher 0,5 bis 2 Metern pro Minute beim herkömmlichen Laserauftragschweißen um mehrere Größenordnungen auf bis zu 500 Meter pro Minute gesteigert werden. [@BremsscheibenEffektivSchuetzen, @BeschichtungBremsscheibenMittels] Aufgrund der hohen Bearbeitungsgeschwindigkeiten wird die Anforderung an die Messtechnik und die Auswertung nochmals gesteigert.

Zur effizienten Integration unserer Messhardware in Ihre Fertigungsanlagen bieten wir folgende Teilschritte in einem exemplarischen Zeithorizont an:

* First-Shot-Analyse (1 Tag)
* The-Long-Run (im Anschluss, x-Wochen)
* Als Produkt (Integration der Softwaremodule 3-6 Monate)

## First-Shot-Analyse

![Schematischer Aufbau zur Acoustic-Emission Messung \\label{ae}](images/acoustic_emission.png){ width=60mm height=30mm }

Unsere Zustandsüberwachung von Maschinen und unsere Qualitätssicherung der Produkte basiert auf Acoustic Emission Messungen. Mit diesem Messverfahren werden transiente, elastische Wellen in Festkörpern festgestellt. Die Wellen werden durch plastische Deformation, Rissausbreitung, Korrosion oder einen Stoß verursacht. Der verwendete Messbereich reicht von 20 kHz bis zu 2 MHz. [@vallenSchallemissionsprufung2003] Aufgrund des sehr hochfrequenten Messbereich ist der Einfluss von Umgebungsgeräuschen reduziert.
Wir betreiben unsere Produktentwicklung mit Fokus auf Acoustic Emission \\ref{ae} seit einigen Jahren auf Basis verschiedener forschungsgetriebener Anwendungsfälle aus dem Industrieumfeld, hier ein Überblick:

* Detektion und Ortung von Nadelbrüchen bei der Textilvliesfertigung
* Überwachung von Lagerkomponenten in speziellen Elektromaschinen
* Erkennung von Prozessabweichungen beim Laserstrahlschweißen
* Detektion von Verschleiß und singulären Events beim Drahtzug
* Analysen im Bereich von Spritzgussmaschinen
* Untersuchungen im Hinblick auf Ultraschallschweißen und Hochgeschwindigkeitsstanzen

Zur Prüfung der Anwendbarkeit der AE-Messtechnik beim EHLA-Verfahren bietet sich zum Einstieg unsere First-Shot-Analyse an, diese umfasst folgende Teilschritte:

* Erste Abstimmungen zu den technischen Randbedingungen und Möglichkeiten zur Montage der Sensortechnik
* Anbringung ausgewählter AE-Sensoren am Laserkopf und an nicht rotierenden Teilen der Maschine (in bisherigen Anwendungsfällen lag eine ausreichend hohe Signalqualität über Lagerungsschnittstellen vor)
* Auswahl des Messsystems und der Sensoren, sowie der Messeinstellungen
* Dokumentation anhand des Messplans, inkl. Fotos
* Kalibriermessung mittels einer HSU-Nielsen-Schallquelle, Ruhemessung und Betriebsmessungen im Normalzustand
* Abstimmung mit Maschinenbedienern und Entwicklern zu bekannten Störungen, welche beim EHLA-Verfahren möglich sind
* Erste Messungen möglicher Störungen im Betrieb

![Live-Darstellung der Zeitrohdaten im Wasserfall \\label{waterfall}](images/waterfall.png){ width=60mm height=60mm }

* Schneller Einstieg durch Live-Analysen (z.B.: durch ein Echtzeit Wasserfall-Spektrogramm, siehe Abb. \\ref{waterfall}) und Abgleich provozierter Störungen mit dem Normalzustand
* Erkennung von impulshaften Geräuschen durch den integrierten Hit-Processor
* Anwendung unserer automatisierten Prozesstakterkennung und Zerlegung
* Erste Varianzuntersuchungen unterschiedlicher Chargen bzw. Materialzusammensetzung von Bremsscheiben oder Beschichtungspulver
* Darstellung ausgewählter Features und der Zeitrohdaten in hochauflösenden Wasserfalldiagrammen und Spektrogrammen in Echtzeit
* Abschlussbericht mit einer Zusammenfassung aller Ergebnisse

**Ergebnis:** Ein umfangreicher erster Einblick in die erfassbaren Schwingungen und eine Abschätzung zur Erkennung von Abweichungen und Störungen.

Unser unverbindliches Angebot für diese Einstiegsanalyse liegt bei 2560 € exklusive der Anreisekosten. Der maximale Leistungsumfang liegt hier bei 10 Stunden durch unsere beiden Experten im Bereich akustischer Messung und Auswertung. Für komplexere Anwendungsfälle, wie dem Laserauftragschweißen, ist zur Entwicklung der Features und der Detektionsmodelle eine höhere Datenbasis und damit ein längerer Überwachungszeitraum notwendig.

## The-Long-Run

![Prototyping-Entwicklungsumgebung im Hardcase \\label{koffer}](images/Messkoffer.png){ width=100mm height=60mm }

Für die Durchführung von automatisierten Analysen im Dauerlauf bieten wir unsere Prototyping-Entwicklungsumgebung an, siehe Abb. \\ref{koffer}. Diese eignet sich für die Auswahl und Anpassung von Features, Entwicklung und Training von Machine Learning Modellen oder zur Messung und Erkennung sporadischer Abweichungen, welche nicht innerhalb weniger Stunden erfasst werden können. Im Anschluss an die First-Shot-Analyse kann das Condition Monitoring System direkt vor Ort installiert werden. Dafür ist lediglich eine Ethernet-Anbindung mit Internetzugriff oder die Verfügbarkeit von Mobilfunk notwendig. Unser Basispaket beinhaltet folgende Leistungen:

* Montage notwendiger Komponenten (Messsystem, UMTS-Router, Netzwerkrouter, Stromversorgung, Industrie-PC, Sensoren) im Hardcase
* Unterstützung bei der Integration in das Kundennetzwerk
* Kontrolle und Sicherstellung der Datenaufzeichnung durch unsere Cloud
* Die Entwicklung eines spezifischen Featurescores für die Detektion einer ausgewählten Störung unabhängig von Maschineninformationen
* Auswahl der besten Feature und Bewertung der Qualität der Features
* Die komprimierte, anonymisierte und skalierte Bereitstellung von Features innerhalb eines abgetrennten Netzwerkbereichs via MQTT, OPCUA oder REST
* Möglichkeit zur Nachauswertung nach Änderungen am Auswertedesign oder den Features auf Basis gesicherter, komprimierter Zeitrohdaten in unserer Cloud (Verwendung eines intelligenten Datensammlers)
* Klassifizierung erkannter Störungen
* Wöchentliche Bereitstellung einer Zusammenfassung in Berichtsform

**Ergebnis:** Kontinuierliche Ausgabe der Features und der Label in Echtzeit im lokalen Netzwerk oder gebündelt zum Download

Die Bereitstellung unseres Basispakets startet mit wöchentlichen Kosten von 1120 €. Einer unserer AI-Spezialisten unterstützt einen Tag pro Woche die Entwicklung des spezifischen Featurescores und überwacht die Detektion der Ereignisse. Die entwickelten Modelle zur Detektion werden nach dem Entwicklungszyklus in das Produkt implementiert.

## In-Product

![High-End Acoustic Emission Messsystem \\label{system}](images/Fyrsonic_ohne_Logo.png){ width=40mm height=20mm }

Nach dem Long-Run können die Messsysteme entsprechend der notwendigen Konfiguration angeboten werden. Die Softwaremodule können durch unsere Virtualisierungslösung einfach ausgerollt und erweitert werden.

In Abbildung \\ref{system} wird unser High-End Acoustic Emission Messsystem dargestellt, dieses bietet die einfachste Maschinenintegration im kleinsten, geschützten Gehäuse. Abhängig vom Rechenaufwand und der notwendigen Abtastrate kann allerdings zusätzlich ein Industrie-PC notwendig werden.

Bei der Pro-Variante ist dieser systembedingt immer notwendig, hier ist eine deutlich schwächere Soundkarte (Abtastrate und Messbereich) als USB-Device im Einsatz.

Unsere Custom-Variante bietet sich als Sonderlösung für den sehr flexiblen Einsatzbereich an. Der Preis für das System dürfte hier abhängig von der Konfiguration zwischen der Pro und der High-End-Variante liegen und kann auf konkrete Anfrage kalkuliert werden.

Der folgenden Tabelle \\ref{tab:systems} kann eine grobe Kostenaufschlüsselung für unterschiedliche Varianten entnommen werden:

### Systeme (Offline-Variante, ohne Sensoren und Zubehör)

| | Messysteme | | 1 St. | 5 St. | EK 50 St. | EK 150 St. | |--|-----------|--|----------|----------|-----------|------------|----| | 1 | High-End AE-System| VAM-2HQ | 10.464,00 € | 9.526,00 € | 8.523,00 € | 7.673,00 € | | 2 | Pro AE-System | VAM-4Pro | 3.429,00 € | 3.206,00 €| 2.858,00 €| 2.734,00 €| | 3 | Custom AE-System | VAM-4C | \~ 6.000,00 € | - | - | - | Table: Preisabschätzung für unsere Messsystemvarianten \\label{tab:systems}

Zukünftig können Leistungen aus dem Long-Run einzeln als Services zu den Messsystemen hinzugebucht werden. Preis auf Anfrage.

## Literaturverzeichnis