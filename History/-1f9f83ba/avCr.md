## Einleitung

- Ein Bauteil oder Werkzeug meldet sich automatisch bei Beschädigung oder Verschleiß, die Maschine bestellt selbständig neues Material. 
- Zur Erfassung solcher Zustände werden moderne, smarte Sensoren benötigt.
- verfügbare Lösungen am Markt sind abhängig von der Applikation
- Prozessüberwachung, Optimierung und Qualitätsicherung für kostenoptimale und kundengerechte Drahtziehanlage
- Condition Monitoring System um Störgen aus dem Klangbild der Maschine durch Signalanalyse zu extrahieren

Projektantrag oder Zwischenbericht

## Wissenschaftlich-technische Ergebnisse und andere wesentliche Ereignisse

Angestrebt werden kundenspezifische Condition Monitoring Systeme die sich je nach Funktionalität in Systembaukästen mit drei verschiedenen Umfängen untergliedern lassen, wobei die größeren Pakete immer die Funktionalitäten der kleineren Pakete beinhalten:

- Paket S (small)
  - Bereitstellung und Visualisierung der aufbereiteten Messdaten
  - Schnittstelle zur Messdatenübermittlung an den Hersteller
- Paket M (middle)
  - Fehleranalyse/-diagnosen
  - Handlungsempfehlungen
  - Schnittstelle zur Datenübermittlung an den Hersteller
- Vorbereitung zu Paket L (large)
  - Selbstdiagnose
  - Automatisierter Eingriff in die Maschinensteuerung
  - Wartungsempfehlungen

- Druch Low-Cost Sensorintegration, Bewertungsstudien, Merkmalsextraktion und -identifikation kombiniert mit effizienten Auswertealgorithmen soll diese Pakete umgesetzt werden.
- Entwicklungskerngebiete liegen im Bereich von Acoustic-Emission werden bisher nur für impulshaltige Geräusche verwendet.
- Überwachungsmethode entwickeln, die den Zusammenhang zwischen Maschinenparametern und Verschleißerscheinungen am Zieh-/Schälwerkzeug angemessen erklärt

### AP-1 Anforderungs- und Zieldefinition Maschine

#### Zielsetzung

Die vom System zu erfassenden Zustände, Fehler und Daten werden eingegrenzt und klassifiziert.Des Weiteren wird unterschieden bei der Bereitstellung der Daten in Echtzeit, nach Notwendigkeit oder nach Abfrage. Im Entwicklungsprozess können sich weitere Anforderungen oder Randbedingungen ergeben, welche für eine spätere Übertragbarkeit auf weitere Anlagen mit zu erfassen sind.

#### Evaluierung relevanter Einflussgrößen sowie Erarbeitung einer Einflussmatrix

<!-- TODO Zusammenfassung und Update-->
Evaluierung relevanter Einflussgrößen sowie Erarbeitung einer Einflussmatrix (AP 1.1, AMI 1/3 PM)
Ein Katalog der Betriebszustände und zugehöriger Fehlerbilder vom Projektpartner Kieselstein
dient als Grundlage für die Einflussmatrix und die Auswahl der zu untersuchenden Störungen.
Diesen hat AMITRONICS um eine Abschätzung zur Diagnosefähigkeit der Drahtzugfehler
erweitert. Grundsätzlich lassen sich zwei Detektionsklassen unterscheiden: Schäden welche sich
durch transiente Ereignisse kennzeichnen und andere, zumeist verschleißbedingte, welche zu
einem dauerhaften Anstieg der Schallleistung führen. Zur Ersteren zählen Knicke und Kerben im
Draht und transiente Änderungen am Ziehstein, wie Ausbrüche. Eine unzureichende Schmierung
des Prozesses mit zu wenig Ziehseife lässt die Schallleistung hörbar ansteigen.
In Planungsrunden mit den Konsortialpartnern werden Störgrößen ausgewählt, welche sich
synthetisch reproduzieren lassen. Zur Plausibilitätsprüfung werden natürlich verschlissene
Werkzeuge herangezogen. Zur realitätsnahen Abdeckung des Produktionsspektrums werden
vorhandene Drahtcoils mit unterschiedlichen Zugfestigkeiten (C90, 54SICR6, S235JR, 100CR6,
X2CrNiMoN22-5-3) verglichen. Außerdem werden verschiedene Ziehgeschwindigkeiten,
Einzugswinkel, Schmierzustände und Querschnittreduktionen untersucht. Ein möglichst großer
Abdeckungsbereich führt zu stabileren und damit praxisorientierten Klassifikationsmodellen. Der
Ablauf wird in einem Messplan festgehalten (vgl. Messplan.xlsx).
Es gibt zwei wesentliche Drahtzugmethoden: Ziehen und Schälen. Auf den Schälbetrieb wird
verzichtet, da der Ziehbetrieb in der Industrie häufiger eingesetzt wird. Zusätzlich ergeben erste
Messungen, dass die Störquellen im Körperschallsignal beim Schälen dominanter sind als im
Ziehbetrieb. Denn der Materialabtrag und die zusätzlich benötigten Aggregate erzeugen
Störgeräusche. Dies ist beispielhaft an den Messergebnissen an der Sensorposition 7, am
Gehäuse der Ziehsteinkassette, dargestellt. (vgl. Betriebsmessungen_S7.png).

#### Definition der Funktionseinheiten

<!-- TODO Zusammenfassung und Update-->
Zur Vernetzung der Maschinensteuerung mit dem vibroakustischem Messsystem, kurz VAM, einer
grafischen Benutzerschnittstelle und den Datenbanken wird der Industriestandard OPC UA
bestimmt. AMITRONICS erstellt ein Pflichtenheft bezüglich der Hard- und Software zur Definition
der Funktionseinheiten. In diesem sind die Komponenten, Schnittstellen und Anforderungen aller
Projektpartner detailliert beschrieben (vgl. Funktionseinheiten_Schnittstellen.docx).
Das Gesamtsystem wird in Prozessleitebene, Komponentenebene und Sensorebene
aufgeschlüsselt (vgl. Abb. System_Ebenen.png). In der angehängten Darstellung werden die
Bearbeitungsstände farblich (grün=erledigt, orange=in Arbeit, rot=offen) dargestellt

### Umfassende strukturdynamische Analyse der Versuchsanlage zur Charakterisierung der relevanten Maschinen- und Prozesszustände

#### Experimentelle Modalanalyse

<!-- TODO Zusammenfassung und Update-->
Die Vorauswahl der Sensorpunkte wird an den geometrischen Randpunkten der Struktur so
gewählt, dass eine möglichst steife Anbindung bei geringen Nichtlinearitäten sichergestellt
werden kann. Da die Versuchsanlage einen massereichen Aufbau und eine hohe Steifigkeit
aufweist, ist eine externe Anregung mit ausreichend hoher Amplitude in den gemessenen
Beschleunigungssignalen nur schwierig umsetzbar. Eine qualitative Untersuchung zeigt, dass die
Strukturresonanzen für die Untersuchungen im Ultraschallbereich nur eine untergeordnete Rolle
spielen. Das Schwingungsverhalten der Versuchsanlage und die gewählten Sensorpositionenwerden in einer umfangreichen Betriebsschwingungsmessung analysiert. Die AMITRONICS
entscheidet sich an Stelle einer vertieften Modalanalyse die Übertragung von Acoustic Emission
Ereignissen auf Basis des HSU-Nielsen-Test durchzuführen. Dieser Test wird auch als
"Bleistiftminentest" bezeichnet. Dabei wird beim Brechen einer Bleistiftmine mit definierter Länge
ein reproduzierbarer Nadelimpuls erzeugt. Die Impulsfunktion entspricht näherungsweise einer
Dirac-Funktion, welche eine stetig, lineare Impulsantwort im Spektrum erzeugt. Durch mehrere
Mittelungen und einen definierten Bruchvorgang kann die Amplitude als Referenzwert für die
korrekte Funktionsweise der AE-Sensoren und zur Bestimmung des Übertragungsverhaltens
verwendet werden. Bei Acoustic Emission Sensoren wird im Gegensatz zu
Beschleunigungsaufnehmern die Eigenfrequenz des Piezokristalls genutzt, womit der
Frequenzgang nicht linear ist.
Zur Festlegung des Arbeitsbereichs der zu entwickelnden Sensoren werden Acoustic-Emission
Hits (transiente Burstsignale) gemittelt und mit dem Ruhepegel verglichen. Die abgebildeten AEEvents werden durch Kerben im Draht erzeugt. Der Ruhepegel zeigt die Resonanzfrequenz des
Sensors bei 150 kHz und die Geräusche der Aggregate unterhalb von 100 kHz. Die
Impulsantworten der Kerben sind im Frequenzbereich mit ausreichendem Signalrauschabstand
(von 20 dB) bis etwa 400 kHz sichtbar. Daher wird eine obere Frequenzgrenze von 400 kHz und
damit eine Abtastrate von 1 MHz festgelegt. (vgl. Ruhepegelabgleich.png)

#### Betriebsschwingungsmessungen

<!-- TODO Zusammenfassung und Update-->
Der Umformvorgang des Drahtes findet innerhalb des Ziehsteins statt. Damit stellt die lokale
plastische Verformung die Hauptschallquelle und den Entstehungsort der Burst Signale dar.
Deshalb sollten die Sensoren so nahe wie möglich am Ziehstein angebracht werden. Im weiteren
Projektverlauf wird der Sensor der TU Chemnitz direkt in eine Nut in der Ziehsteinmatrix
eingepresst. Für eine hohe Vergleichbarkeit bei den ersten Messungen (Messreihe 2-4) wird der
Sensor der TU Chemnitz seitlich an die Ziehsteinmatrize geklebt. Der Referenzsensor (Pos. 3) wird
zum späteren Abgleich der Messsignale durch Magnetbügelhalter an der Matrize montiert (vgl.
Sensorpositionen_Sensorvergleich.png). Die Messungen an den gewählten Sensorpositionen
werden sowohl mit als auch ohne Draht durchgeführt.

Die spektralen Leistungsdichten der Messreihe 4 "Normalbetrieb mit Störungen" (vgl.
Spektrale_Leistungsdichten_Zeitverlauf_Messreihe_4.png) werden zur Validierung der
Sensorpositionen herangezogen. In der Abbildung entsprechen die Nummern der Sensoren
VS900 den Sensorpositionen. Der Sensor 1 der TU Chemnitz befindet sich an Sensorposition 5
und der Sensor 2 der TUC an Position 6. An dem Messpunkt 7 ist der VS150M montiert.

Insgesamt sind 8 Sensoren an der Versuchsanlage montiert. Davon sind fünf VS900, ein VS150,
sowie zwei erste Testsensoren der TU Chemnitz appliziert. Wobei die Nomenklatur der
kommerziellen Sensoren die Resonanzfrequenzen bei 900kHz und 150kHz beschreibt. An
Sensorposition 1, der Trommelanbindung, gibt es keine zeitliche Korrelation zur Störung. Gleiches
gilt an Position 2, der Schälsteinmutter. Im Messsignal des Sensors VS900 an der zukünftigen
Messposition S3 sind Kerben im Draht erkennbar. Bei dieser Messung zeigt der Sensor 1 der TU
Chemnitz keine zeitlichen Ereignisse, sondern ein verrauschtes Frequenzspektrum über den
gesamten Zeitverlauf. TU Chemnitz Sensor 2 hat hier noch Probleme im hochfrequenten Bereich.
Der Sensor VS150M ist hier fehlerhaft. Zum folgenden Messtermin wird untersucht, ob dieser
Sensor einsetzbar ist.Mit Betriebsschwingungsanalysen kann die Anregung der einzelnen Aggregate separat an
mehreren Messpunkten ausgewertet werden. Eine Superposition der Haupt- und
Nebenschallquellen zeigt die relevanten Betriebsschwingformen und die Verschiebung der
vorherrschenden Resonanzfrequenzen. Durch die manuelle Quellentrennung der Aggregate kann
eine blinde Quelltrennung mittels maschineller Lernmethoden validiert werden.

Die größte Amplitude (über alle Messpositionen), exemplarisch an S7 dargestellt, tritt während
dem Betrieb des Spänebrechers auf (vgl. Betriebsmessungen_S7.png). Der Schälbetrieb und
Späneförderungsbetrieb ist in der Amplitude und den Betriebsschwingformen vergleichbar. Die
Kühlung, Hydraulik und Schmiermittelaggregate sind in der Amplitude vernachlässigbar. Da diese
Komponenten sowohl beim Ziehen als auch beim Schälen aktiv sind, ist es vorteilhaft, dass ihr
Störgeräuscheinfluss nicht dominant ist. Der Ziehbetrieb zeigt Strukturresonanzen mit deutlich
geringerem Grundrauschen. Aufgrund dieser Erkenntnis und der höheren Praxisrelevanz wird im
Folgenden nur der Ziehbetrieb weiter analysiert.
Um die Transferfunktion zwischen Draht und dem Sensor an der Matrize zu bestimmen wird der
HSU-Nielsen Test verwendet. Als Anregungspunkte werden mehre Positionen am Draht und der
Versuchsanlage verwendet. Pos. 0 mm ist an der Ziehsteinkassette direkt am Sensor. Die weiteren
Punkte sind entgegen der Laufrichtung des Drahtes mit Koordinatenursprung an Pos. 0 mm
angegeben. Die Kopplungsimpedanz zwischen Draht und Ziehstein führt zu einer
Amplitudenverringerung von 20 dB über das gesamte Spektrum. Weitere Dämpfungen treten
über erhöhten Abstand zum Sensor auf

Durch Anregung am Maschinenfundament und am Drahtcoil kann gezeigt werden, dass
Umgebungseinflüsse aufgrund hoher Dämpfungen vernachlässigbar sind. (vgl.
Vergleich_Abklingkurve2.png)

#### Überprüfung der Algorithmen

Schädigungen am Draht werden zum 1. Messtermin aufgezeichnet, diese sind aufgrund von
Messsystemgrenzen nur bis 50 kHz auswertbar. Für folgende Messtermine wird das CMSMesssystem eingesetzt. Die synthetisch erzeugten Störungen sind dennoch bereits sehr gut
ersichtlich (vgl. Spektrale_Leistungsdichte_Vgl_mit_ohne_Störung.png).

Innerhalb der zweiten Messreihe werden unterschiedliche Drahtdurchmesser und Werkstoffe, bei
verschiedenen Vorschubgeschwindigkeiten mit und ohne Störungen abgefahren. Es können auch
spezielle Ereignisse wie Drahtrisse und Rattermarken aufgezeichnet werden. Allerdings kommt es
zu Beginn der Nachauswertung zu einem nicht wiederherstellbaren Datenverlust am
Messrechner. Dadurch verzögert sich die zeitliche Planung im folgenden Arbeitspaket 3 und 4.
Aus der durchgeführten Zeitbereichsanalyse und dem Echtzeit Spektrogramm können einige
Erkenntnisse für eine Wiederholungsmessung gesammelt werden. So ist eine zweite
Plausibilisierung der gemessenen Ereignisse durch eine optische Prüfung nützlich. Daher wird
eine Hochgeschwindigkeitskamera und Mikrofone für die Aufzeichnung der
Umgebungsgeräusche für die wiederholte Betriebsmessung verwendet. Die Verwendung der
Hochgeschwindigkeitskamera ist zusätzlich zum geplanten Arbeitsumfang und soll die zeitlichen
Verzögerungen aufwiegen.
Mit der Kamera soll die gesamte Drahtmantelfläche in Echtzeit synchron zu den AE-Sensoren
geprüft werden. Die Hochgeschwindigkeitskamera wird an zwei Positionen getestet (vgl.
Mess_6_Aufbau.png, Mess_6_Aufbau_Kamera_Pos2.JPG). Es zeigt sich dass, aufgrund von
Reflektion und Verschmutzungen am Draht, sowie der Kameraauflösung keine sinnvolle
Auswertung möglich ist. Ein weiterer Aufbau mit einer neueren Kamera zeigt leichte
Verbesserungen in der Auflösung. Die Bilder sind aufgrund aufwendiger Synchronisation zu den
Messdaten bisher noch nicht ausgewertet.

Außerdem wird ein weiteres Messsystem verwendet, welches den Einsatz weiterer Sensoren und
Mikrofone erlaubt. Die zusätzlichen AE-Sensoren (TUC Sensor 2, VS75V) erhöhen den abgedeckten
Frequenzbereich auf 30 kHz bis 500 kHz. Die Positionierung der Sensoren sind auf einer
Abbildung der ausgebauten Ziehsteinmatrix gezeigt (vgl. Ziehsteinmatrix_Senspos.png). Die
Mikrofone zeichnen den Frequenzbereich bis 20kHz auf. Mit den Audioaufnahmen der Mikrofone
ist ein Abgleich der Fehlerdetektion im Frequenzbereich, den ein Maschinenbediener hört, mit
dem der AE-Sensoren möglich.

Für die folgenden Analysen des quadratischem Mittelwertes (engl. root mean square, RMS) der
Messung wird nun das Signal des VS150M, der oben auf der Ziehsteinmatrix (S3) befestigt ist,
verwendet. Der Mittelwert bezieht sich auf einen Messblock mit 65536 Abtastpunkten. Das
entspricht einer Zeitdauer von 26 ms bei einer Abtastfrequenz von 2,5 MHz. Als erstes wird der
Einfluss der Ziehgeschwindigkeit auf den RMS untersucht (vgl.
Baustahl_Vergleich_RMS_beschaedigter_Ziehstein.png)

Für diese Messungen ist das Drahtmaterial Baustahl und der Ziehstein ist durch Riefen künstlich
beschädigt. Dargestellt sind Messungen mit Ziehgeschwindigkeiten von 30, 60, 90 und 120 m/min.
Es ist erkennbar, dass mit höheren Ziehgeschwindigkeiten, der RMS dauerhaft einen höheren
Wert annimmt. Da während dem Ziehprozess mit beschädigtem Ziehstein Schwankungen
auftreten, ist der RMS-Wert über die Dauer die Messung nicht konstant. Es wird ersichtlich, dass
der RMS-Wert nicht proportional mit der Ziehgeschwindigkeit zunimmt. Bei höheren
Ziehgeschwindigkeit ist der Anstieg des RMS geringer, obwohl die Geschwindigkeit um den
gleichen Betrag erhöht ist.

Die zweite Darstellung des RMS, zeigt diesen für Betriebsmessungen beim Ziehen von Baustahl
bei 30 m/min. Vergleichend sind Messungen im Gesundzustand, bei Kerben im Ausgangsdraht
und bei einem beschädigtem Ziehstein gezeigt. Der beschädigte Ziehstein verursacht einen
deutlich erhöhten RMS-Wert. Dagegen kann durch eine Betrachtung des quadratischen
Mittelwertes nicht zwischen dem Gesundzustand und einem Ziehprozess mit einzelnen Kerben im
Draht unterschieden werden.

Abschließend wird eine Analyse des RMS hinsichtlich der Auswirkung von verschiedenen
Drahtmaterialien (vgl. Vergleich_RMS_Ziehmaterialien.png) durchgeführt. Für diese Messung wird
mit einem Vorschub von 30 m/min gezogen und der Ziehstein ist unterschiedlich stark
beschädigt. Für die verschiedenen Materialien sind in dieser Messreihe keine gleichen
Ausgangsdurchmesser vorhanden. Deshalb ist die Reduktion des Durchmessers unterschiedlich.
Der Baustahl wird von 4 mm auf 3,36 mm Durchmesser gezogen (Differenz: 0,64 mm), der
Edelstahl von 7,7 auf 7,16 mm (Differenz 0,54 mm) und der Draht aus Federstahl von 9,1 auf 8,4
mm (Differenz 0,7 mm). In der Darstellung zeigen sich Einflüsse mehrer Parameter
(Durchmessreduktion, Drahtmaterial und Ziehsteinstörung), daher ist ein direkter Vergleich nicht
möglich. Hierfür müssten getrennte Messungen durchgeführt werden.

Zusätzlich zu den Messungen der Betriebsschwingungen wird durch mehrere HSU-Nielsen-Tests
entlang des eingespannten Drahtes, beginnend von der Matrize, eine Abklingkurve der
Wellenpakete erstellt (vgl. Abklingkurve_Amplitude.png, Abklingkurve_Energie.png). Die
Drahtzugmaschine und alle Nebenaggregate sind während der Messung abgeschaltet und der
Draht ist vorgespannt.

Die Abbildungen stellen die gemessene Amplitude und den Energieinhalt einer Anregung in
Abhängigkeit vom Anregungsort zum Sensorort da. In Kombination mit der gemessenen
Amplitude der Störgeräusche, kann bestimmt werden bis zu welchem Abstand zum Sensor ein
Ereignis von den Störgeräuschen unterscheidbar ist. Als Sensor wird ein VS150M an der Pos. 3verwendet.
Meilenstein 1: Die Sensorpositionen wurden definiert und die handelsübliche Hardware
implementiert und getestet. Die elektronischen Schnittstellen werden im Laufe des AP 5
finalisiert.

### Auswerten der Messdaten mit den entwickelten Algorithmen

Zur Extraktion der relevanten Merkmale innerhalb der gesammelten Messdaten werden
verschiedene Metriken im Zeit- und Frequenzbereich angewendet. Im ersten Schritt werden die
Messungen der künstlichen Kerbschläge im Baustahl (S235JR) analysiert. Im Zeitbereich kann
durch den Crest-Faktor (Peakamplitude/RMS), Impulsfaktor (Peak/Mittelwert) und Margin(Peak/
Quaddratwurzel der Absolutwerte) die Impulshaftigkeit für die Messblöcke untersucht werden.
Jeder Messblock hat vergleichbar zur RMS-Auswertung eine Dauer von 26 ms. Bei einer
Ziehgeschwindigkeit von 30 m/min und einem Kerbabstand von 2 cm haben die Impulse einen
Abstand von 40 ms. Dadurch liegt in jedem Block nur ein Impuls vor. Die Auswertung zeigt, dass
zwischen den Blocknummern 2000 und 2500 die höchste Impulshaftigkeit vorliegt. In diesem
Bereich liegen auch die eingeschlagenen Kerben. Dennoch werden auch außerhalb dieses
Bereichs Impulse festgestellt, welche eine hohe Impulshaftigkeit aufweisen. Das liegt am
sporadischen Anschlagen des Drahts auf dem Boden und den Einzugsrollen.

Features im Frequenzbereich sollen die Erkennung der Kerben verbessern. Das gelingt mit einer
Berechnung des HFC (High Frequency Content), welcher hauptsächlich zur Onset-Erkennung in
Musikstücken eingesetzt wird. Hier werden die Kerben mit einer höheren Amplitude gegenüber
anderen Impulsen sichtbar. Beim Anfahren der Maschine liegt ebenfalls ein Impuls mit sehr
hochfrequentem Anteil vor, welcher falsch erkannt werden würde. Daher müssen mehrere
Features berücksichtigt werden. Im Anschluss werden diese Features mit Varianzanalysen und
weiteren statischen Methoden auf ihre Unabhängigkeit untersucht. Die besten Features werden
für die Entwicklung der ML-Modelle herangezogen.

## Literaturverzeichnis
