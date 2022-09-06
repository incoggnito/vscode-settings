## Einleitung

Ein Hindernis für den Technologie- und Erkenntnistransfer der PM-Forschung aus Produktionskontexten ist zum einen in der unzureichenden Adaption bisheriger Verfahren der Künstlichen Intelligenz (KI) an die vorhandene Datenbasis zu finden und zum anderen haben sich aufgrund der Neuartigkeit des Betrachtungsfeldes und des damit verbundenen niedrigen Technologiestandes industrielle Normen und Standardisierungen noch nicht ausreichend etablieren können, um bestehende KI-Verfahren mit geringem Aufwand und Risiko anwendbar zu machen.

Aus dieser Forschungslücke leitet sich das Gesamtziel des Vorhabens ab: Eine Reduzierung von Kosten und Zeit zur Erstellung einer PM-Lösung für Fahrzeugkomponenten unter Einhaltung der Qualitätsstandards.

Die Amitronics GmbH (AMI) möchte die Projektergebnisse nutzen, um ihr Dienstleistungsportfolio an strukturdynamischen und akustischen Messdienstleistungen entscheidend in Richtung KI zu erweitern. Dies soll in mehreren Schritten erfolgen. In einem ersten Schritt sollen insbesondere die bei AMI vorhandenen kommerziellen Mess- und Analysetechniken und -systeme, darunter das mit einem Partner entwickelte Vibroakustische Condition Monitoring System (VAM) für körperschallbasierte Ereignisse an Maschinenstrukturen, in einem breiteren Rahmen für die Themen rund um PM im Automobil nutzbar gemacht werden. Angedacht ist hier, die im Vorhaben entwickelten Cloudlösungen (AP4) für die Aus- und Bewertung der mit unserer Messtechnik erzielten Ergebnisse zu nutzen. Dadurch soll einerseits die Effizienz unserer Messdienstleistungen erhöht und andererseits die Aussagekraft der Ergebnisse dahingehend erweitert werden, dass mit Hilfe von Machine Learning Ansätzen neue, bisher nicht betrachtete Parameter und Abhängigkeiten, wie z.B. spezielle Transferfunktionen und Abhängigkeiten zwischen einzelnen Baugruppen und Komponenten, aber auch zwischen einzelnen Ergebnissen, bei der Ergebnisbewertung und bei der Ableitung von akustischen und strukturdynamischen Lösungsvorschlägen einfließen können.

Gerade hier sieht AMI ein hohes Potenzial für eine qualitativ verbesserte Ergebnisinterpretation bis hin zur Einbindung der Ergebnisse in die von den Partnern entwickelten Verschleißmodelle. Und gerade die Nutzung unserer Daten in Verschleißmodellen würde das Dienstleistungsangebot der AMI weiter ausbauen. Die AMI sieht ein hohes Verwertungspotenzial für ähnliche Aufgaben bei anderen Automobilherstellern, wie z.B. der BMW AG. Aufgrund der fahrzeugtechnischen Breite des Vorhabens (Fahrwerk, Getriebe, Elektronikkomponenten) ist auch hier eine entsprechende Breite an späteren Angeboten zu erwarten, von der Analyse des Planverschleißes bis hin zur Früherkennung von Riss- und Bruchereignissen.

Kurz- und mittelfristig werden hier Dienstleistungsgewerke für AMI von ca. 250T€/Jahr erwartet, langfristig, insbesondere unter Einbeziehung von Fragestellungen aus der Elektromobilität, von 500-750 T€/Jahr. Der Anwendungsbereich der neuen Dienstleistungen geht letztlich weit über den Automobilbau hinaus, wie es die Messdienstleistungen der AMI bereits tun. Zu nennen sind hier der Anlagen- und Maschinenbau sowie die Elektronik bis hin zum Bauwesen und zur Luftfahrt. Dabei liegen die Umsatzerwartungen in ähnlicher Höhe wie im Automobilbau. Darüber hinaus möchte die AMI ihr VAM fahrzeugtauglicher gestalten. Dies betrifft sowohl die Hardware in Bezug auf die Geometrie, einschließlich der Montage im Fahrzeug, als auch den Preis. Ebenfalls angepasst werden muss die Software (Abtastrate, Frequenzbereich, Cloudfähigkeit), um ein kleines, funktionales und fahrzeugtaugliches System nutzen zu können. Bei entsprechender Umsetzung (relevante fahrzeugtypische Parameter und kostenreduziert) ist auch ein permanenter Verbau des Systems im Fahrzeug zum Datenmanagement (Erfassung, Aus-, Bewertung und Bereitstellung) denkbar.

Die AMI strebt an, im Anschluss an das Projekt mehrere Systeme für Premium-Versuchsfahrzeuge bereitzustellen, um die Datenbasis beim Hersteller zu erhöhen und die Aussagekraft der fahrzeuginternen Sensorik gezielt zu validieren und ggf. zu erweitern. Die Umsetzung der Verwertung erfordert die Schaffung neuer, teilweise hochqualifizierter Arbeitsplätze und den Erhalt der derzeit vorhandenen.

## Wissenschaftlich-technische Ergebnisse und andere wesentliche Ereignisse

Die wesentlichen Ziele im Gesamtprojekt liegen in der Schaffung eines Baukastensystems zur schnelleren und effizienteren Entwicklung von Prädiktionsmodellen für Komponentenverschleiß und -ausfälle.

### AP-1 Anwendungsszenarien, Anforderungsanalyse und Systemspezifikation

Eindeutig definierte Anwendungsszenarien (Demonstrationsszenarien) und Indikatoren zur qualitativen und quantitativen Überwachung der Zielerfüllung sowie Anforderungen an Gesamt- und Teilsysteme.

#### Vorgehensweise Technische Akustik

Um eine möglichst modulare Herangehensweise zur Problembehandlung innerhalb eines Referenzmodells zu erzielen, wird zunächst die Ausgangsstellung analysiert.

Die Technische Akustik (kurz NVH - Noise, Vibration, Harshness) gehört meist zu den fünf wichtigsten Eigenschaften, die bei der Konstruktion eines Fahrzeugtyps Priorität haben. Aus Sicht der Technischen Akustik erfolgt im Rahmen der Fahrzeugentwicklung üblicherweise folgende Vorgehensweise [@moserTechnischeAkustik2015,@kollmannPraktischeMaschinenakustik2006, @moserMesstechnikAkustik2010]:

* Fahrzeugziele um den Kundenanspruch, z.B. im Hinblick auf Fahrkomfort zu bedienen
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

In einer Netzwerkkampagne mit unterschiedlichen NVH-Fachbereichen werden Verantwortliche der Gesamtfahrzeug-, Fahrwerks- und Bremsenakustik in das Projekt eingebunden. Damit kann eine umfassende Betrachtung globaler und lokaler akustischer Ereignisse sichergestellt und damit eine stabile Basis für den Baukasten, aus Sicht der Fahrzeugakustik, geschaffen werden. Außerdem erfolgen eine Reihe von Abstimmungen mit Fahrzeugverantwortlichen und Messtechnikausrüstern zur Vorbereitung der Fahrzeuge. Ziel ist es, mit einer Messtechnikaufrüstung im Testfahrzeug langfristig möglichst viele Use-Cases bearbeiten zu können.

In den folgenden Teilabschnitten werden die neuen Use Cases aus Sicht der Technischen Akustik kurz vorgestellt und der Stand der Technik zusammengefasst.

#### Use Case "Radunwucht" {#sec:unwucht}

Jedes an einem Kraftfahrzeug montierte Rad ist in gewisser Weise unwuchtbehaftet. Dafür verantwortlich sind beispielsweise Fertigungstoleranzen, Materialinhomogenitäten, über den Umfang ungleich verteilte Bauteile (z.B. Ventilsitz) oder Verschleißerscheinungen der Lauffläche. Bereits Unwuchten von wenigen Gramm führen bei höheren Geschwindigkeiten zu Vibrationen am Lenkrad und reduzieren somit den Fahrkomfort. Die Auswertung erfolgt üblicherweise im Verhältnis zur Drehzahl am Rad in einer Ordnungsanalyse. Die Ordnungsanalyse ist ein weiterführendes Verfahren der Zeit-Frequenzanalyse an rotierenden Maschinen. Während bei einer herkömmlichen Spektralanalyse die einzelnen Fouriertransformierten als Wasserfall oder Farbkodierung über die Zeit dargestellt werden, wird bei der Ordnungsanalyse die Frequenzachse auf die aktuelle Drehzahl normiert. Damit hat man den Vorteil, dass bei steigender Drehzahl nicht die einzelnen drehzahlabhängigen Frequenzen proportional verschoben werden, sondern als konstante Vielfache der Grundschwingung, die „Ordnungen“ im Ordnungsspektrogramm entlang der Ordinate fix bleiben.

#### Use Case "Sitzschiene"

Sitzschwingungen werden üblicherweise durch analoge Beschleunigungssensoren an der Sitzschiene des Fahrersitzes gemessen. Die gemessenen Antwortsignale können nach einer Aufbereitung in einem Viertelfahrzeugmodell simuliert werden. Im Fahrzeug vorhandene Businformationen sollen zur Berechnung einer virtuellen Sitzschiene herangezogen werden und die analoge Messtechnik ersetzen. Für eine Fahrzeugbaureihe existiert bereits ein Modell zur Reproduktion der realer Fahrbedingungen am Simulator, dieses soll nun auf weitere Fahrzeugbaureihen ausgeweitet werden. Neben unterschiedlichen Anregungen durch die Fahrbahn soll eine Unwuchtanregung am Reifen als spezifischer Anregungsfall erkannt werden. Damit können Anforderungen aus unterschiedlichen Fachbereichen vereint werden. In Zukunft soll die Berechnung des virtuellen Sensorkanals direkt in der Cloud stattfinden. Dieser Anwendungsfall erlaubt in situ eine Nachstellung der Fahrsituation beim Kunden.

### AP-2 Entwicklung des PANAMERA-Referenzmodells

Entwicklung des PANAMERA-Referenzmodells, bestehend aus einem Prozessmodell und einem PM–Baukasten und zur Evaluierung dienen einige ausgewählte Fahrzeugkomponenten.

#### NVH-Baukasten

Um einen effizienteren Prozessablauf und transparentere Schnittstellen zu generieren, müssten aus Sicht eines Akustikingenieurs die Prozesse im Fachbereich nicht wesentlich geändert werden. In der folgenden Abbildung \ref{spec} wird eine solche Vorgehensweise exemplarisch dargestellt und entsprechend erweitert.

![Erweiterung des NVH-Baukastens für eine Datenbereitstellung \label{spec}](images/Baukasten2.drawio.png){ width=150mm height=200mm }

Die Messdaten aus dem NVH-Umfeld stellen eine große Datenquelle innerhalb der Entwicklung eines Fahrzeugs dar. Zur Entwicklung des individuellen Markensounds und zur Unterdrückung von Störgeräuschen werden unzählige Tests in verschiedenen Fachabteilungen durchgeführt. Akustikingenieure sind an der Entwicklung und Absicherung der meisten Komponenten des Fahrzeugs beteiligt. Von Fahrbahn-, Rad-, Motorerregung, dem Fahrgeräusch und dem Sound Design finden sich sehr unterschiedliche Gründe für die akustische Datenerfassung am Fahrzeug. [@zellerHandbuchFahrzeugakustikGrundlagen2013]

Üblicherweise werden diese Use Cases unabhängig voneinander in einer Vielzahl spezifischer Projekte bearbeitet. Die Messdaten werden zwar in der Regel lokal abgelegt, sind allerdings nur selten für übergreifende Analysen nutzbar. Das liegt an fehlenden Zugriffsrechten, unterschiedlichen Datenformaten, unzureichender Datenbeschreibung oder zu spezifischen Randbedingungen. Große Datensammler sollen diese Herausforderung langfristig lösen. Dazu ist es notwendig, dass den Datenerzeugern aus den unterschiedlichen Fachbereichen die Schnittstellen und übergreifende Analysemöglichkeiten bekannt sind. Den Datenanalysten fehlen zumeist nutzbare Daten, daher werden bisher oftmals zusätzliche Tests durchgeführt, welche nicht zwingend notwendig wären.

Bei fehlenden Daten im NVH-Bereich wird zu Beginn geprüft, ob bereits ein Versuchsaufbau vorhanden ist. Fehlt ein Testaufbau, so ist es meist notwendig, den Anregungsmechanismus und die Wirkweise in ihren Grundlagen zu verstehen. Ein vollständiges Verständnis des Wirkmechanismus ist meist kostenaufwendig und wird auf notwendige Umfänge begrenzt. Sobald alle Randbedingungen bekannt sind und die Sensoren und Messsysteme ausgewählt sind, kann der Messplan abgearbeitet werden. Oftmals werden hier bereits Werkzeuge zur Echtzeitanalyse eingesetzt, um die Dauer der Iterationsschleifen gering zu halten.

Für die Datensammler wäre nun eine einheitliche Beschreibung der Rahmenbedingungen innerhalb von definierten Objekten sinnvoll. Diese liegt in der Praxis bisher nur selten vor. Im Bereich der technischen Akustik etabliert sich hier der ASAM ATFX Standard. Hier wird aktuell nach den zuständigen Experten gesucht, welche das entsprechende Datenmodell für Porsche spezifizieren.

Ein weiterer kritischer Punkt ist die Qualität der Messdaten, welche in der Regel durch den Fachbereich eingestuft werden sollten. Im Idealfall wird eine exemplarische Datenpipeline in Zusammenarbeit mit dem Daten-Injektions-Team durchgeführt und es werden objektive Metriken zur Qualitätssicherung eingeführt. Dieser idealisierte Prozessablauf soll im nächsten Kapitel in die Praxis überführt und an einzelnen Anwendungsfällen getestet werden.

### AP-3 Datenerfassung und Datenvorverarbeitung (der ausgewählten Komponenten) und Entwicklung zusätzlicher benötigter dezentraler Datenvorverarbeitun

Die „klassischen“ Daten aus den Fahrzeugsensoren, sowie die im Rahmen des Projektes zusätzlich erhoben Fahrzeugdaten sollen möglichst vollumfänglich, zueinander synchronisiert und verlustfrei komprimiert gespeichert sowie den nachfolgenden Ketten sowohl „live“ als auch offline zur Verfügung gestellt werden.

Daher ist es das Ziel, das BDEMS von EXX um entsprechende APIs zu erweitern, um einerseits als Ausführungsplattform für fremde Softwareanteile zu dienen oder andererseits, integriert auf fremden Plattformen ausgeführt werden zu können. Ebenso sollen weitere APIs integriert werden, um die einfache Überführung von anfallenden Schritten zu unterstützen, die in der Projektumgebung stattfinden, wie z.B. Featureauswahl/-extraktion.

#### Messaufbau

![Messaufbau zur Abdeckung der Use Cases \label{pos}](images/Aufbau2.drawio.png){ width=100mm height=140mm }

Der Messaufbau wird so gewählt, dass mit einer Fahrzeugaufrüstung möglichst viele Use Cases parallel bearbeitet werden können. Damit wird im weiteren Verlauf eine hohe Skalierung vorliegender Datenquellen sichergestellt. Die Anzahl der Bussignale ist mit der am Messsystem verfügbaren Abtastgruppe auf 50 Kanäle begrenzt. Das ist für die einzelnen Use Cases zwar in der Regel ausreichend, könnte sich in Kombination allerdings als grenzwertig erweisen. Hier wird eine iterative Komprimierung auf notwendige Signale angestrebt. Die Stromversorgung für die Verbraucher stellt sich als zu schwach dar und begrenzt die Messzeit aktuell auf 2 Stunden. Die Kapazität des Batteriespeichers soll zukünftig erhöht und ein Wechselrichter für weitere Verbraucher, wie das VAM-System, eingesetzt werden. Die Sensorpositionierung wird in folgender Abbildung \ref{pos} dargestellt. Es werden 4 Beschleunigungsaufnehmer an der Sitzschiene montiert. Diese sind bereits ab 0,1 Hz einsetzbar. Aufgrund einer fehlenden Kopfstütze kann bisher nur ein Mikrofon eingesetzt werden. Zukünftig soll das durch spezielle Halterungen erweitert werden. Die Beschleunigungssensoren an den Schwenklagern sind nahe der äquivalenten Fahrzeugsensoren verbaut. Außerdem wird bereits ein offener Road-Condition-Sensor für kommmende Messungen im Zusammenhang mit dem Use Case "Bremsgeräuscherkennung" getestet. Dieser ist aufgrund mangelhafter Speisespannung kurzfristig allerdings noch nicht einsetzbar und muss für die nächste Messreihe aufbereitet werden.

#### Auswertung HF-Analyse Elektroantrieb (VAM-System)

In Vorbereitung für den Use Case "Lagerschaden am Elektromotor", wird bereits frühzeitig das VAM-System mit den Acoustic Emission Sensoren auf dem Gehäuse des Elektromotors positioniert.
Das VAM-System wird dabei als IoT-Gerät eingesetzt, welches über verschiedene Protokolle Informationen von zwei AE-Sensoren zur Verfügung stellen kann und über verschiedene Live-Auswertungsmöglichkeiten verfügt. Auf dem Messsystem können direkt Pipelines zur Datenvorverarbeitung und zur Detektion von Ereignissen umgesetzt werden. Als Übertragungsprotokoll soll das MQTT-Protokoll eingesetzt werden. Der Vorteil dieses Protokolls ist die einfache Struktur der Kontrollnachrichten, die Möglichkeit, es auf Systemen mit geringen Ressourcen zu verwenden und die Möglichkeit der einfachen Integration in das Informationssystem des Kunden durch quelloffene Softwarebibliotheken. [@shaoutUsingMQTTProtocol2018]. Die MQTT-Schnittstelle soll im nächsten Versuchsaufbau im Zusammenspiel mit dem BEDMS-System getestet werden. Der kurze Test soll zeigen, ob überhaupt messbare Amplituden im hochfrequenten Bereich am Gehäuse des Elektromotors gemessen werden können. In Abbildung \ref{waterfall} zeigen sich bei laufendem Elektromotor ausgeprägte spektrale Komponenten. Die Interpretation dieser Komponenten erfolgt mit der zuständigen Fachabteilung für den UseCase. Die technischen Randbedingungen für die kommende Messreihe am Elektromotor konnten damit bereits vorbereitet werden. Im nächsten Schritt soll eine Messung während der Fahrt durchgeführt werden.

![Wasserfalldiagramm Anfahren Elektroantrieb \label{waterfall}](images/AcousticEmission.png){ width=80mm height=80mm }

#### Auswertung Unwucht und Sitzschiene

Neben dem eigenen IOT-Messsystem werden weitere akustische Messsysteme, wie das System von MBBM PAK, im Testfahrzeug eingesetzt. Diese erlauben eine deutlich höhere Anzahl von Messkanälen bei geringerer Auflösung. Als einheitliches Datenformat für den Export wird hier das ASAM Transport File Format (ATFx) ausgewählt. Von der Struktur ist die ATFx-Datei eine reguläre XML-Datei, die normalerweise Informationen zur Beschreibung einer Messung enthält. Der Hauptunterschied zu einer normalen XML-Datei besteht darin, dass die ATFx-Datei ein Header-Element mit einem ASAM ODS-Datenmodell enthält. [@ASAMATFxDateiformat]

Dieses Datenmodell beschreibt das Prüfobjekt, den Versuchsablauf und die Randbedingungen.
Vor der Versuchsreihe werden die Sensorkanäle beschrieben und zu verschiedenen Abtastgruppen gruppiert und kalibriert. Die triaxialen Sensoren werden mit dem Fahrzeugkoordinatensystem abgeglichen und die Montageposition wird dokumentiert. Die Fahrzeugidentfikationsnummer, der Zustand des Reifendrucks und entsprechende Modifikationen am Fahrzeug beschreiben neben vielen Weiteren Größen den Ausgangszustand des Fahrzeugs. Vor der Messung erfolgt eine dynamische Messbereichsermittlung und eine Streckenfestlegung, sowie die Erfassung der Umgebungsbedingungen, wie beispielsweise Luftdruck, Temperatur und Luftfeuchte. Der Prüfablauf wird oftmals im Versuchsnamen dokumentiert. Für die Erfassung einer Unwucht werden beispielsweise mehrere Konstantfahrten bei unterschiedlichen Geschwindigkeiten und Massen am Rad durchgeführt. Der Titel der Messung lautet dann beispielsweise "Kv140-5_30g_VR_M1". Die Weitergabe des verwendeten Übersetzungschlüssels (Konstantfahrt mit 140 km/h über 5 km mit einer Unwuchtmasse von 30g, am vorderen rechten Rad in erster Wiederholung) ist für die Interpretation der Messergebnisse entscheidend. Das Auftreten einer Unwucht stellt hierbei ggf. ein Label für das nachgelagerte Training von Machine Learning Modellen dar.

Die Auswirkungen vom Einbringen einer Unwucht werden wie in Abschnitt \ref{sec:unwucht} beschrieben, durch Auswertungen von Spektrogrammen, oder entsprechenden Ordnungsanalysen durchgeführt. Das in Abbildung \ref{order} dargestellte Spektrogramm zeigt, die dominierende Raddrehzahl näherungsweise als Konstante im Frequenzbereich. Im Diagramm werden vier verschiedene Unwucht- und Geschwindigkeitspaarungen vergleichen. Es wird erwartet, dass bei höherer Unwucht und höherer Geschwindigkeit, die Beschleunigungsamplitude am Sensor durch zunehmende Vibrationen ebenfalls zunimmt. Diese zunehmende Amplitude lässt sich durch eine Ordnungsanalyse am besten visualisieren. Aufgrund des fehlenden Drehzahlkanals in den Busdaten wird hier ein virtueller Drehzahlkanal berechnet, welcher als Referenz für die erste Ordnung dient.

![Spektrogramm des Sensors in Fahrrichtung am rechten, vorderen Schwenklager bei unterschiedlichen Unwuchten und Geschwindigkeiten](images/Spektrogramm.png){ width=150mm height=100mm }

![Ordnungsanalyse durch berechneten Drehzahlkanal \label{order}](images/Ordnungsanalyse.png){ width=150mm height=100mm }

Zur Berechnung von Schwellwerten und zur Erkennung von kritischen Unwuchten kann nun beispielsweise das Maximum ausgewählt werden. In Abbildung \label{firstorder} wird die erste Ordnung, was der Unwucht bei Raddrehzahl entspricht, ausgewertet. Die erwartete Annahme der Pegelzunahme kann hier durch die Auswertung validiert werden.

![Vergleich Körperschallpegel der 1.Ordnung \label{firstorder}](images/ErsteOrdnung.png){ width=150mm height=100mm }

Der Testablauf zur Erfassung der Unwucht lässt sich bei hinreichender Beschreibung der Messdaten und der Metainformationen aus größeren Datenmengen extrahieren. Somit kann die Datenmenge für ein Modelltraining zur Erkennung von Unwuchten gezielt erweitert werden. Die manuelle Auswertung kann in Programmmodulen innerhalb der Cloud automatisiert durchgeführt und auf Flottendaten übersetzt werden.

Die ermittelten Messdaten an der Sitzschiene werden zur Entwicklung der Modelle im ersten Schritt als Rohdaten zur Verfügung gestellt. Es wird nur eine kurze Plausibilitätsprüfung durchgeführt.

### AP-4 Zentrale Cloud-Datenplattform

Hauptziele der zentralen Datenplattform umfassen die Datenzugänglichkeit sowie deren flexible Analyse. Dabei sollen die Daten sowohl in ihrer Rohform zur Verfügung gestellt als auch geeignet vorverarbeitet werden, um beispielsweise eine effiziente Modellentwicklung bzw. Analyse zu unterstützen.
Die Datenplattform soll in der Cloud realisiert werden (wobei AWS als Provider gewählt werden soll), um Skalierbarkeit und Flexibilität zu ermöglichen. Insbesondere wird eine Trennung – wie in Cloudarchitekturen üblich – von Storage und Compute angestrebt. Dadurch kann die Analyse der Daten und die Modellentwicklung mit Use Case spezifischen Tools erfolgen.
Sowohl der Compute als auch der Storage Layer der Datenplattform sollen in weiten Teilen als "Infrastructure as Code" aufgebaut werden. Dadurch soll gewährleistet werden, dass das Baukastenprinzip für wiederverwertbare Komponenten zur Modellentwicklung auch auf Infrastrukturkomponenten übertragen werden kann.

Das technische Onboarding und der Zugriff ist bis auf den VPN-Hardware Token soweit abgeschlossen. Damit besteht nun Zugang zur Cloudera Enterprise Plattform, Confluence, Jira, Gitlab und einigen weiteren Diensten.
Die wesentliche Herausforderung liegt aktuell in der Bereitstellung der rohen Messdaten, welche im ATFx Format übertragen werden sollen. Es gibt erste Entwicklungsansätze zum Einlesen der Daten, allerdings existiert hier noch keine definierte Laderampe. Bisher werden die akustischen Messdaten hauptsächlich im MDF-Format, einem etablierten Prüfstands-Datenformat abgelegt.

Da eine Datenausgabe im MDF-Format beim verwendeten Messsystem nicht direkt möglich ist, werden die Messdaten im ersten Schritt im Matlab Dateiformat zur Verfügung gestellt, welches auf dem HDF Format basiert und ebenfalls weit verbreitet ist. Dieses Format beinhaltet allerdings nur die Signalnamen und die entsprechenden Messdaten ohne die verbundenen Metadaten zum Messablauf.
Im nächsten Schritt wird geprüft, in welchem Umfang die Anbindung von ATFx innerhalb der PAG möglich ist.

Zur Datenablage ist geplant verschiedene Qualitätsmetriken zu verankern. In Zusammenarbeit mit den Konsortialpartnern, fließt dies in die drei Speicherschichten (RAW-Layer, Stage-Layer und Access-Layer) mit ein. Die Entwicklung dieser Speicherschichten, vor allem bei Betrachtung von Testfahrzeugen wurde wesentlich durch die AMI unterstützt. Dabei spielt die Modularisierung aller Teilprozesse eine wesentliche Rolle und erfordert hohen Abstimmungsaufwand.

### AP-5 Zentrale Analytics-Datenplattform

Ziel dieses Arbeitspaketes ist es somit eine Analytics-Plattform bereitzustellen, die einerseits die Vorverarbeitung, die Modell-Entwicklung und potenziell das Modell-Monitoring begleitet und stützt. Andererseits trägt sie zur Daten-Demokratisierung und effektiven Datennutzung im Betriebsalltag bei.

Bisher werden die Datenanalysen auf den Messrechnern oder durch lokale Auswertungen durchgeführt und teilweise in Gitlab zur Verfügung gestellt. Für die PMMLB (Predictive Maintenance Machine Learning Baukasten) der PAG, wird wie von AMI empfohlen auf eine neuere Packaging Variante nach PEP 621 und 631, umgestellt. [@PEP621Storing,@PEP631Dependency]
Damit lässt sich die Bibliothek aufgrund zentraler Metadaten einfacher erweitern und installieren. Die Analytics-Plattform ist bereits vorhanden und die Einarbeitungsphase beginnt hier neben den laufenden Messreihen.

### AP-8 Öffentlichkeitsarbeit und Verbreitung der Ergebnisse

Im Projekt erfolgten die ersten öffentlichen Auftritte im Rahmen einer Fachtagungen (MicroClean Berlin) und einer internen Hausmesse am neuen Firmenstandort in München mit Fachpublikum aus den Bereichen der Maschinen- und Anlagentechnik. Gegebenenfalls kann langfristig eine Softwarebibliothek im Bereich ATFX veröffentlicht werden. Zudem werden zukünftig Projektergebnisse durch soziale Netzwerke, wie beispielsweise LinkedIn geteilt.

### AP-9 Projektmanagement

Zu Beginn des Projekts werden einige organisatorische Rahmenbedingungen für die Kommunikation festgelegt. Nach einer agilen Vorgehensweise wird in 2-wöchigen Sprints zusammen an den Arbeitspaketen gearbeitet. Neben den regelmäßigen Sprints findet eine eigenverantwortliche Abstimmung mit den entsprechenden Fachabteilungen und Partnerunternehmen statt. Innerhalb der Sprints werden die Ergebnisse aus den unterschiedlichen Bereichen zusammengeführt.

Die Aufgaben werden innerhalb einer globalen Verwaltung (Jira) nach der Kanban-Methodik organisiert und die Dokumentation erfolgt auf einer eigenen Plattform (Confluence). Eine gemeinsame Bibliothek für die Softwareentwicklung wird durch Gitlab realisiert. Dies ermöglicht, z.B. die Zusammenarbeit an den Signalanalysetoolboxen.

Die Freischaltungen der genannten Plattformen, welche im ersten Halbjahr viele Ressourcen benötigt hat, ist mittlerweile größtenteils abgeschlossen. In einem Konzern, wie das bei Volkswagen der Fall ist, gestaltet sich die Ermittlung aller Beteiligten einer so umfangreichen Pipeline als äußerst herausfordernd, vor allem da hier oftmals unterschiedliche Interessen innerhalb der Fachabteilungen verfolgt werden. Die notwendigen Berechtigungen und Verantwortlichkeiten erfordert daher einen Großteil unserer bisherigen Aufwendungen.

## Vergleich des Stands des Vorhabens

Der Stand des Vorhabens entspricht dem ursprünglichen Arbeits-, Zeit- und Kostenplan. Die in AP 1 - 5 und 8, 9 vorgesehenen Aufgaben wurden alle erfolgreich durchgeführt.

## Anpassung der Ziele des Vorhabens

Aktuell sind keine Änderungen an den Projektzielen erforderlich.

## Literaturverzeichnis