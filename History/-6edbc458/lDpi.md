
## Einleitung {-}

Merkmale aus akustischen Oberflächenwellen können dank räumlicher Auflösung einzelnen Teilen der Maschine (Werkzeug, Antrieb, Hilfsaggregate) zugeordnet werden und gewinnen so deutlich an Aussagekraft. In Verbindung mit adaptierbarer (Nachrüst-)Sensorik, die weder Anpassungen der Mechanik, der Maschine oder ihrer Steuerung erfordert, kann ein Maschinenbetreiber Zug um Zug seinen Maschinenpark herstellerunabhängig instrumentieren. Auswerteseitig werden nicht nur die von der neu entwickelten Sensorik gelieferten Features herangezogen, sondern auch Planungsdaten aus den kaufmännischen IT-Systemen. Durch diese Daten können die Features entsprechend dem Produkt, der eingesetzten Maschine, dem eingesetzten Werkzeug, der gefahrenen Produktionsgeschwindigkeit und den aktuell verwendeten Vorprodukten ausgewertet werden. Damit wird die Auswertung robuster und muss seltener nachtrainiert werden. Die Auswertung basiert auf Methoden des maschinellen Lernens und stellt eine Verarbeitungsstufe in der Cloud zur Verfügung. Die vorgelagerten Stufen wie die Sensordatenverarbeitung (Edge-Computing) oder die auf einigen Maschinen bereits vorhandene automatische Qualitätssicherung liefern Daten in die Cloud. Diese Datenbasis wird verwendet, um die Algorithmen regelmäßig neu zu trainieren. Durch die Verbindung verschiedener Datenquellen sollen die durch Machine Learning erlernten Modelle von besser instrumentierten Maschinen auf weniger instrumentierte Maschinen übertragen werden.

## Projektorganisation {-}

Im Konsortium werden in regelmäßigen Abständen organisatorische Meetings als Sprints durchgeführt. Die AMI übernimmt die Aufgabe der Projektleitung und organisiert die Aufgaben in einem Kanban System. Der Projektfortschritt wird mittels Ganttchart, siehe Abbildung \ref{Timetable.pdf}, überwacht. Zu Beginn des Projekts gab es eine Verzögerung des Kickoffs aufgrund des Kooperationsvertrags. Die Anforderungsdefinition bzw. die schriftliche Spezifikation hat sich in Folge dessen verzögert. Neben einem Regeltermin werden technische Abstimmungen selbstständig zwischen den Projektpartnern durchgeführt.

![Gantt Diagramm zum Projektfortschritt \label{Timetable.pdf}](images/Timetable.pdf){ width=100% }

Durch die Verwendung cloudbasierter, kollaborativer Arbeitsumgebungen können die gemeinsamen Termine effizient zur Erstellung des Prototyps genutzt werden. Die frühe Implementierung vor Ort und die unabhängige Arbeitsweise an gemeinsamen Arbeitspaketen erlauben rasche Projektfortschritte und den Ausgleich anfänglicher Verzögerungen beim Projektstart.

## Anforderungen\label{sec:anforderung}

Zu Beginn des Projekts werden in Abstimmungsrunden verschiedene Anwendungsszenarien innerhalb von industriellen Produktionsmaschinen untersucht. Dafür wird eine agile, gemeinsame Arbeitsgrundlage geschaffen. Außerdem werden die Voraussetzungen zur qualitativen und quantitativen Überwachung der Zielerfüllung festgelegt.

### Produkt und Werkzeugverschleiß

Wissenschaftlich gesehen, ist die Schallemission ein Phänomen der Erzeugung von Schall- und Ultraschallwellen durch Materialien, die Verformungen und Brüchen ausgesetzt sind [@muravinAcousticEmissionScience].
Aufgrund folgender Eigenschaften ist die Schallemission ein sehr nützliches Werkzeug für die Produktüberwachung [@hamstadReviewAcousticEmission1986]:

- hohe Empfindlichkeit
- Echtzeitfähigkeit
- volumenüberwachender Ansatz

Anhand verschiedener Ansätze zur Bestimmung der Ankunftszeit der ersten P-Welle von akustischen Emissionssignalen (AE-Signalen) können AE-Quellen in beschädigten Strukturen lokalisiert werden [@manuelloAcousticEmissionLocalization]. Geeignet ist vor allem die Acoustic Emission basierte Zustandsüberwachung bei impulshaltigen Geräuschen, welche sich vom Umgebungsrauschen trennen lassen. Ein entsprechend hoher Signal-Rausch-Abstand (SNR) ist daher entscheidend.
Eine Analyse unterschiedlicher Produktionsanlagen zeigt vor allem interessante Anwendungen im Bereich vom Stanzen und bei Ultraschallschweißanlagen. Beim Stanzen ist der Eintritt mehrerer Meißel, zu annähernd gleichen Zeitpunkten, eine Herausforderung bei der Lokalisierung des Schallentstehungsortes. Diesem wird mit hohen Abtastraten begegnet. Jeder Stanzhub ist aufgrund des unterschiedlichen Materialwiderstands einzigartig und erzeugt unterschiedliche Schnittkanten. Ziel ist es diese Unterschiede in den transienten Signalen aufzulösen. Durch spezielle Kameras lassen sich akustische Auffälligkeiten optisch validieren und in objektive Werte überführen.

Durch den Schneidprozess können Rückschlüsse auf den Werkzeugverschleiß gezogen werden. Um den Verschleiß an der Schneide zu messen, müssten die Werkzeuge ausgebaut und vermessen werden.
Durch den Einsatz von AE-Sensoren kann durch diese Kopplungsstellen hindurch gemessen werden, sofern die akustische Dämpfung gegenüber dem Energiegehalt der Wellenpakete klein genug ist. Um quantitative und detaillierte Informationen über verschiedene Verschleißphasen zu erhalten, wird die AE-Energie mittels Short-Term-Fourier-Transformation (STFT) berechnet und in eine geeignete Anzahl von Frequenzniveaus zerlegt. Die individuelle Energieverteilung und die kumulative AE-Energie jeder Frequenzkomponente wird mit einer kontinuierlichen Wavelet Transformation (CWT) analysiert [@baccarWearDetectionMeans2015].
Durch eine Lang- und Kurzzeitbetrachtung der Energieinhalte der Signale in unterschiedlichen Frequenzbereichen lässt sich Verschleiß zuverlässig detektieren. Als Validierungsmaß kann beispielsweise die Ausschussquote bei der optischen Prüfung durch die Kamera herangezogen werden.

### Testumgebung

Als Untersuchungsobjekt wird der in der Abbildung \ref{stanzen.pdf} dargestellte Stanzvorgang genommen. Eine Blechrolle wird abgewickelt, darauf ist ein Sensor-Beacon installiert, welcher die Umfangsbeschleunigung und damit die Drehzahl misst. Dieser lässt sich flexibel magnetisch befestigen und sendet batteriebetrieben, in niedriger Frequenz Messwerte an ein Gateway, das diese an die Sensorik-Bayern-Cloud weiterleitet, dadurch lassen sich Unregelmäßigkeiten im Vorschub erfassen. Die Messwerte stehen den Projektpartnern jederzeit zur Verfügung.

![Schematische Darstellung des Stanzprozesses \label{stanzen.pdf}](images/stanzen.pdf){ width=100% }

Durch den Niederhalter (lila) wird das Blech vorgespannt und die Meißel (rot) durch die obere Platte in das Blech gedrückt. Anschließend prüft ein Kamerasystem die Stanzkanten und ein pneumatischer Abschieber sortiert den Ausschuss direkt aus.
Die Sensorik in der Stanze verhindert, dass ein verkantetes Blech oder ein nicht plan aufsetzender Niederhalter die Meißel zerstört. Durch den Einsatz eines AE-Sensors lassen sich hier gegebenenfalls Kameras und Abstandssensoren einsparen.
Ziel ist es, durch einen Rapid-Prototyping-Ansatz (in Abschnitt \ref{sec:rapidproto}) schnell Messwerte für ein übergreifendes maschinelles Lernen zu erhalten. Daher wird für die optimale Sensorpositionierung vorab eine Bauraumanalyse mittels CAD- und 3D-Druckmodellen der Sensoren durchgeführt, um anhand der verfügbaren Positionen die bestmögliche Befestigungsposition zu ermitteln.
Die Acoustic Emission (AE) Sensoren werden nach einem kurzen Test an der oberen Platte diagonal gegenüberliegend befestigt, da im Betrieb an dieser Platte die höchste Empfindlichkeit gemessen wird. Der Abgleich mit einer Ruhemessung zeigt hier einen ausreichend hohen SNR. Die Anordnung der Sensoren erlaubt eine Ortung in der Ebene. Der Einfluss von Umgebungsgeräuschen und Überlagerungen wird aktuell geprüft.
Viele Produktionsfehler treten nur sporadisch auf und können innerhalb der kurzen Messspanne nicht ermittelt werden. Für aufwendigere Problemstellungen und unterschiedliche Fertigungschargen müssen Machine-Learning Modelle über längere Zeiträume angelernt werden. Daher wird das AE-Messsystem in einem Hardcase verschlossen und an der Maschine für den Dauerlauf gerüstet. Ein UMTS-Router dient zur Remote-Entwicklung und ein Industrie-PC zur Auswertung der Messergebnisse.

### Definition Demonstrator

Als Demonstrationsobjekt wird eine Live-Kategorisierung bekannter Fehler angestrebt, welche zum Ende eines jeden Takts vorliegen. Diese sollen auf Basis einer Streaming Schnittstelle im Rahmen des Demonstrators visualisiert werden. Hier wird eine Visualisierung durch vorhandene quelloffene Software angestrebt, welche sowohl lokal am Messrechner, als auch in der Cloudinfrastruktur funktionsfähig ist. Die Implementierung erfolgt im weiteren Verlauf an einer Massenfertigungsmaschine für Stanzen, welche eine deutlich höhere Taktgeschwindigkeit aufweist.
Die AMI strebt eine akustische Zustandsüberwachung nur auf Basis der akustischen Messdaten an. Weitere Informationsquellen werden auf dieser Prozessebene vorerst nicht berücksichtigt. Zur Validierung auf der nächsten Ebene werden Merkmale zur Verfügung gestellt, welche die Messdaten möglichst komprimiert beschreiben. Diese sogenannten Features werden für die Verarbeitung in Maschine Learning Modellen vorbereitet. Erst an dieser Stelle erfolgt eine Zusammenführung mit weiteren Metainformationen und eine nachgelagerte Validierung mit der optischen Qualitätsprüfung und durch übergeordnete Machine Learning Modelle. Alle Verabeitungsschritte werden im Rahmen dieses Projektes modularisiert, so dass diese langfristig flexibel erweitert und einfach an andere Fertigungsprozesse angepasst werden können. Durch eine hochautomatisierte kontinuierliche Integrations-Pipeline wird eine hohe Qualität des Quellcodes bei AMI sichergestellt. Diese verhindert mögliche Sicherheitsrisikos schon bei der Entwicklung.

### Rollen und Rechte (Informationssicherheit)

Bei AMI werden verschiedene Rollen und damit Zugriffsrechte im Umgang mit den Daten definiert:

- **Systemadministration**, getrennt von den Anwenderrollen für die Auslegung der Verarbeitungspipeline und den Wartungszugriff
- **AI-Experten**, mit Zugriff auf Machine Learning Server und die Zeitreihendaten in einem gesicherten  Netzwerk
- **Projektverantwortliche**, mit Rechten zur Projektverwaltung und allgemeinen Dashboards
- **Messingenieure**, mit Zugriff auf das Messsystem und die Messeinstellungen

Neben der Rollen und Rechtestruktur, für den Einsatz des Messsystems als IOT-Device, ist ein verantwortungsvoller und vertraulicher Umgang mit den Daten entscheidend. Daher werden zu Beginn Datenverantwortlichkeiten und Rollen definiert. Klare IT-Sicherheitsregeln schützen vor Befugnisüberschreitungen.

Die Datenübertragung erfolgt verschlüsselt über ein virtuelles privates Netzwerk. Die Firmware sowie die verwendete Software werden aktuell gehalten und verschiedene Penetrationtests werden automatisiert durchgeführt und manuell geprüft. Eine Netzwerksegmentation inkl. Access Control Lists (ACLs) dient der Zugriffssicherung, die verwendeten Passwörter unterliegen strengen Policies und eine Zwei-Faktor-Autorisierung wird lückenlos eingesetzt [@eross-msftInternetThingsIoT].

Das eingesetzte Messsystem ist vor physischem Zugriff geschützt, die verwendeten Festplatten sind verschlüsselt und weitere Sicherheitsmeachnismen schützen vor ungewolltem Zugriff. Auf dem Gerät werden nur Buffer gespeichert, Zeitreihendaten werden verarbeitet und als Features lokal zur Verfügung gestellt. Die verwendeten virtuellen Maschinen und Container sind separat abgesichert und schützen vor ungewolltem Zugriff der Verarbeitungspipeline. Das System arbeitet auch im Offline-Betrieb zuverlässig und startet bei Ausfall selbstständig neu.

### Evaluierung der Ergebnisse

Die Performance der Prognosegenauigkeit auf Basis der Messdaten bei AMI wird im Vergleich zur Prognose mit kombinierten Metadaten evaluiert. Ein weiteres Bewertungsmaß wird aus dem Abgleich mit den Ausschussraten des optischen Erkennungssystem, welches hier als Referenz angenommen wird, berechnet. Damit ein Ersatz des optischen Prüfssystem umgesetzt werden kann, wird eine 95 % Vorhersageprognose von Ausschussteilen angestrebt. Zusätzlich kann anhand der folgenden zweiteiligen Spezifikation in Abbildung \ref{anforderung.pdf} sichergestellt werden, dass die Anwendbarkeit der akustischen Zustandsüberwachung auf weitere Problemstellung nach einer definierten Vorgehensweise möglich ist.

![Spezifikation der Anforderungen an die Zustandsüberwachung mit Acoustic Emission\label{anforderung.pdf}](images/anforderung.pdf){ width=90% }

Im Basisdesign wird geprüft, ob eine Systemantwort in Form von akustischen Schwingungen zu erwarten ist und ob ein entsprechender Sensor applizierbar ist. Zusätzlich wird geprüft, ob die Leistungsfähigkeit der Messkette ausreicht, um die vorliegenden Schwingamplituden und -frequenzen zu erfassen. In diesem Zusammenhang ist entscheidend, ob die Emissionen der Schallquelle an der Sensorposition erfassbar ist. Mit Basis-Features und einem Autoencoder können bei einfachen Problemstellungen bereits erste Ergebnisse zur Erkennung von Störungen erzielt werden. In den meisten Fällen ist allerdings eine weitere Anpassung an die Applikation notwendig. Hier ist vor allem die Extraktion der Prozessabschnitte und die Entwicklung oder Auswahl relevanter Merkmale entscheidend. Als Basis wird hierbei meist die vorliegende statistische Varianz herangezogen. Tritt die Störungen auf, kann von einer Erkennung durch ein passendes Modell ausgegangen werden. An den markierten Stellen sind meist einige Iterationschleifen notwendig.

## Rapid Prototyping\label{sec:rapidproto}

Dieses Paket dient dem Ziel, möglichst früh im Projekt eine umfangreiche Datenbasis zu schaffen. Dafür wird entsprechende Hardware für einen dauerhaften Betrieb bereits im Vorfeld angeschafft und eine flexible Anbindung über weitverbreitete Schnittstellen ermöglicht. Damit ist durchgehend eine parallele Entwicklung möglich. Denn üblicherweise stellt die späte Datenverfügbarkeit in Forschungsprojekten eine große Herausforderung dar. Hier wird die Entwicklung eines effizienteren Prozessablaufs angestrebt.

Trotz einer zusätzlichen Entwicklungsschleife, aufgrund von Fehlern bei der Zeitreihenspeicherung und der Messeinstellungen, liegt gemäß Zeitplanung eine erste Datengrundlage als Dummy für maschinelles Lernen vor. In Abbildung \ref{requirements.png} werden die dafür grundlegend notwendigen Punkte dargestellt:

![Grundlagen für eine rapide Datenextraktion \label{requirements.png}](images/requirements.png){ width=90% }

### Entwurf der Hard- und Softwarearchitektur

Im Vorfeld wird in einigen Abstimmungsrunden eine Infrastruktur zur schnellen Datenerfassung entwickelt. Diese lässt sich in Abbildung \ref{protoarch.pdf} in einer vereinfachten Hard- und Softwarearchitektur darstellen, welcher auch der Datenfluss, die hierarchische Struktur und die Anteile der Projektpartner entnommen werden können.

![Prototypische Architektur und Datenfluss \label{protoarch.pdf}](images/protoarch.pdf){ width=100% }

Bei der Auslegung der AE-Plattform, welche in Abbildung \ref{hardcase.pdf} aufgezeigt ist, wird vor allem auf eine hohe Flexibilität und Laufzeitstatbilität geachtet. Die AMI hat daher die verwendete Hardware in einem Hardcase mit einem flexiblen Schienensystem montiert. Es wird ein passiv gekühlter UMTS-Router und ein Industrierechner, sowie ein von der AMI entwickeltes VAM-System eingesetzt. Lediglich Stromkabel, UMTS-Antenne, Netzwerkkabel und die Sensorkabel werden aus dem gesicherten Hardcase herausgeführt.

![Darstellung der AE-Plattform für rapide Datenextraktion \label{hardcase.pdf}](images/hardcase.pdf){ width=50% }

Für maximale Flexibilität verwendet die AMI virtuelle Maschinen und Container, welche in Netzwerksegmenten und minimalen Umgebungen spezifische Dienste bereitstellen.
So ist die Messdatenerfassung, die Datenverarbeitung und der Transport in eigenen Containern organisierbar. Die im Router vorhandenen Sicherheitskomponenten erlauben die Bereitstellung eines eigenen MQTT-Brokers oder die Anbindung der Projektpartner innerhalb einer Remote-Arbeitsumgebung.

![Amplitudendarstellung von drei Stanztakten \label{timeraw.png}](images/timeraw.png){ width=90% }

In einer ersten Messserie werden geeignete Sensoren und Messpositionen für den Dauerlauf ausgewählt. Die Live-Analyse der Zeitreihendaten, die manuelle Zerlegung und Diskussion der Prozessschritte sowie die Auswertung der spektralen Komponenten ermöglicht eine rasche Anbindung des Messsystems. In Abbildung \ref{timeraw.png} werden drei Stanztakte exemplarisch dargestellt. Die Messpositionen in diagonaler Anbindung an der oberen Platten, welche die Werkzeuge führt, weißt im Stanzvorgang die geringste Dämpfung der Messsignale auf. Mit Messungen im Ruhe- und im Betriebszustand wird der SNR sichergestellt und durch Kalibriermessungen ist die korrekte Montage der Sensoren validiert. In Abbildung \ref{spectrogram.png} ist das Spektrogramm eines Stanztaktes von 0 bis 500 kHz dargestellt.

![Spektrogramm eines Stanztaktes \label{spectrogram.png}](images/spectrogram.png){ width=90% }

In der Prototypenphase werden die vorhandenen Schnittstellen des Messgerätes (MQTT, OPC UA oder REST) nicht verwendet, stattdessen findet ein direkter Austausch der Projektpartner durch Datentabellen in der AMI-Cloud statt.
AMI stellt eine prototypische, containerbasierte MQTT-Lösung, bestehend aus einem MQTT-Broker und einem Publisher, mit randomisierter Testdatenausgabe bereit, um die Integration in die umfangreiche IT-Infrastruktur der Projektpartner zu vereinfachen.

Die Firma Scherdel (SCH) übernimmt im Projekt das Zusammenführen der Informationen, was aufgrund unterschiedlicher Quellzeitstempel und der komplexen Prozesslogik einen hohen Aufwand darstellt.
Anschließend können verschiedene Quellen sukzessive, synchronisiert werden. Als Austauschformat wird eine Datentabelle mit einer strukturierten Formatierung verwendet. Diese lässt sich flexibel in einer Baumstruktur (Json-File) abbilden und zur Verwendung in MQTT überführen. Die Konvention ist dabei so gewählt, dass in den Spalten ein Multiindex aus mehreren Informationen gebildet wird. Diese beinhalten aktuell folgende Informationen und werden iterativ erweitert:

- die Maschinenidentifikation
- die Prozessschrittnummer
- die skalierten Featurewerte
- die Skalierung oder Gruppierung (log, linear, kubisch, binär)
- die Zeitstempel (UTC-Format)
- den Messkanal, bzw. die Sensorposition

### Methode zur Speicherung der Daten

Die Speicherung der Zeitreihendaten erfolgt bei AMI durch eine Zeitreihendatenbank, welche sich dadurch auszeichnet, dass die Reihenfolge der Einträge von großer Relevanz sind. Entgegen dem Ansatz vorhandene Datenbankeinträge zu aktualisieren, werden Zeitreihendaten typischerweise angehängt, was zu stark wachsenden Datenmengen führt. Die AMI erfüllt bei der Implementierung der Zeitreihendatenbank weitere Kriterien, die kritisch für die Anwendung im industriellen Kontext sind [@martinviitaTimeSeriesDatabase], [@fuReviewTimeSeries2011]:

- So wird darauf geachtet, einen hohen Durchsatz an Speicherungsvorgängen sowie Abfragen auch von mehreren Quellgeräten bzw. Clienten gleichzeitig zu garantieren.
- Replikation, Skalierbarkeit und Zugriffskontrolle sind ebenfalls Faktoren, welche die AMI mit diesem System umsetzt.

Auszüge der Zeitreihendaten werden mit dem Ziel erhoben, Ausreißern gegenüber schon erfasster Datenmodelle zu erkennen und eine Gleichverteilung der Daten in den bekannten Kategorien anzustreben. Mit wenigen Samples soll der Werteraum möglichst vollständig abgebildet werden. Aufgrund der großen Datenmenge werden durch einen intelligenten Datensammler nur Zeitreihen mit einem hohen Informationsgehalt an die AMI Cloud übertragen und dauerhaft gespeichert. Auswertungen werden auf den Anwendungszweck begrenzt. Das erlaubt eine effiziente Anpassung der Modellparameter und eine erleichterte Optimierung der Modelle. Ausgeschöpfte Speicherkapazitäten aufgrund hoher Datenraten (~ 200Gb/Tag) können zu Systemausfällen führen. Aufgrund dessen wird die Entwicklung des intelligenten Datensammlers zur Sicherstellung der Speicherfreigabe priosiert.

### Überführung prototypischer Architektur

Die prototypische Architektur und Spezifikation zur Anwendung von AE im Stanzbetrieb wir im nächsten Schritt auf das Ultraschallschweißen überführt. Damit wird eine Validierung der gewählten Ansätze auf andere Anwendungsfälle umgesetzt.
Zu Beginn ist es notwendig, ein grundlegendes Prozessverständnis aufzubauen. Die Abstraktion vorliegender Prozessinformationen ist in Abbildung \ref{ultraschall.pdf} für das Ultraschallschweißen beschrieben. Nach dem Stanzen der Trägerplatte wird diese mittels Ultraschall mit weiteren Komponenten gefügt. Die Komponenten werden dazu auf einem Fließband transportiert und in zwei Schweißstufen verbunden. In der ersten Stufe werden vier größere Einzelteile hergestellt und in der Zweiten mehrere kleinere Verbindungen.

![Schematische Darstellung Ultraschallschweißen\label{ultraschall.pdf}](images/ultraschall.pdf){ width=100% }

Die Qualität der produzierten Komponenten wird anschließend durch ein Kamerasystem auf Basis geometrischer Aspekte überprüft. Der erste Dauerlauf wird aufgrund interessanter Erkenntnise im Bereich des Ultraschallschweißens über mehrere Wochen durchgeführt. Zum aktuellen Zeitpunkt wird an der notwendigen Prozesszerlegungstiefe gearbeitet. Das Basisdesign zur Datenerhebung konnte bereits umgesetzt und im Dauerlauf erprobt werden. In Abbildung \ref{usprocess.png} sind ein Prozesstakt und zwei Prozessschritte (gemessen an Stütze 1) dargestellt. Aktuell wird die Prozesszerlegung weiter verfeinert, indem geprüft wird, ob sich die vier Sonotroden im Messsignal voneinander trennen lassen.  Im nächsten Schritt ist eine Dauerlaufanalyse an einer der beiden Hochgeschwindigkeitsstanzen geplant. In diesem Zusammenhang sollen auch Abhängigkeiten zwischen den beiden Fertigungsschritten näher untersucht werden.

![Messdaten Prozesszerlegung zum Ultraschallschweißen\label{usprocess.png}](images/usprocess.png){ width=80% }

## Architektur und Design\label{sec:architecture}

### Systemarchitektur

Die prototypische Architektur wird in Abbildung \ref{architectur.pdf} finalisiert. Die Übertragung der Features wird lokal durch einen MQTT-Broker bei Scherdel über speziell gepackte JSON-Files umgesetzt. Die zentrale Datendrehschreibe bei SCH übernimmt die Aufgabe der Datenaggregation und wesentliche Umfänge in der Datenaufbereitung für maschinelles Lernen. Manuelle Workflows werden durch Streaming-Prozesse ersetzt und weiter optimiert.

![Darstellung der Softwarearchitektur\label{architectur.pdf}](images/architectur.pdf)

Die prototypische Architektur aus Abbildung \ref{protoarch.pdf} lässt sich weiter in die einzelnen Teilarchitekturen und ihre Software- bzw. Hardwarekomponenten zerlegen und final zum Referenzmodell weiterentwickeln.

### Systemdesign

In Abbildung \ref{hardware.pdf} wird die aktualisierte Hardwarearchitektur aus Sicht der AMI aufgezeigt. Diese beinhaltet eine Darstellung der verwendeten virtuellen Maschinen (bzw. der Container). Der Development Broker bei Amitronics kann als Übergangslösung zur Integration in die Manufacturing Integration Plattform (MIP) von SCH genutzt werden.

![Darstellung der Hardwarearchitektur \label{hardware.pdf}](images/hardware.pdf){ width=100% }

### Referenzmodell

Es werden Referenzmodelle verwendet, die als Ausgangspunkt für die Entwicklung eines spezifischen Unternehmensmodells nützen, um die Modellierung zu vereinfachen. Sie dienen der Dokumentation, mit Hinblick auf die Unterstützung bei der Einführung von Standardanwendungssoftware. Das vorliegende Referenzmodell in Abbildung \ref{referenz.pdf} zeigt die Applizierung beliebiger Werkzeugmaschinen mit Messtechnik zur Entwicklung der notwendigen Datentiefe und zur Modellierung einer Zustandsüberwachung. Im Flussdiagramm werden entsprechende Zwischenschritte mit einer maschinenlesbaren Beschreibung versehen.

![Referenzmodell zur Modellierung einer Zustandsüberwachung auf Basis beliebiger Messdaten \label{referenz.pdf}](images/referenz.pdf){ width=100% }

## Komponentenentwicklung\label{sec:component}

### Signalverarbeitung und Features

Die Zerlegung der Zeitreihendaten und die damit verbundene Datenaufbereitung ist mit großem Aufwand für AMI verbunden und wird noch einige Monate andauern. In mehreren Iterationschschleifen wird die Prozesszerlegung weiter verallgemeinert und automatisiert. In Abbildung \ref{devprocess.pdf} wird der Entwicklungsprozess auszugsweise dargestellt. Im Streaming Mode, dem Ausgangszustand, werden feste Zeitblöcke vearbeitet. Im Processor Mode werden Impulse extrahiert und getriggert. Im sogenannten Step Mode werden die einzelnen Prozessschritte extrahiert und statistische Merkmale zwischengespeichert. Durch Korellation lassen sich die entsprechenden Prozessschritte automatisiert zuweisen. Nach erfolgreicher Modellierung der Zustandsüberwachung werden unsere Prognosen als Label an die Featurematrix angehängt. Hier ist der Ansatz, die manuellen Einstellparameter immer weiter zu reduzieren und langfristig den Streaming Mode zu ersetzen. Allgemein umfasst das Feature Engineering generell folgende Teilschritte:

- Erstellung von Merkmalen durch Anwendung von Algorithmen
- Transformation bzw. geeignete Darstellung
- Extraktion von Features mit nützlichen Informationen
- Datenverständnis und Mustererkennung
- Benchmark gegenüber dem Modell

![Entwicklungsprozess zur Aufbereitung der Datengrundlage \label{devprocess.pdf}](images/devprocess.pdf){ width=100% }

Die Generierung neuer Merkmale ist einer der schwierigsten Aspekte
des maschinellen Lernens.[@katzExploreKitAutomaticFeature2016] Für akustische Merkmalsgewinnung lassen sich große Funktionssammlungen und verschiedene Transformationen verwenden. (Siehe [@peetersLargeSetAudio2004])
Einige der verwendeten Basisfeatures für Impulse lassen sich aus folgender Abbildung \ref{impuls.png} entnehmen. Des Weiteren werden im Bereich der Psychoakustik auch akustische Features wie die Impulshaftigkeit ausgewertet.

![Darstellung einiger Basis Features zur Beschreibung eines Impulses\label{impuls.png}](images/impuls.png){ width=70% }

Ein wichtiger Punkt für die Auswahl der Features ist das Datenverständnis und die Mustererkennung. Diese kann beispielsweise durch folgende Box-Plot Darstellung in Abbildung \ref{boxplot_base.pdf} erfolgen. Im ersten Beispiel werden einige stupide Basis Features über einen Messtag beim Ultraschallschweißen (US) ausgewertet, es liegt Ausschuss im zweistelligen Bereich vor.
Der Median der zwischen 0 und 1 skalierten Werte liegt ist in grün gekennzeichnet. Die Quantile und die sog. Whisker geben Rückschluss über die Verteilung der Daten der verschiedenen Features (2,5%, 25%, 75% und 97,5%). Hier kann vorwiegend eine schiefe Verteilung (F2 und F3), sowie eine steile Wölbung entnommen werden. Es gibt nur wenige Ausreißer und damit nur eine geringe Streung der Daten. Ein hohe Modellqualität ist aufgrund geringer Streuung und der Schiefe nicht zu erwarten. Außerdem sind die Features teilweise sehr ähnlich (F2 und F3).

![Boxplot der stupider Featureauswahl\label{boxplot_base.pdf}](images/boxplot_base.pdf){ width=100% }

Nach Entwicklung der Prozessschrittzerteilung und der Anwendung weiterer Features kann in Abbildung \ref{boxplot.pdf} eine deutlich unterschiedlichere Verteilung der Features festgestellt werden. Es ist hier von einer besseren Wahrscheinlichkeit für ein gutes Modell auszugehen. Die Modellentwicklung wird nach Zusammenführung mit anderen Datenquellen von IISYS durchgeführt.

![Boxplot nach Optimierung der Features\label{boxplot.pdf}](images/boxplot.pdf){ width=100% }

Ein wesentlicher Aspekt des Projektes ist die Entwicklung oder die Auswahl spezifischer Features, die für eine möglichst kompakte Beschreibung des aktuellen Prozesses dienen. Hierzu verwendet die AMI meist Lösungen aus den Bereichen:

- Hauptkomponentenanalyse
- Autoencoder
- Unabhängigkeitstests

Für das visuelle Feature Engineering nutzt die AMI einen sogenannten Spanselector und eine Measurement-GUI zur Darstellung. Aktuell können damit Zeitbereiche ausgewählt, Features berechnet und dargestellt werden. Die visuelle Extraktion und der Benchmark lassen sich an diese Tools anbinden.

### Blinde Quellentrennung

Zur Unterdrückung von Hintergrundgeräuschen wird ein Dekonvolutionsansatz ohne Vorwissen über die Impulsantwort verwendet. Dazu müssen in einem generischen Modell allerdings Annahmen über die Quellen getroffen werden. Aktuelle Studien befassen sich mit der Verwendung von Autoencodern, wobei der Encoder für die Quelltrennung und der Decoder für das Mixing verantwortlich ist. Zwischen Messpunkten kann außerdem eine Kreuzkorrelation der CWT-Koeffizienten durchgeführt werden, um die Laufzeitunterschiede zu berechnen. Diese Methode kann ebenfalls zur Lokalisierung der Geräuschquelle verwendet werden. Die Erprobung dieser Verfahren hinsichtlich Stanzen oder Ultraschallschweißen wird in den kommenden Monaten verfolgt.

### Lokalisierung SEO

Die Lokalisierung des Schallenstehungsortes (SEO) basiert auf einer Bestimmung der Ankunftszeit der Wellenpakete. Hier setzt die AMI bisher verschiedene Kriterien, wie Hinkley, AIC, Wavelet oder Choi-Williams ein. Durch eine Bestimmung der Laufzeitunterschiede und Berücksichtigung der Sensorpositionen und der Objektgeometrie kann anschließend der Entstehungsort numerisch bestimmt werden. Im vorliegenden Projekt soll ein neuer Ansatz umgesetzt und getestet werden. Aktuell wird ein Versuchsaufbau mit einer Stahlplatte bei AMI als Dummy umgesetzt. Die gesamte Entwicklungsumgebung bei AMI wird dazu aktuell weiter in Richtung testgetriebener Entwicklung optimiert.

### Logging Schnittstelle

Datenprotokollierung, d.h. Logging, im Kontext der Softwareentwicklung ist ein wichtiges Mittel, um Informationen zum Verständnis des Laufzeitverhaltens und der Ressourcenallokation von Softwaresystemen zu aggregieren und damit die Basis für eine Wartung dieser Systeme zu schaffen [@rongSystematicReviewLogging2017].
Durch Log Aggregation werden Daten aus verteilten Systemen, zum Beispiel im Kontext der Containervirtualisierung zusammengeführt und verarbeitet. Zur Fehlersuche und zur Wartung des Condition Monitoring Systems wird eine zentrale Logging Infrastuktur erarbeitet. Durch den Einsatz von Datenloggern ergeben sich mehrere Vorteile:

- effiziente Speicherung
- Vereinfachung von Datenabfragen über mehrere Quellen
- Schnittstelle zur uniformen Datenanalyse

Im Einzelnen wird Datenlogging bei AMI-Systemen verwendet, um den Zustand des Messsystems und der Software mit ihren Teilprozessen zu erfassen. Darüber hinaus wird der Status der zugrunde liegenden Hardware und Container-Virtualisierung erfasst. Eine weitere Anwendung findet sich in der Auswertung der für die Machine Learning Modelle akquirierten Datensätze. So werden Ausreißer, welche nicht klassifiziert werden können, dokumentiert. Durch ein schwellenwertbasiertes Warnsystem werden kritische Vorkommnisse im Ereignislog vermerkt und in Folge dessen werden Nutzer automatisch informiert.
Die Verarbeitungspipeline wird mithilfe einer Kaskade unterschiedlicher Softwarekomponenten realisiert. Zuerst werden die internen Metriken auf den verteilten Messsystemen durch ein Protokollaggregationssystem an eine zentrale horizontal skalierbare Zeitreihendatenbank übertragen. Die erfassten Daten werden für Warnsysteme und zur Kontrollvisualisierung verwendet oder für weitere Analyseverfahren aufbereitet.

## Literaturverzeichnis
