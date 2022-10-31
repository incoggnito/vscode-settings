
## Einleitung {-}

Ein Bauteil oder Werkzeug meldet sich automatisch bei Beschädigung oder Verschleiß, die Maschine bestellt selbstständig neues Material. Für solche  Szenarien aus dem Umfeld Industrie 4.0 sind zur Erfassung der Zustände moderne, smarte Sensoren und Messsysteme notwendig. Verfügbare Lösungen am Markt sind abhängig von der Applikation und für die Anwendung beim Drahtziehen oftmals unzureichend.
Um den Drahtziehprozess zu überwachen werden im industriellen Umfeld sowie in der Forschung unterschiedliche Lösungsansätze und Methoden verwendet. Neben optischen Systemen, welche sich zur Prozessüberwachung auf kamerabasierte Sichtsysteme[@larssonProcessMonitoringWire2017] oder Wärmesicht[@larssonMonitoringEvaluationWire2019] stützen, exisiteren auch durch Virbationssensorik[@pejryd_process_2017] gestützte Überwachungsverfahren. Diese Lösungsansätze unterscheiden sich in der Herangehensweise, fokussieren aber die Überwachung Schmierung des Drahtes. Eine fehlende Schmierung kann zu Materialschäden bzw. Schäden an der Drahtoberfläche führen, welche zu Rissen oder Kerben führt. Da eine Mangelschmierung sowie die Oberflächenschäden des gezogenen Drahts den Körperschall verändern, wird der Drahtzugprozess seitens AMI über den Körperschall überwacht und dem Maschinenbediener dargestellt.

## Anforderungs- und Zieldefinition

Angestrebt werden kundenspezifische Condition Monitoring Systeme (CMS), die sich je nach Funktionalität in Systembaukästen mit zwei verschiedenen Umfängen untergliedern lassen, wobei das größere Paket die Funktionalität des kleineren Pakets beinhaltet:

- Paket S (small)
  - Bereitstellung und Visualisierung der aufbereiteten Messdaten
  - Schnittstelle zur Messdatenübermittlung an den Hersteller
- Paket M (middle)
  - Fehleranalyse/-diagnosen
  - Handlungsempfehlungen
  - Schnittstelle zur Datenübermittlung an den Hersteller

Die vom CMS zu erfassenden Zustände, Fehler und Daten werden eingegrenzt und klassifiziert. Des Weiteren wird bei der Bereitstellung der Daten unterschieden:

- in Echtzeit, parallel zum Drahtziehprozess
- nach Notwendigkeit bei erkannten Ereignissen
- auf Abfrage des Maschinenbedieners oder anderer Anwender

Im Entwicklungsprozess können sich weitere Anforderungen oder Randbedingungen ergeben, welche für eine spätere Übertragbarkeit auf weitere Anlagen mit zu erfassen sind.

### Evaluierung relevanter Einflussgrößen sowie Erarbeitung einer Einflussmatrix

Ein Katalog der Betriebszustände und zugehöriger Fehlerbilder vom Projektpartner KIESELSTEIN (KIES) dient als Grundlage für die Einflussmatrix und die Auswahl der zu untersuchenden Störungen. Diesen hat AMITRONICS (AMI) um eine Abschätzung zur Diagnosefähigkeit der Drahtzugfehler erweitert.

![Fehlerursachen beim Drahtzug\label{Fehlerursache.pdf}](images/Fehlerursache.pdf){ width=100% }

In der Abbildung \ref{Fehlerursache.pdf} sind die Fehlerursachen zusammengefasst und resultierende Fehler dargestellt. Die relevantesten Fehler lassen sich auf die Maschinenparametern, die Schmierung, das Material oder auf das Werkzeug zurückführen. Als Projektziel wird die Detektion von Rattermarken, Ringmarken, Schrammen und Ziehriefen definiert. Daneben wird die Erkennung von Rucken des Drahtes und das Herabfallen des Drahtes angestrebt. Rattermarken und Ringmarken lassen sich dabei entweder auf eine falsche Ziehgeschwindigkeit oder ein ungünstiges Schmiermittel zurückführen. Schrammen werden überwiegend durch eine unzureichende Schmierung oder Inhomogenitäten im Drahtmaterial verursacht. Eine unzureichende Schmierung oder ein scharf gelaufener Ziehstein können in Ziehriefen resultieren. Eine nicht optimale Abläuferregelung bewirkt ein Rucken oder Herabfallen des Drahtes.
Grundsätzlich lassen sich die Schäden in zwei Detektionsklassen unterteilen:

- transiente Ereignisse, z.B.: Rattermarken, Ablösungen am Ziehstein
- dauerhafte Ereignisse, insbesondere Verschleiß oder eine Mangelschmierung

In Planungsrunden mit den Kooperationspartnern werden Störgrößen ausgewählt, welche sich synthetisch reproduzieren lassen, z.B. Rattermarken und Ringmarken sollen durch eingeschlagene Kerben im Ausgangsdraht nachgestellt werden. Zur Plausibilitätsprüfung werden verschlissene Werkzeuge herangezogen. Für die Betriebsmessungen werden Messserien in regelmäßigen Abständen durchgeführt. Die zeitliche Plannung der Messserien wird in Abbildung \ref{Gantt.pdf}) dargestellt.

![Durchgeführte Messreihen\label{Gantt.pdf}](images/Gantt.pdf)

- **1 Strukturanalyse und Sensorabgleich**
Zwischen der ersten und der zweiten Messserie wird der Sensor der TU Chemnitz (TUC) und das vibroakustische Messsystem von AMI weiterentwickelt.

- **2, 3 Sensorpositionierung, Fehlerkatalog und Schädigungsmechanismen**
Anhand der Ergebnisse der ersten Messungen werden geeignete Sensorpositionen ausgewählt. Ab der zweiten Messserie werden hochfrequente Acoustic Emission Messungen durchgeführt. Bei der zweiten und dritten Messserie werden verschiedene Drahtmaterialien verwendet.

- **4, 5 Messserien zur Zustandsüberwachung**
In der vierten Messserie wird mit dem in die Ziehmaschine integrierten Sensor der TUC gemessen. Zwischen den letzten beiden Messserien ist ein größer zeitlicher Abstand geplant, um alle Aufgaben und evtl. auftretende Verbesserungsmöglichkeiten umsetzen zu können. Mit der 5. Messserie wird das CMS validiert.

Bei allen Betriebsmessungen werden die Ziehgeschwindigkeit und weitere Betriebsparameter, wie die Kühlung und Schmierung, variiert. Zusätzlich wird neben dem regulären Ziehprozess, der Betrieb bei künstlich eingebrachten Störungen analysiert. Um das Produktionsspektrum annähernd abzudecken, werden Drahtcoils mit unterschiedlichen Zugfestigkeiten: *C90 (Federstahl), 54SICR6, S235JR (Baustahl), 100CR6, X2CrNiMoN22-5-3 (Edelstahl)* verglichen. Ein Überblick der verwendeten Parameter ist in Tabelle \ref{tab:allparams} dargestellt. Ein möglichst großer Abdeckungsbereich führt zu stabileren und damit praxisorientierten Prognosemodellen.

Auf den Schälbetrieb wird verzichtet, da der Ziehbetrieb in der Industrie häufiger eingesetzt wird und erste Messungen zeigen, dass die Störquellen im Körperschallsignal beim Schälen dominanter sind als im Ziehbetrieb.

### Definition der Funktionseinheiten

Beim Drahtziehen im Allgemeinen und durch Messpositionen nahe am Ziehstein muss die verwendete Messtechnik folgende Anforderungen erfüllen (vgl. Tabelle \ref{env}):

| Anforderung      | Beschreibung                                                                                                                                                                                                                                   |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Temperatur       | Beim Ziehen mit mangelnder Schmierung oder bei ausgefallender Kühlung können Oberflächentemperaturen an der Ziehsteinkassette bis ca. 140°C auftreten                                                                                          |
| Feuchtigkeit     | Die Sensoren und das Condition Monitoring System sollten gegen Spritzer geschützt sein, da diese in der Umgebung der Ziehmaschine nicht ausgeschlossen werden können.                                                                          |
| Staub            | Als Schmierung wird unter anderem pulverförmige Ziehseife verwendet. Beim Nachfüllen der Ziehseife treten regelmäßig Staubwolken auf.                                                                                                          |
| Schlagfestigkeit | Leichte Stöße und Schläge auf die Sensorik und das Messsystem können bei Montagearbeiten an der Ziehmaschine nicht vermieden werden. Erschütterung durch Abrisse von Drähten unter extremen Betriebsparametern dürfen nicht zu Schäden führen. |

Table: Anforderungen an die Messtechnik \label{env}

Zur Vernetzung der Maschinensteuerung mit dem vibroakustischen Messsystem (VAM), einer grafischen Benutzerschnittstelle und den Datenbanken wird der Industriestandard OPC UA gewählt [@opcfoundationOPCUnifiedArchitecture2014].
Dieses wird als modulares Interface implementiert, um die Verwendung anderer Protokolle zuzulasssen. Ein Pflichtenheft bezüglich der Hard- und Software zur Definition der Funktionseinheiten, welches die Komponenten, Schnittstellen und Anforderungen aller Projektpartner detailliert beschreibt, wird erstellt. Die Architektur des Gesamtsystem wird in Prozessleitebene, Komponentenebene und Sensorebene aufgeschlüsselt (vgl. Abb. \ref{Gesamtkonzept.pdf}). Durch die einzelnen Ebenen und möglichst allgemeinen Schnittstellen wird ein sehr modulares Gesamtkonzept angestrebt. Das OPC UA Netzwerk kann um weitere OPC UA Server und Clients erweitert werden, die direkt an das lokale Netzwerk des CMS angeschlossen werden.

![Gesamtkonzept Condition Monitoring System \label{Gesamtkonzept.pdf}](images/Gesamtkonzept.pdf){ width=85% }

Um im Projekt eine frühe Verfügbarkeit der Informationen der Maschinensteuerung zu ermöglichen, wird diese durch AMI in einem gesonderten Prozess simuliert. Über eine Benutzerschnittstelle in Form eines Kommandozeileninterfaces (command line interface, CLI) können die Prozessparameter und Maschinendaten eingetragen werden, welche mit OPC UA gestreamt werden.
Die Informationen umfassen folgende Größen: Ziehgeschwindigkeit, Schmierung, Kühlung, Material, Ausgangsdurchmesser und gezogener Durchmesser (vgl. Abb. \ref{KommuStruktur.pdf}). Als konstante Metainformationen werden beispielhaft Maschinentyp,  Seriennummer, Einsatzort, Kundenname und der Hersteller für die spätere Verwendung beim Kunden und für das Federated-Learning hinterlegt.

Die Messdaten und alle Metainformationen werden in SQL-Datenbanken auf File-Ebene mittels SQLite abgespeichert.[@SQLiteHomePage] Als Datenformat wird das in pywaveline definierte Format gewählt, welches auf Basis der FLAC-Komprimierung von Audiodateien und bezüglich der Zugriffszeiten und hoher Abtastraten mit bis zu 10 MHz optimiert ist. [@WaveLineWavelineDocumentation, @FLACWhatFLAC]
Das Interface zur Hardware und die Verarbeitungspipeline wird durch AMI entwickelt. Die Verarbeitung der Daten erfolgt parallel in separaten Prozessen. Bei dem entwickelten CMS sollen final nur die Features berechnet werden, welche die wesentlichen Merkmale zur Identifikation von vorliegenden Störgrößen beinhalten. Diese dienen als Eingangsgröße für die Machine Learning Modelle zur Zustandsbewertung. Eine Darstellung der Features erfolgt mittels einer modularen GUI (vgl. Abschnitt \ref{chap:CMSGUI}).
Durch die modulare und parallele Vorgehensweise ist die Einhaltung der Echtzeitfähigkeit nur von der Berechnung der Features abhängig. Komplexe Features müssen ggf. verzögert und nur bei Bedarf ausgewertet werden.
Zur zeitlichen Markierung von transienten Ereignissen während einer Messung setzt AMI eine weitere CLI ein. In einem Konfigurationsfile sind bekannte Events vordefiniert. Bei der Auswahl wird die ID des Events mit dem Zeitstempel in der Datenbank hinterlegt. Dadurch können die Messdaten live gelabelt und für das Machine Learning vorbereitet werden. Beispielsweise kann somit der Zeitpunkt, wenn eine künstliche erzeugte und farblich markierte Kerbe den Ziehstein passiert, erfasst werden.

Die Struktur der Kommunikation ist in Abbildung \ref{KommuStruktur.pdf} dargestellt. Die Zustandsdaten, die als Eingangsgröße für die Machine Learning Modelle verwendet werden, setzen sich aus den zeitlich synchronisierten Sensordaten, Daten der Events und den Betriebsparametern zusammen. Mit diesen Daten wird der aktuelle Zustand bewertet und gelabelt. Die Sensordaten umfassen die Zeitrohdaten und Features, die auf Basis der Zeitrohdaten berechnet werden. Die Benutzereingabe des aktuellen Events wird zum Training der Modelle verwendet. In den Zustandsdaten werden neben den Sensordaten alle Betriebsparameter zusammengefasst.

![Informationsmodell \label{KommuStruktur.pdf}](images/KommuStruktur.pdf){ width=85% }

## Acoustic Emission Analyse (AE-Analyse)

Die ursprünglich geplante strukturdynamische Untersuchung(Modal, Eigenfrequenz- und Flächenbeitragsanalyse) wird nach einer ersten Testmessung verworfen. Die Schallemission der Maschinenstruktur ist gegenüber der Schallquelle zur Identifikation von Fehlern beim Drahtziehen von geringer Relevanz. Stattdessen werden Analysen der Schallemissionen an der Quelle, dem Ziehstein, durchgeführt. Diese wurde durch eine Transferpfadanalyse und die Erstellung von Abklingkurven vertieft.

### Ermittlung geeigneter Sensorpositionen

Die Vorauswahl der Sensorpunkte wird an den geometrischen Randpunkten der Struktur so gewählt, dass eine möglichst steife Anbindung bei geringen Nichtlinearitäten sichergestellt werden kann. Hierzu wird im ersten Schritt eine Bauraumanalyse an einem CAD Modell der Maschine durchgeführt. Die Ziehmaschine und die Ziehsteinkassette sind in Abb. \ref{ZiehmaschineCAD.pdf} dargestellt. Der Umformvorgang des Drahtes findet innerhalb des Ziehsteins statt. Damit stellt die lokale plastische Verformung die Hauptschallquelle und den Entstehungsort der AE-Signale dar. Als geeignete Sensorpositionen werden Positionen in der direkt auf der Ziehsteinkassette identifiziert (vgl. \ref{Strukturanalyse.png}).

![CAD-Modell der Ziehmaschine \label{ZiehmaschineCAD.pdf}](images/ZiehmaschineCAD.pdf){ width=100% }

![Sensorpositionen für die strukturdynamische Analyse \label{Strukturanalyse.png}](images/Strukturanalyse.png){ width=100% }

Auf Basis des HSU-Nielsen-Tests werden Messungen an verschiedenen Messpunkten durchgeführt. Zur Bestimmung des relevanten Frequenzbereichs (des Drahtziehprozesses) werden AE-Events (transiente Burstsignale) gemittelt und mit dem Ruhepegel verglichen. Die abgebildeten AE-Events werden durch Kerben im Draht erzeugt. Der Ruhepegel zeigt die Resonanzfrequenz des Sensors bei 150 kHz und die Geräusche der Aggregate unterhalb von 100 kHz. Die Impulsantworten der Kerben sind im Frequenzbereich mit ausreichendem Signalrauschabstand (von 20 dB) bis etwa 400 kHz sichtbar. Daher wird eine obere Frequenzgrenze von 400 kHz und eine Abtastrate von 1 MHz festgelegt (vgl. Abb. \ref{Ruhepegelabgleich.png}).

![Ruhepegelabgleich \label{Ruhepegelabgleich.png}](images/Ruhepegelabgleich.png){ width=100% }

### Betriebsschwingungsmessungen mit Kerben

Im weiteren Projektverlauf wird der Sensor der TUC direkt in eine Nut in der Ziehsteinkassette eingepresst. Der Referenzsensor (Pos. 3 in Abb. \ref{Strukturanalyse.png}) wird mit Magnetbügelhaltern an der Kassette montiert. Die spektralen Leistungsdichten des Normalbetriebs mit Störungen (vgl. \ref{Spek_Leistdicht2.png}) werden zur Validierung der Sensorpositionen herangezogen. In der Abbildung entsprechen die Nummern der Sensoren den Sensorpositionen in Abb. \ref{Strukturanalyse.png}. An den Positionen S1 bis S4 und an Position S7 sind handelsübliche AE-Sensoren angebracht. Die Sensoren PT-Piesa 1 & 2 der TUC befinden sich an Sensorposition 5 & 6.

![Spektrale Lesistungsdichten des Normalbetriebs mit Kerben \label{Spek_Leistdicht2.png}](images/Spek_Leistdicht2.png){ width=100% }

An Sensorposition 1 und 2 (Trommelanbindung, Schälsteinmutter) gibt es keine zeitliche Korrelation zur Störung. Im Messsignal des Sensors an der Kasette sind aufgrund der Kerben im Draht, Impulse erkennbar. Diese sind auch im Spektrogramm des Sensors 4 sichtbar, wobei der Einfluss hier stärker gedämpft wird. Bei dieser Messung zeigt der PT-Piesa 1 keine Korrelation zum Referenzsensor(S3). PT-Piesa 2 kann die vorliegenden Impulse im hörbaren Frequenzbereich auflösen.

### Analyse von Betriebsschwingformen der Prüfmaschine

Mit Betriebsschwingformanalysen kann die Anregung der einzelnen Aggregate separat an mehreren Messpunkten ausgewertet werden. Eine Superposition der Haupt- und Nebenschallquellen zeigt die relevanten Betriebsschwingformen und die Verschiebung der vorherrschenden Resonanzfrequenzen (vgl. \ref{noise_aggregats.png}).

![Triaxiale Körperschallanalyse unterschiedlicher Aggregate\label{noise_aggregats.png}](images/noise_aggregats.png)

Diese Analyse wird mit triaxialen Beschleunigungssensoren im Frequenzbereich bis 5 kHz durchgeführt. Die größte Amplitude (über alle Messpositionen), exemplarisch an S7 dargestellt, tritt während dem Betrieb des Spänebrechers auf. Der Schälbetrieb und Späneförderungsbetrieb ist in der Amplitude und den Betriebsschwingformen vergleichbar. Die Kühlung, Hydraulik und Schmiermittelaggregate sind in der Amplitude vernachlässigbar. Da diese Komponenten sowohl beim Ziehen als auch beim Schälen aktiv sind, ist es vorteilhaft, dass ihr Störgeräuscheinfluss nicht dominant ist. Der Ziehbetrieb zeigt Strukturresonanzen mit deutlich geringerem Grundrauschen. Aufgrund dieser Erkenntnis und der höheren Praxisrelevanz wird im Folgenden nur der Ziehbetrieb weiter analysiert.

### Ableitung der Körperschallübertragungspfade der Prüfmaschine

Um die Transferfunktion zwischen Draht und Sensor an der Matrize zu bestimmen, wird der HSU-Nielsen Test verwendet. Als Anregungspunkte werden mehrere Positionen am Draht und an der Versuchsanlage verwendet. Der Koordinatenursprung ist an der Ziehsteinkassette direkt am Sensor definiert. Die weiteren Punkte sind entgegen der Laufrichtung des Drahtes positiv angegeben. Die Kopplungsimpedanz zwischen Draht und Ziehstein führt zu einer Amplitudenverringerung von 20 dB über das gesamte Spektrum. Weitere Dämpfungen treten durch einen erhöhten Abstand zum Sensor auf (vgl. \ref{Abkling1.png}).

![Vergleich der Abklingkurve an verschiedenen Anregungspositionen\label{Abkling1.png}](images/Abkling1.png){ width=100% }

Durch Anregung am Maschinenfundament und am Drahtcoil kann gezeigt werden, dass Umgebungseinflüsse aufgrund hoher Dämpfungen vernachlässigbar sind (vgl. \ref{Abkling2.png}).

![Abklingkurve der Umgebungseinflüsse \label{Abkling2.png}](images/Abkling2.png){ width=100% }

Die Messergebnisse bei synthetischer Anregung stimmen mit den Erkentnissen der Betriebsmessungen (vgl. Abb. \ref{Spek_Leistdicht2.png}) überein.
Zusammenfassend zeigt sich die Sensorposition an der Ziehsteinkassette als valide Messposition. Hier werden die vorliegenden Umgebungseinflüsse hinreichend gedämpft und Änderungen im Drahtziehprozess werden detektiert.

### Vergleich des Körperschallverhaltens zwischen synthetischem und laufendem Betrieb

Die Ergebnisse der ersten Messserie zeigen, dass die synthetisch erzeugten Störungen sehr gut auflösbar sind (vgl. \ref{SpekBetriebStoer.png}). Die spektrale Struktur der Phänomene ist allerdings nur schwierig zu unterscheiden.
Innerhalb der zweiten und dritten Messserie werden unterschiedliche Drahtdurchmesser und Werkstoffe bei verschiedenen Ziehgeschwindigkeiten mit und ohne Störungen gezogen.

![Spektrale Leistungsdichte des regulären Betriebs und bei Störungen \label{SpekBetriebStoer.png}](images/SpekBetriebStoer.png){ width=50% }

#### Analyse des Luftschallverhaltens

Für die Analyse des Luftschallverhaltens der Ziehmaschine werden Mikrofone an einem weiteren Messsystem (synchron zum VAM-System) angeschlossen (vgl. Abb. \ref{Mess_6_Aufbau.png}).

![Messaufbau mit Mikrofone und Hochgeschwindigkeitskamera \label{Mess_6_Aufbau.png}](images/Mess_6_Aufbau.png){ width=80% }

Für die Verwendung von Mikrofonen wird eine neue frei programmierbare Hardware zugekauft, welche mit den Softwaremodulen des VAM-Systems ausgestattet wird. Die hohe Modularität unserer Toolboxen erlaubt eine schnelle Anbindung. Das Interface zur Kommunikation mit der Hardware wird über den geplanten Projektumfang hinaus entwickelt. Die Messungen mit den Mikrofonen ergeben, dass der Informationsgehalt der Mikrofone keinen Mehrwert gegenüber den AE-Sensoren bietet. Diese Erkenntnis unterstreicht die Eignung der AE-Sensoren für diesen Anwendungsfall.

### Optische Auswertung zur Validierung der akustischen Zustandsüberwachung

Während den ersten Messreihen stellt sich heraus, dass eine objektive Bewertung des Verschleißes für das Training der Zustandsüberachung unzureichend ist. Es gelingt nicht, den aktuellen Verschleiß des Ziehsteins oder die aktuelle Schmiermenge objektiv zu bewerten. Zur Zustandsbewertung des Ziehsteins müsste dieser wiederholt ausgebaut werden, was sich für eine Inspektion in den benötigten kurzen Messintervallen als unpraktikabel darstellt. Die Ziehseife kann nicht restlos entfernt werden und das Restschmierverhalten variiert deutlich. Für eine durchgehende, objektive Qualitätsbeurteilung der Drahtoberfläche wird diese, in einer Mehrleistung, im Rahmen der dritten Messserie mit einer Hochgeschwindigkeitskamera gefilmt (vgl. Abb. \ref{Mess6_Kamerapos.png} und Abb. \ref{Mess_6_Aufbau.png}).

![Aufbau der Hochgeschwindigkeitskamera für eine durchgehende, objektive Qualitätsbeurteilung \label{Mess6_Kamerapos.png}](images/Mess6_Kamerapos.png){ width=50% }

Anhand der Aufnahmen sollen Qualitätsfehler zeitlich den Messdaten zugeordnet werden. Mit erheblichen Aufwand wird der Aufnahmestart der Kamera mit dem Start der Messung synchronisiert. Es stellt sich heraus, dass die Reflexion der benötigten Beleuchtung und Schmierstoffreste auf dem Draht keine zuverlässige Qualitätsbeurteilung zulassen.

Für eine nachgelagerte Qualitätsanlyse wird der Draht im Stillstand an Stützstellen mikroskopisch untersucht. Durch einen definierten Abstand der Stützstellen und einer Markierung des Starts und Endes der Messungen auf der Drahtoberfläche lassen sich die Oberflächenanalysen mit den Messdaten synchronisieren. Eine automatisierte Auswertung der Messreihen ist daher nicht möglich und ein manueller Abgleich ist notwendig. Eine optische Prüfeinheit zur Absicherung der akustischen Zustandsüberwachung wäre im Rahmen der Entwicklung sehr hilfreich. Ein Vergleich der Drahtoberfläche in Abbildung \ref{DrahtMikro1.png} und \ref{Drahtmikro2.png} verdeutlicht dies.

| ![Ziehriefen und Schrammen\label{DrahtMikro1.png}](images/DrahtMikro1.png){ width=40% } | ![Gute Oberflächenqualität\label{DrahtMikro2.png}](images/DrahtMikro1.png){ width=40% } |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
|                                                                                         |                                                                                         |

Table: Optischer Vergleich der Drahtoberflächen

Zusätzlich werden die Ziehsteine wiederholt vor und nach den Messungen mikroskopisch untersucht (vgl. Abb. \ref{ZiehsteinAnalyse.png}), um deren Betriebszustände zu ermitteln.

![Mikroskopaufnahmen der Ziehsteine \label{ZiehsteinAnalyse.png}](images/ZiehsteinAnalyse.png){ width=80% }

Die Obefläche ausgewählter Drahtstücke der letzten Messserie werden ferner von der TUC vermessen, um objektive Qualitätskriterien zu ermitteln. Das Training der Zustandsüberwachung kann dadurch im Nachgang verfeinert werden.

Über die Qualitätskontrolle des gezogenen Drahtes und der Inspektion der Ziehsteine sind Rückschlüsse auf die Belastungs- und Beanspruchungssituation der Ziehmaschine und des Ziehsteins bei den jeweiligen Messungen möglich. Die Auswirkungen von fehlerhaften Betriebsbedingungen können dadurch ermittelt werden.

## Entwicklung akustischer Merkmale und Algorithmen

Folgende Analysen ausgewählter Features beziehen sich auf das Messsignal eines handelsüblichen AE-Sensors, mit einer Resonanzfrequenz um 150 kHz, welcher an S3 befestigt ist.
Zu Beginn wird der Einfluss der Ziehgeschwindigkeit auf das quadratische Mittel (root mean square, RMS) untersucht. (vgl. Abb. \ref{BaustahlRMSTest.png})

![RMS für verschiedene Ziehgeschwindigkeiten\label{BaustahlRMSTest.png}](images/BaustahlRMSTest.png)

Im Folgenden Abschnitt wird Baustahl verwendet und der Ziehstein ist bereits vorgeschädigt. Dargestellt sind Messungen mit Ziehgeschwindigkeiten von 30, 60, 90 und 120 m/min. Es wird ersichtlich, dass die Amplitude nicht proportional, sondern nur abgeschwächt mit Erhöhung der Ziehgeschwindigkeit zunimmt. Die Schwankungen im Pegel zeigen den unruhigen Ziehprozess.

![RMS für verschiedene Zustände des Ziehsteins \label{BaustahlRMSSchaeden.png}](images/BaustahlRMSSchaeden.png)

Die zweite Darstellung des RMS (vgl. Abb. \ref{BaustahlRMSSchaeden.png}), zeigt eine Auswertung beim Ziehen von Baustahl mit 30 m/min. Vergleichend sind Messungen im Gesundzustand, bei Kerben im Ausgangsdraht und bei einem beschädigtem Ziehstein gezeigt. Der beschädigte Ziehstein verursacht deutlich erhöhte RMS-Werte. Dagegen kann nicht zwischen dem Gesundzustand und einem Ziehprozess mit einzelnen Kerben im Draht unterschieden werden.

Im Rahmen der Messserien werden die Prozessparameter wiederholt sehr umfangreich variiert. Folgender Tabelle \ref{tab:allparams} können alle verwendeten Prozessparameter entnommen werden:

| Parameter                   | Verwendete Werte                                                                                           |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Ziehgeschwindigkeit [m/min] | 0, 30, 60, 90, 120                                                                                         |
| Betriebszustand             | Anfahren, stationärer Ziehprozess, Abbremsen, nur Aggregate an, Spänebrecher an                            |
| Schmierung                  | Vorhanden, Übergang zur Mangelschmierung, Mangelschmierung                                                 |
| Kühlung                     | Ein, Aus                                                                                                   |
| Drahtmaterial               | S235JR, 14462, 54SICR6, 100CR6, C90                                                                        |
| Ausgangsdurchmesser [mm]    | 4.0, 6.5, 7.7, 8.2, 8.5, 9.05, 9.1, 9.5, 10                                                                |
| Gezogener Durchmesser [mm]  | 3.36, 5.56, 6.5, 7.16, 7.7, 8.3, 8.5, 8.4, 9.2, 9.3                                                        |
| Zustand des Ausgangsdrahtes | gewalzt, gezogen, schlechte Ziehqualität                                                                   |
| Zustand des Ziehsteins      | neu, gebraucht, mit Ringverschleiß, mit künstlichem Verschleiß, mit Ausbrüchen, beschichtet, unbeschichtet |
| transiente Ereignisse       | keine, künstliche Kerben, Draht am Boden anschlagen, Hammerschläge, Drahtsprünge am Ausgangscoil           |

Table: Prozessparameter Variationen\label{tab:allparams}

Zur ersten Überprüfung der Features werden verschiedene Metriken im Zeit- und Frequenzbereich, auf die Messdaten eines Ziehprozesses mit künstlichen Kerbschlägen im Baustahl (S235JR), angewendet.
Im Zeitbereich kann mit dem Crest-Faktor, dem Impulsfaktor und dem Margin die Impulshaftigkeit der Messdaten untersucht werden. Dazu werden diese Kennwerte über eine festgelegte Blocklänge berechnet. Bei einer Ziehgeschwindigkeit von 30 m/min und einem Kerbabstand von 2 cm haben die Impulse einen Abstand von 40 ms. Dadurch liegt in jedem Block nur ein Impuls vor.

![Features des Zeitbereichs zur Kerben Erkennung\label{TimeFeatures.png}](images/TimeFeatures.png)

Die Auswertung in Abb. \ref{TimeFeatures.png} zeigt, dass etwa im Bereich der Zeitblöcke 2000 bis 2500 die höchste Impulshaftigkeit vorliegt. In diesem Bereich liegen auch die eingeschlagenen Kerben. Dennoch werden auch außerhalb dieses Bereichs ähnlich hohe Ausschläge festgestellt. Diese stammen von dem sporadischen Anschlagen des Drahts auf dem Boden und an den Einzugsrollen. Features im Frequenzbereich sollen die Erkennung der Kerben verbessern. Das gelingt mit einer Berechnung des hochfrequenten Anteils (High Frequency Content, HFC), vgl. Abb \ref{SpectralFeatures.png}.

![Hochfrequenter Anteil der Messung mit künstlichen Kerben \label{SpectralFeatures.png}](images/SpectralFeatures.png)

Die Kerben können durch einen höheren hochfrequenten Anteil von anderen Impulsen getrennt werden. Beim Anfahren der Maschine liegt ebenfalls ein Impuls mit sehr hochfrequentem Anteil vor, welcher falsch erkannt werden würde. Daher müssen mehrere Features und die Betriebsparameter der Ziehmaschine berücksichtigt werden. Im Anschluss werden diese Features mit Varianzanalysen und weiteren statistischen Methoden auf ihre Unabhängigkeit untersucht. Die besten Features werden als Eingangsdaten für die ML-Modelle verwendet.

**Meilenstein 1:** Die Sensorpositionen wurden definiert und die handelsübliche Hardware implementiert und getestet. Die elektronischen Schnittstellen werden im Laufe des AP 5 finalisiert.

## Auswertung und Algorithmenentwicklung

### Merkmalsidentifizierung und -interpretation - statistische Analysen der Maschinen- und Prozessdaten

Viele psychoakustische Features lassen sich nicht direkt für Acoustic-Emission im hochfrequenten Messbereich verwenden, da diese für den vom Menschen hörbaren Bereich definiert sind. Ein Beispiel dafür ist die A-Bewertung, bei der das Spektrum der gemessenen Schalldruckpegel mit einer frequenzabhängigen Gewichtung, die dem menschlichen Gehör nachempfunden ist, multipliziert wird [@ArbeitsringLarmDEGA].

Als signalanalytische Merkmale für die Zustandsüberwachung des Drahtziehprozesses werden deshalb Kennwerte verwendet, welche an die Definition psychoakustischer Features angelehnt sind.
Zur Beurteilung der Impulshaftigkeit des gemessenen Signals werden folgende Features verwendet: Crest-Factor, K-Factor, Impulse-Factor, Margin-Factor, Shape-Factor, Clearance-Factor, Kurtosis, Skewness [@SignalFeaturesMATLAB, @caesarendraReviewFeatureExtraction2017]. Die Impulshafigkeit kann objektiv zur Zustandsüberwachung verwendet werden und ist ein übliches psychoakustisches Merkmal [@yannikPsychoakustikPsychoakustikEffekte]. Neben der Impulshafigkeit des Signals wird die Schärfe berücksichtigt, bei der der hochfrequente Energieanteil mit der Gesamtenergie des Signals verglichen wird [@SoundQualityAlgorithms, @kaneApplicationPsychoacousticsGear2016].

#### Erprobung verschiedener Netzwerkarchitekturen und Machine-Learning Techniken an relevanten Ausfallmechanismen

Im vorliegenden Projekt soll erkannt werden, wann der Drahtziehprozess vom Referenzzustand abweicht und die Abweichungen sollen bekannten Schadenstypen zugeordnet werden.
Die Erkennung des Referenzzustands und der Abweichungen von diesem entsprechen der Anomalieerkennung. Die darauffolgende Erkennung vorliegender Abweichungen ist eine Klassifikationsaufgabe.

Es existieren verschiedene kategorische Ansätze zur Anomalieerkennung, z.B. distanz- oder dichtebasierte Methoden [@smiti_critical_2020, @tayeh_distance-based_2020, @lou_local_2015].
Dabei liefern Ansätze aus dem Deep Learning Bereich insbesondere der Autoencoder verlässliche Ergebnisse [@pang_deep_2022, @shao_novel_2017, @zhou_anomaly_2017, @longari_cannolo_2021, @maleki_unsupervised_2021, @saumya_spam_2022].

Empirische Untersuchungen seitens AMI demonstrieren, dass LSTM basierte Auto Encoder für die Überwachung des Drahtziehens auf Basis der AE die höchste Genauigkeit aufweisen [@liu_arrhythmia_2022, @bli22_binli826lstm-autoencoders_2021-1, @said_elsayed_network_2020].

Für das Klassifikationsproblem existieren diverse Lösungsansätze, jedoch ist es im Hinblick auf das propagierte zweistufige Analyseverfahren und der Minimierung des Rechenaufwands sinnvoll, die bereits durch den Encoder reduzierte Datenrepräsentation der Eingabedaten aus dem Latent Space (vgl. Kapitel \ref{}) für die dadurch weniger rechenintensive Klassifikation zu nutzen [@abiodun_state---art_2018, @sen_supervised_2020].

Im vorliegenden Projekt werden unterschiedliche Autoencoder Modelle und deren Netzwerkanasätze erprobt. Diese lassen sich in Abbildung \ref{modelnet.pdf} darstellen.

:::![Autoencoder Netzwerkarchitktur\label{modelnet.pdf}](images/modelnet.pdf)

#### Extrahierung von Kenngrößen und Merkmalen für Prozessfehler

Eine repräsentative Auswertung der Zeitrohdaten in Abbildung \ref{time90kerben.pdf} zeigt, erwartete Kerben in den gelben Bereichen, teilweise treten dort Impulse oder Minima auf. Eine umfassende Analyse zeigt hier allerdings kein verlässliches Muster. Es wird angenommen, dass die vorliegenden Kerben zu unterschiedlich ausgeprägt sind. Der Wiener Filter (grüne Kurve) zeigt eine deutliche Wirkung zur Extraktion impulshaltiger Ereignisse.

![Zeitreihen mit Kerben\label{time90kerben.pdf}](images/time90kerben.pdf)

Um eine effiziente Analyse des Drahtziehprozesses zu ermöglichen, wird für die KI-gestützten Verfahren eine Auswahl an relevanten Features getroffen. Es wird eine Teilmenge der am wenigsten korrelierenden Features, also jene Merkmale mit der größten stochastischen Unabhängigkeit voneinander, ausgewählt.

Diese Auswahl erfolgt anhand statistischer Verfahren, wie der Varianzanalyse oder dem Chi-Quadrat-Test. Damit ergeben sich die folgenden besten acht Features für die Anomalieerkennung (Stufe 1, Abweichung vom Referenzzustand) und Schadenstypisierung (Stufe 2, Fehlerklassifikation) des Drahtziehprozesses:

- Crest Factor
- Mean
- Signal Strength
- Hit Peak
- Hit Energy
- Power Mean
- HFC
- Spectral Peak

#### Schwellwerte psychoakustischer Features v.s. Autoencoder

Die psychoakustischen Features lassen sich in in Abbildung \ref{} durch einen paarweisen Plot gegenüberstellen. Die Einfärbung erkannter Impulse gegenüber zeigt, ...

Gegenüber dem folgenden Autoencoder ist das Schwellwertverfahren ...

#### Statistische Auswertung der Messergebnisse und Beurteilung der Zuverlässigkeit

Die vorliegenden Messreihen und die skalierten Features lassen sich übergreifend durch eine Reihe von Boxplots vergleichen. Hiermit kann die Verteilung der Datenpunkte ...

#### Entwicklung einer geeigneten Darstellungsform bei auftretenden Fehlerereignissen

Neben der Datengrundlage und der Architektur für die Zustandsüberwachung wird die Visualisierung im Laufe des Projekts stetig weiterentwickelt. Dabei fließt bei Abstimmungsmeetings und bei den Messterminen das Feedback aller Projektteilnehmer ein. Durch den Einsatz bei den Messungen kann die Praxiseignung aus Sicht der Messingenieure, des Maschinenbedieners und der Softwareentwickler validiert werden. Die Auswahl der Features in \ref{ap6} wird auf Basis der vorangegangen Featureanalyse getroffen.

### Anlernen einer KI\label{ap5}

#### Zweistufiges Analyseverfahren

Die Erkennung des Referenzzustands und der Abweichungen von diesem während des Drahtziehprozesses bildet die erste Stufe des KI-gestützten Analyseverfahrens. Für die darauffolgende zweite Stufe des Anaylseverfahrens, die Einteilung bzw. Zuordnung in vordefinierte Abweichungen oder Schadenstypen, ist ein geeignetes Klassifikationsverfahren nötig.

Autoencoder sind neuronale Netze, welche aus einem Encoder und einem Decoder, bestehen. Während die Einsatzgebiete sowie die architektonische Beschaffenheit von Autoencodern variieren, ist der zugrunde liegende Funktionsmechanismus immer ähnlich.
Die Funktionsweise eines Autoencoders besteht darin, den zugeführten Input zu komprimieren und aus dieser reduzierten Repräsentation, das ursprüngliche Eingangssignal so exakt wie möglich aber nicht identisch, wieder auszugeben.
Da das neuronale Netz durch die Transformation in einen niederdimensionaleren Raum und zurück in die Ausgangsdimension zur Gewichtung der Informationen gezwungen wird, werden nur (vermeintlich) nützliche Eigenschaften und versteckte Abhängigkeiten in den Daten gelernt.

Die verwendete Autoencoder-Architektur basieren beide auf dem Long Short-Term Memory (LSTM), einer speziellen Version eines rekurrenten neuronalen Netzes. Der Autoencoder wird auf die Erkennung des Normalzustand beim Drahtziehprozesses angelernt. Dieses Anlernen ist ein iterativer Prozess welcher stetig die Genauigkeit und Robustheit des Modells gegenüber Fehlern steigert.

Die markantesten Features (vgl. Abschnitt \ref{}) werden für das Training verwendet und als Dateninput in das neuronale Netz gespeist. Mit der Wahl eines geeigneten Fehlermaßes (loss-function), z.B. der mittleren quadratischen Abweichung (MSE) kann die Größe des Fehlers (loss) zwischen rekonstruierten und tatsächlichen Eingangsdaten berechnet werden.
Anschließend wird der Gradient dieser loss-function gebildet und die internen Gewichtungen zwischen den einzelnen Neuronen so optimiert, dass sich der numerische Fehler bei einem erneutem Durchlauf der gleichen Inputdaten minimiert.
Da der Autoencoder mit fehlerunbehafteten Daten gespeist wird, ist dieser nach dem Training in der Lage, den normalen Arbeitsprozess, repräsentiert durch die beschriebenen Features, bis zu einem gewissen Fehler zu erkennen. Dieser Fehler, bzw. das Resultat der loss-function, kann als Schwellenwert für die Anomalieerkennung genutzt werden, welcher die Klassifizierung auslöst.

#### Klassifizierungsstufe

Das zur Klassifikation verwendete neuronale Netz erhält die komprimierten Datenrepräsentationen aus dem latent space beider Autoencoder als Eingangsdaten und gibt nach der Verarbeitung einen Vektor aus, welcher die Zugehörigkeitswahrscheinlichkeit zu jeder Klasse enthält.
Dieses Netzt besteht aus mehreren Dense Layer, von denen das letzte Output Layer die normalisierte Exponentialfunktion (vgl. \ref{eq:softmax}) (Softmax-Funktion) als Aktivierungsfunktion verwendet, um die Komponenten des Ausgabevektors in den Wertebereich von (0,1) zu transformieren (welche in Summe 1 ergeben), um so die entsprechenden Wahrscheinlichkeiten für die unterschiedlichen Kategorien der Fehlertypen zu berechnen.
Für das Training dieser Architektur wird die Kreuzentropie ausgenutzt. Aus dem ausgebenen Wahrscheinlichkeitsvektor und dem sogenannten one-hot-codierten Vektor mit der tatsächlichen Klassenzugehörigkeit wird über die Kreuzentropie der Fehler bzw. der Cross Entropy Loss (vgl. \ref{eq:crossentropy} berechnet.
Wie bereits beim Autoencoder wird der Gradient dieser Funktion mittels Fehlerrückführung verwendet, um die Gewichtungen des neuronalen Netzes zu aktualisieren.

### Optimierung der Rechenleistung

Um die Rechenleistung zu optimieren, wird das Speichern der Zeitdaten, die Berechnung der Features und die Anwendung der Machine Learning Modelle in seperate Prozesse aufgeteilt, die parallel ausgeführt werden und die Ressourcen optimal nutzen. Außerdem erfolgt die zweite Stufe des Analyseverfahrens, die Klassifizierung der Abweichung vom Referenzzustand nur bei Bedarf.
Die Datenspeicherung erfolgt zusätzlich asynchron. Dadurch können die Daten in dem Zeitraum abgespeichert werden, bis von dem Messsystem ein neuer Block an Messdaten vorliegt.
Für die Berechnung der Features werden optimierte Algorithmen und aktuelle python-Bibliotheken verwendet, wie z.B.: numba  oder cpython [@NumbaHighPerformance].
Durch diese und weitere Optimierungsschritte ist die Sofware, auf der das Condition Monitoring System basiert, effizient und ressourcenschonend.

>MS 3: Funktionsfähige Algorithmen liegen vor, die die strukturdynamische Detektion von Fehlermustern ermöglichen.

## Integration der Sensorik in die Versuchsanlage

Das Arbeitspaket wurde anstatt der Piezosensorik unter Verwendung handelsüblicher Acoustic Emission Sensoren durchgeführt.

### Funktionalitäts- und Zuverlässigkeitsbewertung der Algorithmen

- Architektur bewerten
- Kleine Bilder-Tabelle mit den Lernkurven unterschiedlicher Encoder
- Abweichung von Hammer (bzw. Impuls)

### Erprobung der Zustandsüberwachung, basierend auf den zu entwickelnden Selbstlernfähigkeiten

:::

Der Aufbau der verwendeten LSTM-Zelle ermöglicht das Mitführen von Informationen über einen internen Zustand über mehrere Zeitschritte ermöglicht.

- Trigger selbständig auslösen

### Erprobung einer neuartigen psychoakustischen Überwachung

Die psychoakustischen Features bilden eine wesentliche Grundlage für die Modelle, ...

Folgende Features besonders relevant...

### Vertieftes Training des neuronalen Netzes

Die erarbeiteten Algorithmen werden auf jede neue Messung der Messserien angewendet. Dadurch steigt die Datenmenge der Rohdaten und die Datenmenge der daraus abgeleiteten Features. Die vergrößerte Datenmenge hat einen direkten positiven Einfluss auf die Genauigkeit der Modelle. Aufgrund dieses Zusammenhangs muss auch mit jeder zusätzlichen Messung und Trainingsiteration eine erneute Anpassung des  Schwellenwerts vorgenommen werden.
Um die Qualität der zustandsüberwachenden Systeme besser beurteilen zu können, werden die trainierten Modelle der letzten Iteration unter realen Bedingungen an einer neuen Messung getestet.
Anhand dieser kann die Präzision genauer überprüft und bei Bedarf der Schwellenwert feinjustiert werden. Die Messung und die Ergebnisse werden weiterhin in einer Datenbank gespeichert, welche relevant für zukünftige Trainingsiterationen ist.
Die Ergebnisse der Anomalieerkennung, also die Unterteilung in fehlerunbehafteten Referenzzustand und Erkannten, aber nicht näher bestimmten Fehler im Arbeitsprozess, ist die entscheidende Datengrundlage für das darauffolgende Training des Klassifizierers.
Somit kann erneut eine Verbesserung an der Architektur und deren Präzision vorgenommen werden, bis die gewünschte Genauigkeit beider Stufen des Analyseverfahrens erreicht ist.

### Validierung des kompletten Überwachungssystems unter relevanten Einsatzbedingungen

Da trotz vielfacher Anpassungen des Sensorkonzepts **der TUC** nicht die erforderliche Sensitivität für ein CMS erreicht werden konnte, kann angenommen werden, dass die zugrundeliegende Integration von Piezoelementen als sensorische Einheit für den spezifischen Anwendungsfall „Drahtziehen“ ungeeignet ist. Es wurde daher im Konsens mit dem Projektkonsortium beschlossen, dass das CMS unter Verwendung handelsüblicher AE-Sensoren entwickelt und finalisiert wird. Die Untersuchungsergebnisse deuten jedoch auch darauf hin, dass das entwickelte Sensorkonzept in dünnwandigen Strukturen funktionsfähig ist und eine ausreichende Sensitivität für CMS-Anwendungen aufweist.

#### Bewertung der mathematischen und akustischen Modelle

Die verwendete Pipeline und die Autoencoder sind für die Verschleißerkennung vollständig einseztbar. Die Erkennung der Kerben ist aufgrund fehlender Datenmenge  ...

#### Validierung des Modellansatzes und der Algorithmen

- Autoencoder flexibel
-

#### Erfassung der Messwerte der unterschiedlichen Einfluss- und Bewertungsgrößen

Einflüsse:

- Äußere Impulse
- Abwicklerverzug
- Drahtverschmutzung
- Teilschmierung

Bewertungsgrößen

- Optische Prüfeinheit
-

#### Analysen bestehender Wechselwirkungen

- Abhängigkeit der Ziehgeschwindigkeit
- Einfluss von Störungen

### Ableitung von Potenzialen zur Verbesserung der Modelle

Bei längeren Einsätzen des CMS´s und bei Verwendung verschiedener Ziehmaschinen könnten mehr Daten gewonnen werden. Mit diesen Daten könnten die Machine Learning Modelle trainiert und bezüglich ihrer Performance stabiler und akkurater werden.
Mit einer Inline-Qualitätskontrolle könnten die gemessenen Daten objektiv und automatisch gelabelt werden. Dies würde eine manuelle Aufbereitung der Daten vor dem Training der Modelle vermeiden und die Dauer zwischen Messung und neuen Modellen erheblich verkürzen. Die Aufbereitung könnte dann komplett automatisiert erfolgen.

Da bei den Messserien kein Sensordefekt auftrat, wird ihre Eintrittswahrscheinlichkeit als gering eingeschätzt.
Das Drahtziehen erzeugt Körperschall mit hoher Energie und ein Sensordefekt würde sich durch einen deutlichen Energieabfall im Messsignal zeigen. Dies würde in Featurewerten, die erheblich von denen des Referenzzustandes abweichen, resultieren und die Machine Learning Modelle würden einen Fehlerzustand erkennen.
Für einen Dauereinsatz in der Industrie sollte der handelsübliche AE-Sensor, oben an der Ziehsteinkassette montiert werden und das Kabel zum Messsystem durch eine Einhausung geschützt werden.

> MS 4: **Die** Demonstration einer erfolgreichen Fehlerdiagnostik mittels neuentwickelten Piezosensoren und **innovativer** Algorithmen wurde teilweise erreicht:
>
> - Fehlerdiagnostik wurde demonstriert, jedoch ohne neuentwickelter Piezosensorik

## Konzipierung der CMS-Pakete\label{chap:CMSGUI}

### CMS Paket S und M

Die durchgeführten Messserien zeigen, dass sowohl für das CMS-Paket S als auch für das Paket M ein AE-Sensor an der Ziehsteinkassette für die Zustandsüberwachung genügt. Bei Ziehprozessen mit mehreren Ziehstufen wird pro Stufe an der jeweiligen Ziehsteinkassette ein Sensor benötigt, um ein Lokalisieren auftretender Fehler zu ermöglichen.
Bei dem Basis Paket S werden dem Bediener Änderungen in den Zustandsdaten deutlich angezeigt. Mittels einer Visualisierung im Stil einer Ampel wechselt der Zustand von Grün über Orange zu Rot. Bei Orange ist eine Kontrolle nötig und ein baldiges Eingreifen des Bedieners wahrscheinlich. Sofortmaßnamen, wie z.B. ein Stoppen der Maschine ist bei Rot nötig. Überschreiten die Kennwerte, die voreingestellten Grenzen oder sind kurz davor dies zu tun, ist dies für den Bediener sofort ersichtlich und er kann rechtzeitig darauf reagieren.
Das CMS-Paket M erweitert das Paket S um Vorschläge für den Benutzer, die ihm helfen, Einstellparameter so zu verändern, dass der Prozess wieder in den Gutbereich gelenkt wird. Dazu werden die Featurewerte in dem oben dargestellten zweistufigen Verfahren mittels Machine Learning Modellen klassifiziert. Zu jeder bekannten Schadensklasse sind entsprechende Vorschläge, zur Vermeidung des Schadens, hinterlegt, die bei Bedarf angezeigt werden. Dadurch kann schnellstmöglich in den Prozess eingegriffen und Fehlproduktionen vermieden werden.

Im Industrieeinsatz können die Modelle um neu auftretende Schadensklassen erweitert werden und in Absprache mit KIES oder der Fachabteilung vor Ort können Hilfestellungen für den Maschinenbediener erarbeitet werden. So wird eine stetige Verbesserung des CMS gewährleistet.

Für die Umsetzung der Mensch-Maschine-Schnittstelle wird eine graphische Benutzeroberfläche (GUI) entwickelt.
Aufgrund folgender Vorteile wird die Programmiersprache QT verwendet: Open-Source-Software, Cross-Plattform-Support, High Performance und Objekt-Orientierter Ansatz.
QT unterstützt alle üblichen Interaktionen des Bedieners über Tastatur, Maus und Touchscreen. Ferner ist QT unabhängig vom Betriebssystem, dass bedeutet, die Benutzeroberfläche kann direkt für verschiedene Zielsysteme entwickelt werden.
Da QT sowohl für Echtzeitanwendungen als auch auf embedded Systeme erfolgreich verwendet wird, ist diese Programmiersprache sehr gut für den Anwendungsfall im Rahmen dieses Forschungsprojektes geeignet [@mezeiCrossplatformGUIEducational2017, @tanEmbeddedLightweightGUI2018].
Der Fokus der Entwicklung der Benutzerschnittstelle liegt darauf, dass die GUI für die Benutzer einfach in der Handhabung ist und auf dem neuesten Stand der Technik basiert. Diese beiden Punkte können entscheidend für die Akzeptanz der GUI und für mögliche Wettbewerbsvorteile sein [@granadoCreatingRichHumanmachine2015].

#### Aufbau Graphical User Interface für den Maschinenbediener

Die inhaltlichen Komponenten der GUI konzentrieren sich auf die für den Bediener der Drahtziehanlage wesentlichen Informationen. Die Auswahl, Gestaltung und Anordnung der User Interface Elemente orientieren sich dabei an DIN EN ISO 9241-161 [@DINISO9241161a]:

**Einfaches Design**

Die Benutzeroberfläche ist übersichtlich strukturiert und auf die wesentlichsten Kenndaten für die Prozessüberwachung beschränkt. Die eingesetzten Elemente teilen sich auf verschiedene Registerkarten (vgl. \ref{GUImain.pdf}) auf. Auf die Eingabeelemente, welche klar sichtbar sind, kann leicht zugegriffen werden.

![GUI Hauptansicht \label{GUImain.pdf}](images/GUImain.pdf)

**Zielgerichtetes Seitenlayout**

Das Seitenlayout für die erste Registerkarte beginnt mit einer Visualisierung- und Eingabemaske der Einstellungen für die Messung und Grenzwerte der Features für den Maschinenbediener. Diese sind abhängig von dem gewählten Prozess und Material. Die Einstellungen werden bei Installation des Systems initial festgelegt. Die Grenzwerte der Features und des Schwellenwertes für die Machine Learning Modelle werden automatisch, z.B. tagesweise, geupdatet. Im unteren Bereich wird die Einhaltung der angegebenen Grenzwerte, in Anlehnung an eine Ampel, sowie das Klassifizierungsergebnis angezeigt. Die Klassifizierung durch Machine Learning Modelle ist nur Bestandteil des CMS Pakets M. Im Paket S werden die Features tagesweise statistisch ausgewertet und Grenzwerte bestimmt, die der Benutzer bei Bedarf anpassen kann.

**Hierarchische Struktur**

Die Anordnung und der Inhalt der Registerkarten richten sich nach Relevanz sowie der voraussichtlichen Nutzungshäufigkeit der Elemente. Beginnend von links mit den wichtigsten Einstellungen, folgen anschließend die Registerkarten für eine Live-Darstellung der Features (vgl. \ref{FeatureLive.pdf}), ein Spektrogramm (vgl. \ref{SpekLive.pdf}) sowie die weiteren Maschinen- und Eventdaten (vgl. \ref{MaschinenData.pdf}).

![Liveplot der Features \label{FeatureLive.pdf}](images/FeatureLive.pdf)

![Livedarstellung eines Spektogramms \label{SpekLive.pdf}](images/SpekLive.pdf)

![Anzeige der aktuellen Betriebsparamter der Ziehmaschine \label{MaschinenData.pdf}](images/MaschinenData.pdf)

## Literaturverzeichnis{-}
