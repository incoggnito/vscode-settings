## Einleitung

Merkmale aus akustischen Oberflächenwellen können dank räumlicher Auflösung einzelnen Teilen der Maschine (Werkzeug, Antrieb, Hilfsaggregate) zugeordnet werden und gewinnen so deutlich an Aussagekraft. In Verbindung mit der ohne Eingriff in die Mechanik oder die Steuerung der Maschinen adaptierbaren (Nachrüst-)Sensorik kann ein Maschinenbetreiber Zug um Zug seinen Maschinenpark herstellerunabhängig instrumentieren. Auswertungsseitig werden nicht nur die von der neu entwickelten Sensorik gelieferten Features herangezogen, sondern auch Planungsdaten aus den kaufmännischen IT-Systemen. Durch diese Daten können die Features entsprechend dem Produkt, der eingesetzten Maschine, dem eingesetzten Werkzeug, der gefahrenen Produktionsgeschwindigkeit und den aktuell verwendeten Vorprodukten ausgewertet werden. Damit wird die Auswertung robuster und muss seltener nachtrainiert werden. Die Auswertung basiert auf Methoden des maschinellen Lernens und stellt eine weitere Verarbeitungsstufe in der Cloud zur Verfügung. Die vorgelagerten Stufen wie die Sensordatenverarbeitung (Edge-Computing) oder die auf einigen Maschinen bereits vorhandene, automatische Qualitätssicherung liefern Daten in die Cloud. Diese Datenbasis wird verwendet, um die Algorithmen regelmäßig neu zu trainieren. Durch die Verbindung verschiedener Datenquellen sollen die Modelle von besser instrumentierten Maschinen auf weniger instrumentierte Maschinen übertragen werden.

## Projektorganisation

Im Konsortium werden in regelmäßigen Abständen organisatorische Meetings als Sprints durchgeführt. Die AMI übernimmt die Aufgabe der Projektleitung und organisiert die Aufgaben in einem Kanban System. Der Projektfortschritt wird mittels Ganttchart, siehe Abbildung \ref{Timetable.svg}, überwacht. Zu Beginn des Projekts gab es eine Verzögerung des Kickoffs aufgrund des Kooperationsvertrags. Die Anforderungsdefinition bzw. die schriftliche Spezifikation hat sich in Folge dessen verzögert. Neben einem Regeltermin werden technische Abstimmungen selbstständig zwischen den Projektpartnern durchgeführt.

![Gantt Diagramm zum Projektfortschritt \label{Timetable.pdf}](images/Timetable.pdf)

Durch die Verwendung cloudbasierter, collaborativer Arbeitsumgebungen können die gemeinsamen Termine effizient zur Erstellung des Prototyps genutzt werden. Die frühe Implementierung vor Ort und die unabhängige Arbeitsweise an gemeinsamen Arbeitspaketen erlauben rasche Projektfortschritte und den Ausgleich anfänglicher Verzögerungen beim Projektstart.

## Wiss. tech. Ergebnisse

### Anforderungen

Zu Beginn des Projekts werden in Abstimmungsrunden verschiedene Anwendungsszenarien innerhalb von industriellen Produktionsmaschinen untersucht. Dafür wird eine agile, gemeinsame Arbeitsgrundlage geschaffen. Außerdem werden die Voraussetzungen zur qualitativen und quantitativen Überwachung der Zielerfüllung festgelegt.

#### 1.1.1 Produkt

Wissenschaftlich gesehen ist die Schallemission ein Phänomen der Erzeugung von Schall- und Ultraschallwellen durch Materialien, die Verformungen und Brüchen ausgesetzt sind.[@muravinAcousticEmissionScience]
Aufgrund ihrer hohen Empfindlichkeit, ihrer Echtzeitfähigkeit, ihres volumenüberwachenden Ansatzes und ihrer Empfindlichkeit gegenüber allen Prozessen oder Mechanismen, die Schallwellen erzeugen, ist die Schallemission ein sehr nützliches Werkzeug für die Produktüberwachung. [@hamstadReviewAcousticEmission1986] Es wurden verschiedene Ansätze zur Bestimmung der Ankunftszeit der ersten P-Welle von akustischen Emissionssignalen (AE-Signalen) vorgeschlagen, um die Lokalisierung von AE-Quellen in beschädigten Strukturen durchzuführen. [@manuelloAcousticEmissionLocalization] Geeignet ist es vorallem für die akustische Zustandsüberwachung bei impulshaltigen Geräuschen, welche sich vom Umgebungsrauschen trennen lassen. Ein entsprechend hoher Signal-Rausch-Abstand (SNR) ist daher entscheidend.
Eine Analyse unterschiedlicher Produktionsanlagen zeigt vorallem interessante Anwendungen im Bereich vom Stanzen und bei Ultraschallschweißanlagen. Beim Stanzen ist der Eintritt meherer Meißel, zu annhähernd gleichen Zeitpunkten, eine Herausforderung bei der Lokalisierung des Schallentstehungsorts. Diesem wird mit hohen Abtastraten begegnet. Jeder Stanzhub ist aufgrund des unterschiedlichen Materialwiderstands einzigartig und erzeugt unterschiedliche Schnittkanten. Ziel ist es diese Unterschiede in den transienten Signalen aufzulösen. Durch spezielle Kameras lassen sich akustische Auffälligkeiten optisch validieren und in objektive Werte überführen.

#### 1.1.2 Werkzeug

Durch den Schneidprozess können inderekt Rückschlüsse auf den Werkzeugverschleiß gezogen werden. Zur Messungs des Verschleiß an der Scheinde müssten die Werkzeuge ausgebaut und Vermessen werden. Durch Einsatz von AE-Sensoren kann durch diese Kopplungsstellen hindurch gemessen werden, sofern die akustische Dämpfung gegenüber dem Energiegehalt der Wellenpakete klein genug ist. Um quantitative und detaillierte Informationen über verschiedene Verschleißphasen zu erhalten, wird die AE-Energie mittels Short-Term-Fourier-Transformation (STFT) berechnet und in eine geeignete Anzahl von Frequenzniveaus zerlegt. Die individuelle Energieverteilung und die kumulative AE-Energie jeder Frequenzkomponente wird mit einer kontinuierlichen Wavelet Transformation (CWT) analysiert.[@baccarWearDetectionMeans2015]
Durch eine Lang- und Kurzzeitbetrachtung der Energieinhalte der Signale in unterschiedlichen Frequenzbereichen lässt sich verschleiß zuverlässig detektieren. Als Validierungsmaß kann beispielsweise die Ausschussquote bei der optischen Prüfung durch die Kamera herangezogen werden.

#### 1.2 Testumgebung

Als Untersuchungsobjekt wird der Stanzvorgang innerhalb der in Abbildung \ref{stanzen.svg} dargestellt. Ein Blechcoil wird abgewickelt, darauf ist ein Sensor-Beacon installiert, welcher die Umfangsbeschleunigung und damit die Drehzahl misst. Dieses kann flexibel magnetisch befestigt werden und sendet batteriebetrieben, in niedriger Frequenz Messwerte an ein Gateway, welches diese an die Cloud von Sensorik-Bayern weiterleitet. Damit lassen sich beispielsweise auch unregelmäßigkeiten im Vorschub erfassen. Die Messwerte können stehen den Projektpartnern jederzeit zur Verfügung.

![Schematische Darstellung des Stanzprozesses \label{stanzen.pdf}](images/stanzen.pdf)

Das Blech wird durch den Niederhalter (lila) vorgespannt und die Meißel (rot) werden durch die obere Platte in das Blech gedrückt. Ein Kamerasystem prüft anschließend die Stanzkanten und ein pneumatischer Abschieber sortiert den Aussschuss direkt aus. Am Fundament ist ein Abstandsensor verbaut, welcher verhindert, dass ein verkanteter Blechausschuss die Meißel zerstört. Durch einen Acoustic-Emission Sensor lassen sich hier gegebenenfalls Kameras und Abstandssensoren einsparen.
Ziel ist es durch einen rapiden Prototyping Ansatz (in AP2) schnell Messwerte für übergrefeifendes maschinelles Lernen zu erlangen. Daher wird für die optimale Sensorpositionierung im Vorfeld eine Baurraumanalyse durch CAD und 3D-Druck durchgeführt, um an Hand der verfügbaren Positionen die bestmögliche Befestigungspositon zu ermitteln.
Die Acoustic Emission (AE) Sensoren werden nach einem kurzem Test an der oberen Platte diagonal gegenüberliegend befestigt, da an dieser Platte die höchste Empfindlichkeit gemessen wird. Der Abgleich mit einer Ruhemessung zeigt hier ausreichend hohen SNR im Betrieb. Die Befestigung in der Ebene erlaubt die Ortung durch zwei Sensoren im Betrieb. Der Einfluss von Umgebungsgeräuschen und Überlagerungen wird aktuell geprüft.
Viele Produktionsfehler treten nur sporadisch auf und können innerhalb der kurzen Messspanne nicht ermittelt werden. Für aufwendigere Problemstellungen und unterschiedliche Fertigungschargen müssen Machine-Learning Modelle über längere Zeiträume angelernt werden. Daher wird das AE-Messsystem in einem Hardcase verschlossen und an der Maschine für den Dauerlauf gerüstet. Ein UMTS-Router dient zur Remote-Entwicklung und ein Industrie-PC zur Auswertung
der Messergebnisse.

#### 1.3 Definition Demonstrator

Als Demonstrationsobjekt wird eine live Kategorisierung bekannter Fehlstellen angestrebt, welche zum Ende eines jeden Takts ein Ergebnis darstellen kann. Diese können auf Basis einer Streaming Schnittstelle im Rahmen des Demonstrators visualisert werden. Hier wird eine Visualisierung durch vorhandene quelloffene Software angestrebt, welche sowohl lokal am Messrechner, als auch in der Cloudinfrastruktur funktionsfähig ist. Die Implementierung erfolgt im weiteren Verlauf an einer Massenfertigungsmaschine für Stanzen, welche für höhere Taktgeschwindigkeiten ausgelegt und keine Kameraüberwachung einsetzt.
Die AMI strebt eine akustische Zustandsüberwachung nur auf Basis der Messdaten an. Eine weitere Informationsquelle wird auf dieser Prozessebene vorerst nicht berücksichtigt. Zur Validierung in der nächsten Prozessebene werden Merkmale zur Verfügung gestellt, welche die Zeitrohdaten möglichst komprimiert beschreiben. Diese sog. Features werden für die Verarbeitung in Maschine Learning Modellen vorbereitet. Erst an dieser Stelle erfolgt eine Zusammenführung mit weiteren Metainformationen und eine nachgelagerte Validierung durch übergeordnete Machine Learning Modelle. Alle Verabeitungsschritte werden in Rahmen dieses Projektes modularisiert, so dass diese langfristig flexibel erweitert und einfach an andere Fertigungsprozesse angepasst werden können. Durch eine hochautomatisierte Pipeline wird eine ausreichend hohe Qualtität des Quellcodes bei AMI sichergestellt. Diese prüft auch mögliche Sicherheitsrisikos schon bei der Entwicklung. Als Ergebnis daraus entsteht ein Template für die Erstellung neuer Projekte in Python.

#### 1.4 Rollen und Rechte

Für den Einsatz des Messsystem als IOT-Device ist ein verantwortungsvoller und ein vertraulicher Umgang mit den Daten entscheidend. Daher werden zu Beginn klare Datenverantwortlichkeiten und Rollen definiert. Klare IT-Sicherheitsregeln schützen vor überschreiten der Rollenbefugnisse.
Die AMI sammelt Zeitrohdaten ausschließlich mit dem Fokus der Erkennung von Ausreißern gegenüber bekannten Datenmodellen und einer Gleichverteilung der Daten in den bekannten Kategorien. Aufgrund der Datenmenge werden durch einen intelligenten Datensammler nur notwendige Zeitreihen an unsere Cloud übertragen. Auswertungen werden auf Anwendungszweck begrenzt. Das erlaubt uns effizient Änderung an den Parametern der verwendeten Modelle vorzunehmen und unsere Modelle zu optimieren. Die Übertragung erfolgt verschlüsselt über ein virtuelles privates Netzwerk. Die Firmware, sowie die verwendete Software wird aktuell gehalten und verschiedene Penetrationtests werden automatisiert durchgeführt und manuell geprüft. Es wird eine Netzwerksegmentation verwendet, die verwendten Passwörter unterliegen strengen Policies und eine 2 Faktor Authorisierung wird lückenlos eingesetzt.[@eross-msftInternetThingsIoT]
Das verwendete Messsystem ist gegen physischen Zugriff geschützt, die verwendeten Festplatten sind verschlüsselt und weitere Sicherheitsmeachnismen schützen vor ungewolltem Zugriff. Auf dem Gerät werden nur Buffer gespeichert, Zeitrohdaten werden verarbeitet und als Features lokal zur Verfügung gestellt. Die verwendeten virtuellen Maschinen und Container sind separat abgesichert und schützen vor Korruption der Verarbeitungspipeline. Das System arbeitet auch im Offline Betrieb zuverlässig und startet bei Ausfall selbstständig neu. Desweiteren werden bei AMI verschiedene Rollen definiert:

- Systemadministration, getrennt von den Anwenderrollen für die Auslegung der Verarbeitungspipeline und den Wartungszugriff
- AI-Experten, mit Zugriff auf Machine Learning Server und die Zeitrohdaten in einem gesicherten  Netzwerk
- Projektverantwortliche, mit Rechten zur Projektverwaltung

#### 1.5 Evaluierung der Ergebnisse

Ein wesentliches Ergebnis zur Evaluierung der Performance bei AMI ist die Prognosefähigkeit auf Basis der Messdaten im Unterschied zur Prognose mit komibinierten Metadaten. Ein wesentliches Ergebnis ist außerdem der Abgleich mit den Aussschussraten aus den optischen Erkennungssystem, welche hier als Referenz angenommen werden. Es wird eine 99 % Vorhersageprognose von Aussschussteilen angestrebt.

#### Spezifikation

### 2. Rapid Protyping

Dieses Paket dient dem Ziel, möglichst früh im Projekt eine umfangreiche Datenbasis zu schaffen. Dafür wird entsprechende Hardware (Dauerbetrieb, flexible Schnittstellen) bereits im Vorfeld angeschafft. Damit sind parallele Entwicklungsmöglichkeiten über einen großen Zeitraum möglich. Üblicherweise stellt die späte Datenverfügbarkeit in Forschungsprojekten eine große Herausforderung dar. Hier wird die Entwicklung eines effizienten Prozessablaufs angestrebt.

Wir konnten bereits früh im Projekt und nach Zeitplan eine Datengrundlage für maschinelles Lernen bereitstellen. In Abbildung \ref{requirements} wird zusammengefasst was aus unserer Sicht grundlegend notwendig ist:

![Grundlagen für eine rapide Datenextraktion \label{requirements.pdf}](images/requirements.png)

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

Im Vorfeld wird in einigen Abstimmungsrunden eine Infrastruktur zur schnellen Datenerfassung entwicklet. Diese wird in Abbildung \ref{protoarch} in einer vereinfachten Hard-/ und Softwarearchitektur aufgezeigt. Dieser kann auch der Datefluss, die hierarchische Struktur und die Anteile der Projektpartner entommen werden.

![Prototypische Architektur und Datenfluss \label{protoarch.pdf}](images/protoarch.pdf)

Bei der Auslegung der AE-Plattform, welche in Abbildung \ref{hardcase.svg} wird vorallem auf hohe Flexibilität und Laufzeitstatbilität geachtet. Die AMI hat daher die verwendete Hardware, in einem Hardcase mit einem Schienensystem montiert. Es wird ein passiv gekühlter UMTS-Router und ein Industrierechner, sowie unser VAM-System eingesetzt. Lediglich Stromkabel, UMTS-Antenne, Netzwerkkabel und die Sensorkabel werden aus dem gesicherten Hardcase herausgeführt.

![Darstellung der AE-Plattform für rapide Datenextraktion \label{hardcase.pdf}](images/hardcase.pdf)

Für maximale Flexibilität verwenden wir virtuelle Maschinen und Container, welche in Netzwerksegmenten und minimalen Umgebungen spezifische Dienste bereitstellen. So ist die Messdatenerfassung, die Datenverarbeitung und der Transport in eigenen Containern organisiert. Die im Router vorhandenen Sicherheitskomponenten erlauben hier sogar die Bereitstellung eines eigenen MQTT-Brokers oder die Anbindung der Projektpartner. Durch den UMTS-Router sind nur wenige vor Ort-Termine notwendig.

In der Prototypen Phase werden die vorhandenen Schnittstellen des Publishers (MQTT, OPC UA oder REST) vorgehalten und ein direkter Austausch der Projektpartner findet, durch Datentabellen, in der AMI-Cloud statt. AMI stellt eine prototypische, containerbasierte MQTT-Lösung zur Verfügung, um die Integration in die umfangreiche IT-Infrastruktur der Projektpartnern zu vereinfachen.

Die Firma Scherdel (SCH) übernimmt im Projekt das Zusammenführen aller Informationen, was aufgrund unterschiedlicher Quellzeitstempel und der komplexen Prozesslogik einen hohen Aufwand darstellt. Trotz des Aufwands ist dies am praktikabelsten bis IT-Sicherheit, Rechnerkapazitäten und Personalauslastung eine Integration erlauben. Anschließend können die verschiedenen Quellen sukzessive,  synchronisiert werden. Als Austauschformat wird eine Datentabelle verwendet, welche eine strukturierte Formatierung aufweist. Dise lässt sich flexibel in einer Baumstruktur abbilden und zur Verwendung in MQTT überführen. Die Konvention ist dabei so gewählt, dass in den Spalten ein Multiindex aus meheren Informationen gebildet wird. Diese beinhalten aktuell folgende Informationen und werden iterativ erweitert:
