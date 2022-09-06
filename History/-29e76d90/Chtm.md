## Einleitung

Ein Hindernis für den Technologie- und Erkenntnistransfer der PM-Forschung aus Produktionskontexten ist zum einen in der unzureichenden Adaption bisheriger Verfahren der Künstlichen Intelligenz (KI) an die vorhandene Datenbasis zu finden. Zum anderen haben sich aufgrund der Neuartigkeit des Betrachtungsfeldes und des damit verbundenen niedrigen Technologiestandes industrielle Normen und Standardisierungen noch nicht ausreichend etablieren können, um bestehende KI-Verfahren mit geringem Aufwand und Risiko anwendbar zu machen.

Aus dieser Forschungslücke leitet sich das Gesamtziel des Vorhabens ab: Eine Reduzierung von Kosten und Zeit zur Erstellung einer PM-Lösung für Fahrzeugkomponenten unter Einhaltung der Qualitätsstandards.

Die Amitronics GmbH (AMI) möchte die Projektergebnisse nutzen, um ihr Dienstleistungsportfolio an strukturdynamischen und akustischen Messdienstleistungen entscheidend in Richtung KI zu erweitern. Dies soll in mehreren Schritten erfolgen. In einem ersten Schritt sollen insbesondere die bei AMI vorhandenen kommerziellen Mess- und Analysetechniken und -systeme, darunter das mit einem Partner entwickelte Vibroakustische Condition Monitoring System (VAM) für körperschallbasierte Ereignisse an Maschinenstrukturen, in einem breiteren Rahmen für die Themen rund um PM im Automobil nutzbar gemacht werden. Angedacht ist hier, die im Vorhaben entwickelten Cloudlösungen (AP4) für die Aus- und Bewertung der mit unserer Messtechnik erzielten Ergebnisse zu nutzen. Dadurch soll einerseits die Effizienz unserer Messdienstleistungen erhöht und andererseits die Aussagekraft der Ergebnisse dahingehend erweitert werden, dass mit Hilfe von Machine Learning Ansätzen neue, bisher nicht betrachtete Parameter und Abhängigkeiten, wie z.B. spezielle Transferfunktionen und Abhängigkeiten zwischen einzelnen Baugruppen und Komponenten, aber auch zwischen einzelnen Ergebnissen, bei der Ergebnisbewertung und bei der Ableitung von akustischen und strukturdynamischen Lösungsvorschlägen einfließen können.

Gerade hier sieht AMI ein hohes Potenzial für eine qualitativ verbesserte Ergebnisinterpretation bis hin zur Einbindung der Ergebnisse in die von den Partnern entwickelten Verschleißmodelle. Und gerade die Nutzung unserer Daten in Verschleißmodellen würde das Dienstleistungsangebot der AMI weiter ausbauen. Die AMI sieht ein hohes Verwertungspotenzial für ähnliche Aufgaben bei anderen Automobilherstellern, wie z.B. der BMW AG. Aufgrund der fahrzeugtechnischen Breite des Vorhabens (Fahrwerk, Getriebe, Elektronikkomponenten) ist auch hier eine entsprechende Breite an späteren Angeboten zu erwarten, von der Analyse des Planverschleißes bis hin zur Früherkennung von Riss- und Bruchereignissen.

Kurz- und mittelfristig werden hier Dienstleistungsgewerke für AMI von ca. 250T€ / Jahr erwartet, langfristig, insbesondere unter Einbeziehung von Fragestellungen aus der Elektromobilität, von 500 - 750 T€ / Jahr. Der Anwendungsbereich der neuen Dienstleistungen geht letztlich weit über den Automobilbau hinaus, wie es die Messdienstleistungen der AMI bereits tun. Zu nennen sind hier der Anlagen- und Maschinenbau sowie die Elektronik bis hin zum Bauwesen und zur Luftfahrt. Dabei liegen die Umsatzerwartungen in ähnlicher Höhe wie im Automobilbau. Darüber hinaus möchte die AMI ihr VAM fahrzeugtauglicher gestalten. Dies betrifft sowohl die Hardware in Bezug auf die Geometrie, einschließlich der Montage im Fahrzeug, als auch den Preis. Ebenfalls angepasst werden muss die Software (Abtastrate, Frequenzbereich, Cloudfähigkeit), um ein kleines, funktionales und fahrzeugtaugliches System nutzen zu können. Bei entsprechender Umsetzung (relevante fahrzeugtypische Parameter und kostenreduziert) ist auch ein permanenter Verbau des Systems im Fahrzeug zum Datenmanagement (Erfassung, Aus-, Bewertung und Bereitstellung) denkbar.

Die AMI strebt an, im Anschluss an das Projekt mehrere Systeme für Premium-Versuchsfahrzeuge bereitzustellen, um die Datenbasis beim Hersteller zu erhöhen und die Aussagekraft der fahrzeuginternen Sensorik gezielt zu validieren und ggf. zu erweitern. Die Umsetzung der Verwertung erfordert die Schaffung neuer, teilweise hochqualifizierter Arbeitsplätze und den Erhalt der derzeit vorhandenen.

## Wissenschaftlich-technische Ergebnisse und andere wesentliche Ereignisse

Die wesentlichen Ziele im Gesamtprojekt liegen in der Schaffung eines Baukastensystems zur schnelleren und effizienteren Entwicklung von Prädiktionsmodellen für Komponentenverschleiß und -ausfälle.

### AP-1 Anwendungsszenarien, Anforderungsanalyse und Systemspezifikation

#### Zielsetzung

Eindeutig definierte Anwendungsszenarien (Demonstrationsszenarien) und Indikatoren zur qualitativen und quantitativen Überwachung der Zielerfüllung sowie Anforderungen an Gesamt- und Teilsysteme.

#### Vorgehensweise Technische Akustik

Um eine möglichst modulare Herangehensweise zur Problembehandlung innerhalb eines Referenzmodells zu erzielen, wird zunächst die Ausgangsstellung analysiert.

Die Technische Akustik (kurz NVH - Noise, Vibration, Harshness) gehört meist zu den fünf wichtigsten Eigenschaften, die bei der Konstruktion eines Fahrzeugtyps Priorität haben. Aus Sicht der Technischen Akustik erfolgt im Rahmen der Fahrzeugentwicklung üblicherweise folgende Vorgehensweise [@moserTechnischeAkustik2015,@kollmannPraktischeMaschinenakustik2006, @moserMesstechnikAkustik2010]:

* Fahrzeugziele um den Kundenanspruch z.B. im Hinblick auf Fahrkomfort zu bedienen
* Umwandlung subjektiver, funktionaler Imageziele in objektive, technische Metriken
* Kaskadieren von Zielen auf Fahrzeugebene zu NVH-Zielen auf System- und Komponentenebene
* Schwachstellenanalyse durch messtechnische Analyse und Simulation von Teil- und Gesamtsystemen
* Unterscheidung des Schallträgers (Luft, Struktur)
* Erstellung von Bewertungsstrategien und Absicherung der Systeme
* Erforschung der Entstehungsursache und des Wirkmechanismus
* Maßnahmen erfolgen meist durch Dämpfung, Isolation oder Veränderung der Struktur

Störgeräusche mit einer Vielzahl an Abhängigkeiten können bisher nur durch aufwändige Iterationsschleifen abgesichert werden. Ein beliebtes Beispiel ist hier die Scheibenbremse, welche eine Vielzahl von äußeren Einflüssen, hohen Freiheitsgraden und Nichtlinearitäten aufweist. Das System kann sehr instabil und schwer abzusichern sein, da bereits kleine Änderungen im Produktionsablauf große Einflüsse auf das Geräuschverhalten haben können. Im Projekt sollen solche Anwendungsfälle ausgewählt werden, die eine hohe technische und wirtschaftliche Relevanz haben.

#### Auswahl der Use Cases

Die bisherige Auswahl der Use Cases Bremsgeräusch und Elektroantrieb auf Basis der Risikomatrix erweist sich im Zusammenhang mit der messtechnischen Erfassung als zu langwierig. Das liegt vor allem an Verfügbarkeiten von Komponenten und Fahrzeugen. Daher wird die Auswahl der Themen aus dem ersten Quartal erweitert. Es wird nach konkreten, akustischen Anwendungsfällen gesucht, um zügig zur hochauflösenden Messung am Testfahrzeug voranzuschreiten. Wie sich innerhalb der Datenanalyse zeigt, sind die gemessenen Daten zur Validierung und zum Erstellen von Modellen innerhalb der Flotte dringend notwendig.

In einer Netzwerkkampange mit unterschiedlichen NVH-Fachbereichen werden Verantwortliche der Gesamtfahrzeug-, Fahrwerks- und Bremsenakustik in das Projekt eingebunden. Damit kann eine umfassende Betrachtung globaler und lokaler akustischer Ereignisse sichergestellt und damit eine stabile Basis für den Baukasten aus Sicht der Fahrzeugakustik geschaffen werden. Außerdem erfolgen eine Reihe von Abstimmungen mit Fahrzeugverantwortlichen und Messtechnikausrüstern zur Vorbereitung der Fahrzeuge. Ziel ist es mit einer Messtechnikaufrüstung im Testfahrzeug langfristig möglichst viele Use-Cases bearbeiten zu können.

In den folgenden Teilabschnitten werden die neuen Use Cases aus Sicht der technischen Akustik kurz vorgestellt und der Stand der Technik zusammengefasst.

##### 3. Use Case "Radunwucht"

<!-- TODO Quellen und weitere Inhalte -->
Jedes an einem Kraftfahrzeug montierte Rad ist in gewisser Weise unwuchtbehaftet.
So zeichnen sich Fertigungstoleranzen, Material-Inhomogenität, über den Umfang ungleich verteilte Bauteile (z.B. Ventilsitz) oder auch Verschleiß dafür verantwortlich.
Bereits Unwuchten von 30g führen bei hohen Geschwindigkeiten zu Vibrationen am Lenkrad und reduzieren somit den Fahrkomfort. Die Auswertung erfolgt üblicherweise im Verhältnis zur Drehzahl am Rad in einer Ordnungsanalyse. Die Ordnungsanalyse ist ein weiterführendes Verfahren der Zeit-Frequenzanalyse an rotierenden Maschinen. Während bei einer herkömmlichen Spektralanalyse die einzelnen Fouriertransformierten in Wasserfall oder Farbkodierung über die Zeit dargestellt werden, wird bei der Ordnungsanalyse die Frequenzachse auf die aktuelle Drehzahl normiert. Damit hat man den Vorteil, dass bei steigender Drehzahl nicht die einzelnen drehzahlabhängigen Frequenzen proportional verschoben werden, sondern als konstante Vielfache der Grundschwingung, die „Ordnungen“ im Ordnungsspektrogramm entlang der Ordinate fix bleiben.

#### 4. Use Case "Sitzschiene"
<!-- TODO Quellen und weitere Inhalte -->
Sitzschwingungen werden üblicherweise durch analoge Beschleunigungssensoren an der Sitzschiene des Fahrersitzes gemessen. Die gemessenen Antwortsignale können nach einer Aufbereitung in einem Viertelfahrzeugmodell simuliert werden. Im Fahrzeug vorhandene Businformationen sollen zur Berechnung einer virtuellen Sitzschiene herangezogen werden und die analoge Messtechnik ersetzen. Für eine Fahrzeugbaureihe existiert bereits ein Modell zur Reproduktion der realer Fahrbedingungen am Simulator, dieses soll nun auf weitere Fahrzeugbaureihen ausgeweitet werden. Neben unterschiedlicher Anregungen durch die Fahrbahn soll eine Unwucht Anregung am Reifen als spezifischer Anregungsfall erkannt werden. Damit können Anforderungen aus unterschiedlichen Fachbereichen vereint werden. In Zukunft soll die Berechnung des virtuellen Sensorkanals direkt in der Cloud stattfinden. Dieser Anwendungsfall erlaubt in situ Nachstellung der Fahrsituation beim des Kunden.

### AP-2 Entwicklung des PANAMERA-Referenzmodells

#### Zielsetzung

Entwicklung des PANAMERA-Referenzmodells, bestehend aus einem Prozessmodell und einem PM–Baukasten und zur Evaluierung dienen einige ausgewählte Fahrzeugkomponenten.

#### NVH-Baukasten

Um einen effizienteren Prozessablauf und transparentere Schnittstellen müsste aus Sicht eines Akustikingenieurs (NVH-Experte) müssten die Prozesse im Fachbereich nicht wesentlich geändert werden. In der folgenden Abbildung XX wird eine solche Vorgehensweise exemplarisch darstellt und entsprechend erweitert.

![Erweiterung des NVH-Baukastens für eine Datenbereitstellung](images/Baukasten2.drawio.png){ width=160mm height=220mm }

Die Messdaten aus dem NVH-Umfeld stellen eine große Datenquelle innerhalb der Entwicklung eines Fahrzeugs dar. Zur Entwicklung des individuellen Markensounds und zur Unterdrückung von Störgeräuschen werden unzählige Tests in verschiedenen Fachabteilungen durchgeführt. Akustikingenieure sind an der Entwicklung und Absicherung der meisten Komponenten des Fahrzeugs beteiligt. Von Fahrbahn-, Rad-, Motorerregung, dem Fahrgeräusch und dem Sound Design finden sich sehr unterschiedliche Gründe für die akustische Datenerfassung am Fahrzeug. [@zeller_handbuch_2013]

Üblicherweise werden diese Use Cases unabhängig voneinander in einer Vielzahl spezifischer Projekte bearbeitet. Die Messdaten werden zwar in der Regel lokal abgelegt, sind allerdings nur selten für übergreifende Analysen nutzbar. Das liegt an fehlenden Zugriffsrechten, unterschiedlichen Datenformaten, unzureichender Datenbeschreibung oder zu spezifischen Randbedingungen. Große Datensammler sollen diese Herausforderung langfristig lösen. Dazu ist es notwendig, dass den Datenerzeugern aus den unterschiedlichen Fachbereichen die Schnittstellen bekannt sind und übergreifende Analysemöglichkeiten bekannt sind. Den Datenanalysten fehlen  zumeist nutzbaren Daten, daher werden oftmals separate Tests durchgeführt.

Bei fehlenden Daten im NVH-Bereich wird zu Beginn geprüft ob bereits ein Versuchsaufbau vorhanden ist. Bei fehlendem Testaufbau ist es meist notwendig den Anregungsmechanismus und die Wirkweise zu verstehen. Ein vollständiges Verständnis des Wirkmechanismus ist meist kostenaufwendig und wird auf das Notwendige begrenzt. Sobald alle Randbedingungen bekannt sind und die Sensoren und Messsysteme ausgewählt wurden kann eine Messung durchgeführt werden. Oftmals werden hier Echtzeitanalyse Werkzeuge eingesetzt um die Dauer der Iterationsschleifen gering zu halten.

Für die Datensammler wäre nun eine einheitliche Beschreibung der Rahmenbedingungen innerhalb von definierten Objekten sinnvoll. Diese liegt in der Praxis bisher nur selten vor, im Bereich der technischen Akustik etabliert sich hier der ASAM ATFX Standard. Hier wird aktuell nach den zuständigen Experten gesucht, welche das ATFX-Modell für Porsche spezifizieren.

Ein weiterer kritischer Punkt ist die Qualität der Messdaten, welche in der Regel durch den Fachbereich eingestuft werden kann. Bestenfalls können hier in Zusammenarbeit mit dem Datenanalyse Team objektive Metriken eingeführt werden.

### AP-3 Datenerfassung und Datenvorverarbeitung (der ausgewählten Komponenten) und Entwicklung zusätzlicher benötigter dezentraler Datenvorverarbeitung

#### Zielsetzung

Die „klassischen“ Fahrzeugdaten sowie die im Rahmen des Projektes zusätzlich erhoben Fahrzeugdaten sollen möglichst vollumfänglich, zueinander synchronisiert und verlustfrei komprimiert gespeichert sowie den nachfolgenden Ketten sowohl „live“ als auch offline zur Verfügung gestellt werden.

Daher ist es das Ziel, das BDEMS von EXX um entsprechende APIs zu erweitern, um einerseits als Ausführungsplattform für fremde Softwareanteile zu dienen oder andererseits, integriert auf fremden Plattformen ausgeführt werden zu können. Ebenso sollen weitere APIs integriert werden, um die einfache Überführung von anfallenden Schritten zu unterstützen, die in der Projektumgebung stattfinden, wie z.B. Featureauswahl /-extraktion. 

#### Ergebnisse

#### Messaufbau

Der Messaufbau wird so gewählt, dass mit einem Messaufbau möglichst viele Use Cases berücksichtigt werden können. Die Anzahl der Bussignale ist mit der aktuellen Abtastgruppe auf 50 Kanäle begrenzt. Die Stromversorgung für die Verbraucher stellt sich als grenzwertig dar und begrenzt die Messzeit auf 2h. Die Kapazität des Batteriespeicher soll zukünftig erhöht und ein Wechselrichter für weitere Verbraucher, wie das VAM, eingesetzt werden. Die Sensorpositionierung wird in folgender Abbildung XX dargestellt. Es werden 4 Beschleunigungsaufnehmer an der Sitzschiene montiert. Diese sind bereits ab 0,1 Hz einsetzbar. Aufgrund einer fehlenden Kopfstütze kann nur ein Mikrofon eingesetzt werden. Zukünftig soll das erweitert werden. Möglicherweise wird der Aufbau hier um einen Dachhimmelausbau erweitert. Die Beschleunigungssensoren an den Schwenklagern sind nahe der äquivalenten Fahrzeugsensoren verbaut. In Vorbereitung für den Use Case Lagerschaden am Elektromotor, wird bereits das VAM System nahe des Elektromotors montiert. Hier fehlt bisher noch der MQTT Client auf Seiten des BDEMS-Systems zur Weiterleitung der Daten in die Cloud. Der kurze Test soll zeigen, wie die spektrale Signatur des Elektromotors beim Anfahren aussieht. Außerdem wird bereits ein offener Road-Condition-Sensor für Messungen im Zusammenhang mit dem Use Case "Bremsgeräuscherkennung" getestet. Dieser ist aufgrund mangelhafter Speisespannung kurzfristig nicht einsetzbar und muss für die anstehende Messkampange aufbereitet werden.

![Messaufbau zur Abdeckung der Use Cases](images/Aufbau2.drawio.png){ width=100mm height=140mm }

#### Auswertung HF-Analyse Elektroantrieb

![Wasserfalldiagramm Anfahren Elektroantrieb](images/AcousticEmission.png){ width=80mm height=80mm }

Das vibroakustische Messsystem (VAM) von AMI ist ein IoT-Gerät, welches über verschiedene Protokolle Informationen von zwei AE-Sensoren zur Verfügung stellen kann. Außerdem kann auf dem Messsystem eine Pipeline zur Datenvorverarbeitung umgesetzt werden. Als Übertragungsprotokoll soll das MQTT-Protokoll eingesetzt werden. Der Vorteil dieses Protokolls ist die einfache Struktur der Kontrollnachrichten, die Möglichkeit, es auf Systemen mit geringen Ressourcen zu verwenden und die Möglichkeit der einfachen Integration in das Informationssystem des Kunden durch Softwarebibliotheken. [@shaoutUsingMQTTProtocol2018]

#### Auswertung Unwucht

Neben dem eigenen IOT-Gerät werden weitere akustische Messsysteme (MBBM PAK) im Testfahrzeug eingesetzt. Diese erlauben eine deutlich höhere Anzahl von Messkanälen bei geringerer Auflösung. Als einheitliches Datenformat ist hier ASAM ATFx File Format (ATFx) standardisiert. Von der Struktur ist die ATFx-Datei eine reguläre XML-Datei, die normalerweise Informationen zur Beschreibung einer Messung enthält. Der Hauptunterschied zu einer normalen XML-Datei besteht darin, dass die ATFx-Datei ein Header-Element mit einem ASAM ODS-Datenmodell enthält. [@ASAMATFxDateiformat]

Ein weitverbreitetes Datenformat (ebenfalls von ASAM) ist MDF (Measurement Data Format). Dieses ist ein binäres Dateiformat zur Speicherung aufgezeichneter oder berechneter Daten für die Nachbearbeitung von Messungen, die Offline-Auswertung oder die Langzeitspeicherung. [@ASAMMDFMessdatenformat]

Die Auswirkungen vom Einbringen einer Unwucht wird 
Zur Auswertung werden im ersten Schritt relevante und vergleichbare

![Spektrogramm des Sensors in Fahrrichtung am rechten, vorderen Schwenklager bei unterschiedlichen Unwuchten und Geschwindigkeiten](images/Spektrogramm.png){ width=150mm height=100mm }

![Ordnungsanalyse durch berechneten Drehzahlkanal](images/Ordnungsanalyse.png){ width=150mm height=100mm }

![Vergleich Körperschallpegel der 1.Ordnung](images/ErsteOrdnung.png){ width=150mm height=100mm }

<!-- TODO Mathematik Ordnungsanalyse -->

#### Export ASAM ATFX -> KVM

### AP-8 Öffentlichkeitsarbeit und Verbreitung der Ergebnisse

Im Projekt wird die Veröffentlichung in Fachzeitschriften (z.B. Mess- und Sensortechnik), die Teilnahme an Fachtagungen (MicroClean Berlin) und eine interne Hausmesse am neuen Firmenstandort angestrebt. Gegebenenfalls kann eine Softwarebibliothek im Bereich ATFX veröffentlicht werden. Zudem sollen Projektergebnisse durch soziale Netzwerke, wie beispielsweise LinkedIn geteilt werden.

### AP-9 Projektmanagemnt

Zu Beginn des Projekts werden einige organisatorische Rahmenbedingungen für die Kommunikation festgelegt. Nach einer agilen Vorgehensweise wird in 2-wöchigen Sprints zusammen an den Arbeitspaketen gearbeitet. Neben den regelmäßigen Sprints findet eine eigenverantwortliche Abstimmung mit den entsprechenden Fachabteilungen und Partnerunternehmen statt. Innerhalb der Sprints werden die Ergebnisse aus den unterschiedlichen Bereichen zusammengeführt.

Die Aufgaben werden innerhalb einer globalen Verwaltung (Jira) nach der Kanban-Methodik organisiert und die Dokumentation erfolgt auf einer eigenen Plattform (Confluence). Eine gemeinsame Bibliothek für die Softwareentwicklung wird durch Gitlab realisiert. Dies ermöglicht, z.B. die Zusammenarbeit an den Signalanalysetoolboxen.

Die Freischaltungen der genannten Plattformen, welche im ersten Halbjahr viele Ressourcen benötigt hat, ist mittlerweile größtenteils abgeschlossen. In einem Konzern, wie das bei Volkswagen der Fall ist, gestaltet sich die Ermittlung aller Beteiligten einer so umfangreichen Pipeline als äußerst herausfordernd, vor allem da hier oftmals unterschiedliche Interessen innerhalb der Fachabteilungen verfolgt werden. Die notwendigen Berechtigungen und Verantwortlichkeiten erfordert daher einen Großteil unserer bisherigen Aufwendungen.

## Vergleich des Stands des Vorhabens

Der Stand des Vorhabens entspricht dem ursprünglichen Arbeits-, Zeit- und Kostenplan. Die in AP 1 - 3 und 8, 9 vorgesehenen Aufgaben wurden alle erfolgreich durchgeführt.

## Anpassung der Ziele des Vorhabens

Aktuell sind keine Änderungen an den Projektzielen erforderlich.

## Literaturverzeichnis
