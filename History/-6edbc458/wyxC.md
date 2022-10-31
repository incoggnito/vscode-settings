## Einleitung

Merkmale aus akustischen Oberflächenwellen können dank räumlicher Auflösung einzelnen Teilen der Maschine (Werkzeug, Antrieb, Hilfsaggregate) zugeordnet werden und gewinnen so deutlich an Aussagekraft. In Verbindung mit adaptierbarer (Nachrüst-)Sensorik, die weder Anpassungen der Mechanik der Maschine oder ihrer Steuerung erfordert, kann ein Maschinenbetreiber Zug um Zug seinen Maschinenpark herstellerunabhängig instrumentieren. Auswerteseitig werden nicht nur die von der neu entwickelten Sensorik gelieferten Features herangezogen, sondern auch Planungsdaten aus den kaufmännischen IT-Systemen. Durch diese Daten können die Features entsprechend dem Produkt, der eingesetzten Maschine, dem eingesetzten Werkzeug, der gefahrenen Produktionsgeschwindigkeit und den aktuell verwendeten Vorprodukten ausgewertet werden. Damit wird die Auswertung robuster und muss seltener nachtrainiert werden. Die Auswertung basiert auf Methoden des maschinellen Lernens und stellt eine Verarbeitungsstufe in der Cloud zur Verfügung. Die vorgelagerten Stufen wie die Sensordatenverarbeitung (Edge-Computing) oder die auf einigen Maschinen bereits vorhandene, automatische Qualitätssicherung liefern Daten in die Cloud. Diese Datenbasis wird verwendet, um die Algorithmen regelmäßig neu zu trainieren. Durch die Verbindung verschiedener Datenquellen sollen die durch Machine Learning erlernten Modelle von besser instrumentierten Maschinen auf weniger instrumentierte Maschinen übertragen werden.

## Projektorganisation

Im Konsortium werden in regelmäßigen Abständen organisatorische Meetings als Sprints durchgeführt. Die AMI übernimmt die Aufgabe der Projektleitung und organisiert die Aufgaben in einem Kanban System. Der Projektfortschritt wird mittels Ganttchart, siehe Abbildung \ref{Timetable.pdf}, überwacht. Zu Beginn des Projekts gab es eine Verzögerung des Kickoffs aufgrund des Kooperationsvertrags. Die Anforderungsdefinition bzw. die schriftliche Spezifikation hat sich in Folge dessen verzögert. Neben einem Regeltermin werden technische Abstimmungen selbstständig zwischen den Projektpartnern durchgeführt.

![Gantt Diagramm zum Projektfortschritt\label{Timetable.pdf}](images/Timetable.pdf){ width=100% }

Durch die Verwendung cloudbasierter, kollaborativer Arbeitsumgebungen können die gemeinsamen Termine effizient zur Erstellung des Prototyps genutzt werden. Die frühe Implementierung vor Ort und die unabhängige Arbeitsweise an gemeinsamen Arbeitspaketen erlauben rasche Projektfortschritte und den Ausgleich anfänglicher Verzögerungen beim Projektstart.

## Wiss. tech. Ergebnisse

### Anforderungen

Zu Beginn des Projekts werden in Abstimmungsrunden verschiedene Anwendungsszenarien innerhalb von industriellen Produktionsmaschinen untersucht. Dafür wird eine agile, gemeinsame Arbeitsgrundlage geschaffen. Außerdem werden die Voraussetzungen zur qualitativen und quantitativen Überwachung der Zielerfüllung festgelegt.

#### 1.1.1 Produkt

Wissenschaftlich gesehen ist die Schallemission ein Phänomen der Erzeugung von Schall- und Ultraschallwellen durch Materialien, die Verformungen und Brüchen ausgesetzt sind [@muravinAcousticEmissionScience].
Aufgrund folgender Eigenschaften ist die Schallemission ein sehr nützliches Werkzeug für die Produktüberwachung [@hamstadReviewAcousticEmission1986]:

- hohe Empfindlichkeit
- Echtzeitfähigkeit
- volumenüberwachender Ansatz

Anhand verschiedener Ansätze zur Bestimmung der Ankunftszeit der ersten P-Welle von akustischen Emissionssignalen (AE-Signalen) können AE-Quellen in beschädigten Strukturen lokalisiert werden [@manuelloAcousticEmissionLocalization]. Geeignet ist vor allem die Acoustic Emission basiert Zustandsüberwachung bei impulshaltigen Geräuschen, welche sich vom Umgebungsrauschen trennen lassen. Ein entsprechend hoher Signal-Rausch-Abstand (SNR) ist daher entscheidend.
Eine Analyse unterschiedlicher Produktionsanlagen zeigt vor allem interessante Anwendungen im Bereich vom Stanzen und bei Ultraschallschweißanlagen. Beim Stanzen ist der Eintritt mehrerer Meißel, zu annähernd gleichen Zeitpunkten, eine Herausforderung bei der Lokalisierung des Schallentstehungsorts. Diesem wird mit hohen Abtastraten begegnet. Jeder Stanzhub ist aufgrund des unterschiedlichen Materialwiderstands einzigartig und erzeugt unterschiedliche Schnittkanten. Ziel ist es diese Unterschiede in den transienten Signalen aufzulösen. Durch spezielle Kameras lassen sich akustische Auffälligkeiten optisch validieren und in objektive Werte überführen.

#### 1.1.2 Werkzeug

Durch den Schneidprozess können Rückschlüsse auf den Werkzeugverschleiß gezogen werden. Zur Messung des Verschleiß an der Schneide müssten die Werkzeuge ausgebaut und Vermessen werden.
Durch Einsatz von AE-Sensoren kann durch diese Kopplungsstellen hindurch gemessen werden, sofern die akustische Dämpfung gegenüber dem Energiegehalt der Wellenpakete klein genug ist. Um quantitative und detaillierte Informationen über verschiedene Verschleißphasen zu erhalten, wird die AE-Energie mittels Short-Term-Fourier-Transformation (STFT) berechnet und in eine geeignete Anzahl von Frequenzniveaus zerlegt. Die individuelle Energieverteilung und die kumulative AE-Energie jeder Frequenzkomponente wird mit einer kontinuierlichen Wavelet Transformation (CWT) analysiert [@baccarWearDetectionMeans2015].
Durch eine Lang- und Kurzzeitbetrachtung der Energieinhalte der Signale in unterschiedlichen Frequenzbereichen lässt sich Verschleiß zuverlässig detektieren. Als Validierungsmaß kann beispielsweise die Ausschussquote bei der optischen Prüfung durch die Kamera herangezogen werden.

#### 1.2 Testumgebung

Als Untersuchungsobjekt wird der Stanzvorgang hergenommen, welcher in der Abbildung \ref{stanzen.pdf} dargestellt ist. Eine Blechrolle wird abgewickelt, darauf ist ein Sensor-Beacon installiert, welcher die Umfangsbeschleunigung und damit die Drehzahl misst. Dieser kann flexibel magnetisch befestigt werden und sendet batteriebetrieben, in niedriger Frequenz Messwerte an ein Gateway, welches diese an die Cloud von Sensorik-Bayern weiterleitet. Damit lassen sich Unregelmäßigkeiten im Vorschub erfassen. Die Messwerte stehen den Projektpartnern jederzeit zur Verfügung.

![Schematische Darstellung des Stanzprozesses\label{stanzen.pdf}](images/stanzen.pdf){ width=100% }

Das Blech wird durch den Niederhalter (lila) vorgespannt und die Meißel (rot) werden durch die obere Platte in das Blech gedrückt. Ein Kamerasystem prüft anschließend die Stanzkanten und ein pneumatischer Abschieber sortiert den Ausschuss direkt aus.
Über Sensorik der Stanze wird verhindert, dass ein verkantetes Blech oder ein nicht plan aufsetzender Niederhalter die Meißel zerstört. Durch einen Acoustic-Emission Sensor lassen sich hier gegebenenfalls Kameras und Abstandssensoren einsparen.
Ziel ist es durch einen rapiden Prototyping Ansatz (in AP2) schnell Messwerte für übergreifendes maschinelles Lernen zu erlangen. Daher wird für die optimale Sensorpositionierung im Vorfeld eine Bauraumanalyse durch CAD und 3D-Druck durchgeführt, um an Hand der verfügbaren Positionen die bestmögliche Befestigungsposition zu ermitteln.
Die Acoustic Emission (AE) Sensoren werden nach einem kurzem Test an der oberen Platte diagonal gegenüberliegend befestigt, da an dieser Platte die höchste Empfindlichkeit gemessen wird. Der Abgleich mit einer Ruhemessung zeigt hier ausreichend hohen SNR im Betrieb. Die Anordnung der Sensoren erlaubt eine Ortung in der Ebene. Der Einfluss von Umgebungsgeräuschen und Überlagerungen wird aktuell geprüft.
Viele Produktionsfehler treten nur sporadisch auf und können innerhalb der kurzen Messspanne nicht ermittelt werden. Für aufwendigere Problemstellungen und unterschiedliche Fertigungschargen müssen Machine-Learning Modelle über längere Zeiträume angelernt werden. Daher wird das AE-Messsystem in einem Hardcase verschlossen und an der Maschine für den Dauerlauf gerüstet. Ein UMTS-Router dient zur Remote-Entwicklung und ein Industrie-PC zur Auswertung der Messergebnisse.

#### 1.3 Definition Demonstrator

Als Demonstrationsobjekt wird eine live Kategorisierung bekannter Fehler angestrebt, welche zum Ende eines jeden Takts vorliegen. Diese können auf Basis einer Streaming Schnittstelle im Rahmen des Demonstrators visualisiert werden. Hier wird eine Visualisierung durch vorhandene quelloffene Software angestrebt, welche sowohl lokal am Messrechner, als auch in der Cloudinfrastruktur funktionsfähig ist. Die Implementierung erfolgt im weiteren Verlauf an einer Massenfertigungsmaschine für Stanzen, welche eine deutlich höhere Taktgeschwindigkeit fährt.
Die AMI strebt eine akustische Zustandsüberwachung nur auf Basis der Messdaten an. Weitere Informationsquellen werde auf dieser Prozessebene vorerst nicht berücksichtigt. Zur Validierung auf der nächsten Ebene werden Merkmale zur Verfügung gestellt, welche die Messdaten möglichst komprimiert beschreiben. Diese sog. Features werden für die Verarbeitung in Maschine Learning Modellen vorbereitet. Erst an dieser Stelle erfolgt eine Zusammenführung mit weiteren Metainformationen und eine nachgelagerte Validierung mit der optischen Qualitätsprüfung und durch übergeordnete Machine Learning Modelle. Alle Verabeitungsschritte werden im Rahmen dieses Projektes modularisiert, so dass diese langfristig flexibel erweitert und einfach an andere Fertigungsprozesse angepasst werden können. Durch eine hochautomatisierte kontinuierliche Integrations-Pipeline wird eine hohe Qualität des Quellcodes bei AMI sichergestellt. Diese verhindert mögliche Sicherheitsrisikos schon bei der Entwicklung.

#### 1.4 Rollen und Rechte

TODO Einleitung [Informationssicherheit und physische Absicherung sb]

Für den Einsatz des Messsystems als IOT-Device ist ein verantwortungsvoller und vertraulicher Umgang mit den Daten entscheidend. Daher werden zu Beginn Datenverantwortlichkeiten und Rollen definiert. Klare IT-Sicherheitsregeln schützen vor Überschreiten der Befugnisse.

Die Übertragung erfolgt verschlüsselt über ein virtuelles privates Netzwerk. Die Firmware, sowie die verwendete Software wird aktuell gehalten und verschiedene Penetrationtests werden automatisiert durchgeführt und manuell geprüft. Es wird eine Netzwerksegmentation inkl. Access Control Lists (ACLs) zur Zugriffssicherung verwendet, die verwendeten Passwörter unterliegen strengen Policies und eine Zwei Faktor Autorisierung wird lückenlos eingesetzt [@eross-msftInternetThingsIoT].
Das verwendete Messsystem ist gegen physischen Zugriff geschützt, die verwendeten Festplatten sind verschlüsselt und weitere Sicherheitsmeachnismen schützen vor ungewolltem Zugriff. Auf dem Gerät werden nur Buffer gespeichert, Zeitreihendaten werden verarbeitet und als Features lokal zur Verfügung gestellt. Die verwendeten virtuellen Maschinen und Container sind separat abgesichert und schützen vor Korruption der Verarbeitungspipeline. Das System arbeitet auch im Offline Betrieb zuverlässig und startet bei Ausfall selbstständig neu. Des Weiteren werden bei AMI verschiedene Rollen definiert:

- Systemadministration, getrennt von den Anwenderrollen für die Auslegung der Verarbeitungspipeline und den Wartungszugriff
- AI-Experten, mit Zugriff auf Machine Learning Server und die Zeitreihendaten in einem gesicherten  Netzwerk
- Projektverantwortliche, mit Rechten zur Projektverwaltung
- Messingenieure

#### 1.5 Evaluierung der Ergebnisse

Die Performance der Prognosegenauigkeit auf Basis der Messdaten bei AMI wird im Vergleich zur Prognose mit kombinierten Metadaten evaluiert. Ein weiteres Bewertungsmaß wird aus dem Abgleich mit den Ausschussraten des optischen Erkennungssystem, welches hier als Referenz angenommen wird, berechnet. Damit ein Ersatz des optischen Prüfssystem umgesetzt werden kann, wird eine 99 % Vorhersageprognose von Ausschussteilen angestrebt.

#### Spezifikation

![Spezifikation der Anforderungen an die Zustandsüberwachung mit Acoustic Emission\label{anforderung.pdf}](images/anforderung.pdf){ width=100% }

### 2. Rapid Protyping

Dieses Paket dient dem Ziel, möglichst früh im Projekt eine umfangreiche Datenbasis zu schaffen. Dafür wird entsprechende Hardware für einen dauerhaften Betrieb und eine flexible Anbindung von Schnittstellen bereits im Vorfeld angeschafft. Damit sind parallele Entwicklungsmöglichkeiten über einen großen Zeitraum möglich. Üblicherweise stellt die späte Datenverfügbarkeit in Forschungsprojekten eine große Herausforderung dar. Hier wird die Entwicklung eines effizienten Prozessablaufs angestrebt.

Bereits früh im Projekt liegt dadurch eine Datengrundlage für maschinelles Lernen bereit. In Abbildung \ref{requirements.pdf} werden die grundlegend notwendigen Punkte dargestellt:

![Grundlagen für eine rapide Datenextraktion\label{requirements.pdf}](images/requirements.pdf){ width=90% }

#### 2.1 Entwurf Hard- und Softwarearchitektur

<!--
Frage an VDI: Abgabe Feststellung oder Prozess

@IISYS
- Darstellung Unterstützung
- Prototypische Datenauswertung

@SCH
- Konvention -> Datenformat zur Weiterverarbeitung
- Zusammenführung der Daten
- Prototyp Docker (MQTT)
- Gemeinsame Cloud als Prototypischen Datenaustausch
-->

Im Vorfeld wurde in einigen Abstimmungsrunden eine Infrastruktur zur schnellen Datenerfassung entwickelt. Diese wird in Abbildung \ref{protoarch.pdf} in einer vereinfachten Hard-/ und Softwarearchitektur aufgezeigt. Dieser kann auch der Datenfluss, die hierarchische Struktur und die Anteile der Projektpartner entnommen werden.

![Prototypische Architektur und Datenfluss\label{protoarch.pdf}](images/protoarch.pdf){ width=100% }

Bei der Auslegung der AE-Plattform, welche in Abbildung \ref{hardcase.pdf} aufgezeigt ist, wird vor allem auf hohe Flexibilität und Laufzeitstatbilität geachtet. Die AMI hat daher die verwendete Hardware, in einem Hardcase mit einem Schienensystem montiert. Es wird ein passiv gekühlter UMTS-Router und ein Industrierechner, sowie ein von der AMI entwickeltes VAM-System eingesetzt. Lediglich Stromkabel, UMTS-Antenne, Netzwerkkabel und die Sensorkabel werden aus dem gesicherten Hardcase herausgeführt.

![Darstellung der AE-Plattform für rapide Datenextraktion\label{hardcase.pdf}](images/hardcase.pdf){ width=50% }

Für maximale Flexibilität verwendet die AMI virtuelle Maschinen und Container, welche in Netzwerksegmenten und minimalen Umgebungen spezifische Dienste bereitstellen. So ist die Messdatenerfassung, die Datenverarbeitung und der Transport in eigenen Containern organisiert. Die im Router vorhandenen Sicherheitskomponenten erlauben hier sogar die Bereitstellung eines eigenen MQTT-Brokers oder die Anbindung der Projektpartner innerhalb einer Remote Arbeitsumgebung.

![Amplitudendarstellung von 3 Stanztakten\label{timeraw.png}](images/timeraw.png){ width=90% }

In einer ersten Messserie, werden geeignete Sensoren und Messpositionen für den Dauerlauf ausgewählt. Die Live-Analyse der Zeitreihendaten, die manuelle Zerlegung und Diskussion der Prozessschritte, sowie die Auswertung der spektralen Komponenten ermöglicht eine rasche Anbindung des Messsystems. In Abbildung \ref{timeraw.png} werden drei Stanztakte exemplarisch dargestellt. Die Messpositionen in diagonaler Anbindung an der oberen Platten, welche die Werkzeuge führt, weißt im Stanzvorgang die geringste Dämpfung der Messsignale auf. Messungen im Ruhe- und im Betriebszustand zur Sicherstellung des SNR und Kalibriermessungen prüfen die korrekte Montage der Sensoren. Es wird ein AE-Sensor mit einer Resonanzfrequenz von 375 kHz gewählt, da in diesem Bereich Variationen festgestellt werden können. In Abbildung \ref{spectrogram.png} ist das Spektrogramm eines Stanztaktes von 0 bis 500 kHz dargestellt.

![Spektrogramm eines Stanztaktes\label{spectrogram.png}](images/spectrogram.png){ width=90% }

In der Prototypen Phase werden die vorhandenen Schnittstellen des Publishers (MQTT, OPC UA oder REST) vorgehalten und ein direkter Austausch der Projektpartner findet, durch Datentabellen, in der AMI-Cloud statt. AMI stellt eine prototypische, containerbasierte MQTT-Lösung zur Verfügung, um die Integration in die umfangreiche IT-Infrastruktur der Projektpartner zu vereinfachen.

Anschließend können die verschiedenen Quellen sukzessive, synchronisiert werden. Als Austauschformat wird eine Datentabelle verwendet, welche eine strukturierte Formatierung aufweist. Diese lässt sich flexibel in einer Baumstruktur abbilden und zur Verwendung in MQTT überführen. Die Konvention ist dabei so gewählt, dass in den Spalten ein Multiindex aus mehreren Informationen gebildet wird. Diese beinhalten aktuell folgende Informationen und werden iterativ erweitert:

- die Maschinenidentifikation
- den zeitlichen Zerlegungsschlüssel
- die Feature Anonymisierung
- die Skalierung oder Gruppierung (log, linear, kubisch, binär)
- die Zeitstempel (UTC-Format)
- den Messkanal, bzw. die Sensorposition

<!--
@AMI
- Schnittstellenidentifikation (MQTT, CSV, ...) und Aufwandsabschätzung
- Konvention -> Datenformat zur Weiterverarbeitung
- Prototyp Docker (MQTT)
- Trennung der Netzwerke und der Aufgabenbereiche
- Rechenoperationen auf Basis der Zugriffsrechte
- Zusammenführung der Daten durch Abgleich der Zeitstempel (siehe Härtl)
- Integration der Hardware -> Zusammenstellung der Hardware
- Gemeinsame Cloud als Prototypischen Datenaustausch
-->

#### 2.3 Methode zur Speicherung der Daten

Die Speicherung der Zeitreihendaten erfolgt bei AMI durch eine Zeitreihendatenbank. Zeitreihendatenbanken zeichnen sich dadurch aus, dass die Reihenfolge der Einträge von großer Relevanz sind. Entgegen dem Ansatz vorhandene Datenbankeinträge zu aktualisieren, werden Zeitreihendaten typischerweise angehängt, was zu stark wachsenden Datenmengen führt. Die AMI erfüllt bei der Implementierung der Zeitreihendatenbank weitere Kriterien, die kritisch für die Anwendung im industriellen Kontext sind [@martinviitaTimeSeriesDatabase], [@fuReviewTimeSeries2011]. So wird darauf geachtet einen hohen Durchsatz an Speicherungsvorgängen, sowie Abfragen, auch von mehreren Quellgeräten, bzw. Clienten, gleichzeitig zu garantieren. Replikation, Skalierbarkeit und Zugriffskontrolle sind ebenfalls Faktoren, welche die AMI mit diesem System umsetzt.
Zeitreihendaten werden ausschließlich mit dem Ziel der Erkennung von Ausreißern gegenüber schon erfasster Datenmodelle gesammelt, damit wird eine Gleichverteilung der Daten in den bekannten Kategorien angestrebt. Mit wenigen Samples soll der Werteraum möglichst vollständig abgebildet werden. Aufgrund der großen Datenmenge werden durch einen intelligenten Datensammler nur Zeitreihen mit einem hohen Informationsgehalt an die AMI Cloud übertragen und dauerhaft gespeichert. Auswertungen werden auf den Anwendungszweck begrenzt. Das erlaubt eine effiziente Anpassung der Modellparameter und eine erleichterte Optimierung der Modelle. Ausgeschöpfte Speicherkapazitäten aufgrund hoher Datenraten (~ 200Gb/Tag) können zu Systemausfällen führen. Aufgrundessen wird die Entwicklung des intelligenten Datensammlers bzw. der Speicherfreigabe priosiert.

#### 2.6 Überführung prototypischer Architektur

Die prototypische Architektur und die Spezifikation zur Anwendung von AE wird sowohl für den Stanzbetrieb, als auch für die anschließende Verschweißung von Komponenten verwendet. Damit kann eine Validierung der gewählten Ansätze sichergestellt werden. Zu Beginn ist es notwendig ein grundlegendes Prozessverständnis aufzubauen. Die Abstraktion vorliegender Prozessinformationen ist in Abbildung \ref{ultraschall.pdf} für das Ultraschallschweißen beschrieben. Nach dem Stanzen der Trägerplatte wird diese mit weiteren Komponenten durch Ultraschall verknüpft. Die Komponenten werden dazu auf einem Fließband transportiert und in zwei Schweißstufen verbunden. In der ersten Stufe werden vier größere Einzelteile und in der Zweiten mehrere, kleinere Verbindungen hergestellt.

![Schematische Darstellung Ultraschallschweißen\label{ultraschall.pdf}](images/ultraschall.pdf){ width=100% }

Die Komponenten werden anschließend durch ein Kamerasystem bezüglich der geometrischen Randbedigungen geprüft. Zum aktuellen Zeitpunkt wird an der notwendigen Prozesszerlegung gearbeitet. Das Basisdesign zur Datenerhebung konnte bereits umgesetzt und im Dauerlauf erprobt werden. In Abbildung \ref{usprocess.png} ist ein Prozesstakt und zwei Prozessschritte durch Messung mit nur einem Kanal (an Stütze 1) dargestellt. Aktuell wird an der Zerlegung der vier Sonotroden im Messsignal gearbeitet.

![Messdaten Prozesszerlegung zum Ultraschallschweißen\label{usprocess.png}](images/usprocess.png){ width=100% }

<!--
- Testmessungen an weiterer Maschine
- Beispiel aus AP1 und AP2 mit neuem Use Case Ultraschallschweißen
- Aufzeigen der Unterschiede und der weiteren Entwicklungsaufwände
-->

### 3 Architektur und Design

#### 3.1 Systemarchitektur

Die prototypische Architektur wird in Abbildung \ref{architectur.pdf} finalisiert. Die Kommunikation der Features wird lokal durch einen MQTT-Broker bei Scherdel und gepackte JSON-Files umgesetzt. Die zentrale Datendrehschreibe bei SCH übernimmt die Aufgabe der Datenaggregation und wesentliche Umfänge in der Datenaufbereitung für maschinelles Lernen. Manuelle Workflows werden durch Streaming-Prozesse ersetzt und weiter optimiert.

![Darstellung der Softwarearchitektur\label{architectur.pdf}](images/architectur.pdf){ width=100% }

Die prototypische Architektur lässt sich weiter in die einzelnen Teilarchitekturen und ihre Software- bzw. Hardwarekomponenten zerlegen und final zum Referenzmodell weiterentwickeln. In Abbildung \ref{hardware.pdf} wird die aktuelle Hardwarearchitektur aus der Sicht der AMI aufgezeigt. Diese beinhaltet auch eine Darstellung der verwendeten virtuellen Maschinen (bzw. der Container). Der Development Broker bei Amitronics kann als Übergangslösung zur Integration in die Manufacturing Integration Plattform (MIP) genutzt werden.

![Darstellung der Hardwarearchitektur \label{hardware.pdf}](images/hardware.pdf){ width=100% }

#### 3.2 Systemdesign

In Arbeit...

#### 3.3 Referenzmodell

Referenzmodelle werden als Ausgangspunkt der Entwicklung eines spezifischen Unternehmensmodells genutzt, um damit die Modellierung zu vereinfachen. Sie dienen, mit Hinblick auf die Unterstützung bei der Einführung von Standardanwendungssoftware, der Dokumentation. Das vorliegende Referenzmodell in Abbildung \ref{referenz.pdf} weicht in folgenden Punkten von anderen Referenzmodellen ab...

![Referenzmodell\label{referenz.pdf}](images/referenz.pdf){ width=100% }

### 4 Komponentenentwicklung

#### 4.1 Signalverarbeitung und Features

Die Zerlegung der Zeitreihendaten und die damit verbundene Datenaufbereitung ist mit dem höchsten Aufwand für AMI verbunden und wird die nächsten Monaten andauern. In mehreren Iterationschschleifen wird die Prozesszerlegung weiter verallgemeinert und automatisiert. In Abbildung \ref{devprocess.pdf} wird der Entwicklungsprozess auszugsweise dargestellt. Im Streaming Mode, dem Ausgangszustand, werden feste Zeitblöcke vearbeitet. Im Processor Mode werden Impulse extrahiert und getriggert. Im sog. Step Mode werden die einzelnen Prozessschritte extrahiert und statistische Merkmale werden zwischengespeichert. Durch Korellation lassen sich die entsprechende Prozessschritte automatisiert zuweisen. Hier ist der Ansatz die manuellen Einstellparameter immer weiter zu reduzieren und langfristig den Streaming Mode zu ersetzen.

![Entwicklungsprozess zur Aufbereitung der Datengrundlage\label{devprocess.pdf}](images/devprocess.pdf){ width=100% }

Die verwendeten Basis Features lassen sich aus folgender Abbildung \ref{impuls.png} entnehmen. Desweiteren werden bei AMI automatisiert etwa viele weitere akustische Features, auch im Bereich der Psychoakustik ausgewertet. Eine wesentliche Arbeit im Projekt stellt die Entwicklung oder Auswahl spezifischer Features für eine möglichst kompakte Beschreibung des Signalinhalts dar...

![Darstellung einiger Basis Features zur Beschreibung eines Impulses\label{impuls.png}](images/impuls.png){ width=70% }

<!--
- Review visuelles Feature-Engineering
- Grundsätzliche Vorgehensweise und exemplarisches Beispiel
- Datenvorverarbeitung:
    -  Prozess- und Taktzerlegung
