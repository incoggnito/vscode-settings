## Einleitung

Ein Hindernis für den Technologie- und Erkenntnistransfer der PM-Forschung aus Produktionskontexten ist zum einen in der unzureichenden Adaption bisheriger Verfahren der Künstlichen Intelligenz (KI) an die vorhandene Datenbasis zu finden. Zum anderen haben sich, aufgrund der Neuartigkeit des Betrachtungsfeldes und des damit verbundenen niedrigen Technologiestandes, industrielle Normen und Standardisierungen noch nicht ausreichend etablieren können, um bestehende KI-Verfahren mit geringem Aufwand und Risiko anwendbar zu machen.

Aus dieser Forschungslücke leitet sich das Gesamtziel des Vorhabens ab: Eine Reduzierung von Kosten und Zeit zur Erstellung einer PM-Lösung für Fahrzeugkomponenten unter Einhaltung der Qualitätsstandards.[@aliAcousticEmissionSignal2014]

Die Amitronics GmbH (AMI) möchte die Projektergebnisse nutzen, um ihr Dienstleistungsportfolio an strukturdynamischen und akustischen Messdienstleistungen entscheidend in Richtung KI zu erweitern. Dies soll in mehreren Schritten erfolgen. In einem ersten Schritt sollen insbesondere die bei AMI vorhandenen kommerziellen Mess- und Analysetechniken und -systeme, darunter das mit einem Partner entwickelte Vibroakustische Condition Monitoring System (VAM) für körperschallbasierte Ereignisse an Maschinenstrukturen, in einem breiteren Rahmen für die Themen rund um PM im Automobil nutzbar gemacht werden. Angedacht ist hier, die im Vorhaben entwickelten Cloudlösungen (AP4) für die Aus- und Bewertung der mit unserer Messtechnik erzielten Ergebnisse zu nutzen. Dadurch soll einerseits die Effizienz unserer Messdienstleistungen erhöht und andererseits die Aussagekraft der Ergebnisse dahingehend erweitert werden, dass mit Hilfe von Machine Learning Ansätzen neue, bisher nicht betrachtete Parameter und Abhängigkeiten, wie z.B. spezielle Transferfunktionen und Abhängigkeiten zwischen einzelnen Baugruppen und Komponenten, aber auch zwischen einzelnen Ergebnissen, bei der Ergebnisbewertung und bei der Ableitung von akustischen und strukturdynamischen Lösungsvorschlägen einfließen können.

Gerade hier sieht die AMI ein großes Potenzial für eine qualitativ verbesserte Ergebnisinterpretation bis hin zur Einbindung der Ergebnisse in die von den Partnern entwickelten Verschleißmodelle. Gerade die Nutzung unserer Daten in Verschleißmodellen würde das Dienstleistungsangebot der AMI weiter ausbauen. Zudem sieht die AMI ein hohes Verwertungspotenzial für ähnliche Aufgaben bei anderen Automobilherstellern, wie z.B. der BMW AG. Aufgrund der fahrzeugtechnischen Breite des Vorhabens (Fahrwerk, Getriebe, Elektronikkomponenten) ist mit gesteigerten Angeboten, welches von der Analyse des Planverschleißes bis hin zur Früherkennung von Riss- und Bruchereignissen reicht.

Kurz- bzw. mittelfristig werden hier Dienstleistungsgewerke von ca. 250T€ / Jahr erwartet, langfristig, insbesondere unter Einbeziehung von Fragestellungen aus der Elektromobilität, von 500 - 750 T€ / Jahr. Der Anwendungsbereich der neuen Dienstleistungen geht letztlich weit über den Automobilbau hinaus, wie es die Messdienstleistungen der AMI bereits tun. Zu nennen sind hier der Anlagen- und Maschinenbau sowie die Elektronik bis hin zum Bauwesen und zur Luftfahrt. Dabei liegen die Umsatzerwartungen in ähnlicher Höhe wie im Automobilbau. Darüber hinaus möchte die AMI ihr VAM fahrzeugtauglicher gestalten. Dies betrifft sowohl die Hardware in Bezug auf die Geometrie, einschließlich der Montage im Fahrzeug, als auch den Preis. Ebenfalls angepasst werden muss die Software (Abtastrate, Frequenzbereich, Cloudfähigkeit), um ein kleines, funktionales und fahrzeugtaugliches System nutzen zu können. Bei entsprechender Umsetzung (relevante fahrzeugtypische Parameter und kostenreduziert) ist auch ein permanenter Verbau des Systems im Fahrzeug zum Datenmanagement (Erfassung, Aus-, Bewertung und Bereitstellung) denkbar.

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

Die Auswahl der UseCases erfolgt auf Basis einer Risikobewertungsmatrix des Projektpartners Fraunhofer IPA in Zusammenarbeit mit Porsche und spezifiziert inhaltlich unterschiedliche Anwendungsszenarien. Die AMI bewertet die messtechnische Validierung der UseCases, insbesondere im Fachgebiet der Technischen Akustik. Abbildung \ref{ap12} fasst die möglichen Anwendungen und Anforderungen in einer Mind-Map zusammen. Nach mehreren Abstimmungen mit den entsprechenden Fachabteilungen der Porsche AG über mögliche Anwendungsszenarien haben sich vielversprechende Ausgangspunkte in den Bereichen Bremsgeräusch und Elektromotor gezeigt. Andere Themengebiete, wie beispielsweise Katalysator-, Belag- und Fahrwerksverschleiß, werden aus Gründen der Komplexität, der Validierbarkeit oder des Aufwands verworfen und sind rot markiert. Die Prioritäten werden durch eine Nummerierung markiert. Bei Porsche liegen bereits Messdaten von speziellen Sensoren an Rädern (sog. Road-Condition-Sensoren) über die gesamte Fahrzeugflotte vor. Ob diese Daten für die beiden Anwendungsfälle nutzbar gemacht werden können, soll im Folgenden geklärt werden. Der Sensor überträgt nur eine sehr begrenzte Datenmenge über das Bussystem. Daher ist die Auflösung innerhalb der Fahrzeugflotte nur relativ gering und für tiefer gehende Analysen werden höher auflösende Sensoren benötigt. Die Zeitrohdaten des Road-Condition-Sensors werden in Frequenzbändern im Bereich von 750 - 7250 Hz abgelegt. Je nach Charakteristik des Störgeräusches kann dieser Bereich und die derzeitige Auswerteroutine ausreichend sein, oder es ist eine Weiterentwicklung des Sensors in der Zukunft erforderlich.

![Mind Map zu Inhalten aus AP1\label{ap12}](images/AP1-2.png){ width=\textwidth height=80mm}

In den folgenden Teilabschnitten werden die Use Cases aus Sicht der technischen Akustik näher analysiert und der Stand der Technik zusammengefasst.

##### 1. Use Case Bremsgeräusch "Muhen"

Unter Muhen versteht man ein niederfrequentes Störgeräusch, welches beim Bremsen im niedrigen bis mittleren Geschwindigkeitsbereich auftritt. Es handelt sich hierbei um eine selbsterregte Schwingung, die durch eine dynamische Instabilität aufgrund der Kopplung von zwei oder mehr Moden der Achsen- und Bremskomponenten verursacht wird. Es handelt sich dabei um ein tonales Geräusch mit mehreren Oberschwingungen.

Je nach Masse und Steifigkeit der Achskomponenten (und damit ihrer Resonanzlage) tritt das tonale Geräusch im Bereich zwischen 200 Hz bis 500 Hz auf; mehrere Oberschwingungen sind in der Regel deutlich erkennbar. [@hirtzReduktionBremskraftschwingungenMithilfe2021]

Im Regelfall bildet sich hierbei eine Betriebsschwingform aus, welche sich aus zwei orthogonalen Moden zusammensetzt und sich nach der Kopplung über den Reibwert zu einer komplexen Schwingung ausprägt [@breuerBremsenhandbuchGrundlagenKomponenten2017]. Meist bildet sich eine Translations- und Rotationsmode des Bremssattels um die Anbindungsstelle zum Schwenklager aus. [@breuerBremsenhandbuchGrundlagenKomponenten2017]

Neben den Bauteileigenschaften gilt weiterhin die Temperatur der Bremskomponenten (hauptsächlich Bremsscheibe und Reibbelag) als maßgebliche Einflussgröße. Dabei ist zu beachten, dass eine Veränderung der Reibcharakteristik meist nur zu einer Verschiebung der Auftrittswahrscheinlichkeit und nicht zu einer Vermeidung des Geräusches führt.

Anders als früher angenommen, handelt es sich beim Erregungsmechanismus nicht um einen Stick-Slip Effekt. Dies wird damit begründet, dass die Tangentialgeschwindigkeit von Bremsscheibe und Bremsbelägen zu keiner Zeit identisch ist. [@bauerTechnicalProgrammeEuroBrake2017]

Die auftretenden Störgeräusche können durch Mikrofone im Fahrzeuginnenraum oder einzelne Körperschallaufnehmer im Achsbereich erfasst werden. Eine Identifikation und weitergehende Analyse ist nur möglich, wenn neben den Fahrzeugzustandsdaten (Bremsdruck, Temperatur der Bremsscheibe, Fahrzeuggeschwindigkeit und Lenkeinschlag) auch eine detaillierte Betriebsschwingform der Achse vorliegt. Die Erfassung dieser Betriebsschwingform erfordert einen hohen planerischen und messtechnischen Aufwand, die Zugänglichkeit zu allen Achs- und Bremsenkomponenten muss gewährleistet sein, das Geräusch muss zuverlässig und reproduzierbar auftreten zudem müssen die Umweltbedingungen den Einsatz von Körperschallsensoren erlauben. Nach Erfassung der Betriebsschwingform und der Identifikation des Phänomens ist eine Reduzierung der Messtechnik auf einen bzw. wenige Sensoren möglich, solange das System nicht konstruktiv verändert wird. [@bauerTechnicalProgrammeEuroBrake2017]

Die Amplitude der Oberwellen nimmt im Mittel um ca. 50 % pro Ordnung ab; je nach Pegel der Grundschwingung ist das Muhen somit auch bei höheren Ordnungen ( > 1 kHz) eindeutig zu identifizieren. Diese Theorie soll im Weiteren anhand vorhandener Messdaten geprüft werden.

Nach Auswertung einer speziellen Testfahrt (Muh-Punktsuche) im Fachbereich Bremse zeigt sich, dass die Oberwellen im vorliegenden Fall deutlich in dem Bereich liegen, der vom Road-Condition-Sensor erfasst werden kann. In Abbildung \ref{spec} wird ein Spektrogramm dargestellt, welches im Zeitbereich einen Fahrtausschnitt von 56 s zeigt. Von Sekunde 18 bis 25 ist ein ausgeprägtes Muhgeräusch zu erkennen. Im Frequenzbereich können Oberwellen des Grundgeräusches (< 500 Hz ) bis zu Frequenzen von 6 kHz mit ausreichendem Signal-Rauschabstand erfasst werden. Daher können nun in Abstimmung mit dem Fachbereich weitere Schritte geplant werden.

![Spektrogramm zur Muhpunktsuche\label{spec}](images/Muhpunktsuche.png){ width=\textwidth height=80mm }

Bei der Auswertung gibt es noch einige Herausforderungen. Die Datenformate der vorliegenden Messdaten weichen von den geltenden Standards ab und sind nicht synchronisiert. Die Zeitstempel der Flags und Kommentare vom Fahrer sind ungenau und nur teilweise automatisiert filterbar. Solche Probleme sind aufgrund unterschiedlicher Formate und interner Standards in der Automobilindustrie nicht ungewöhnlich und können in der folgenden Entwicklung des Referenzmodells adressiert werden. Für die gemeinsame Analyse der Störgeräusche wird eine separate Softwarebibliothek zur Verfügung gestellt. Diese dient im fortschreitenden Projekt als gemeinsame Entwicklungsumgebung. Im weiteren Verlauf sollen die Messdaten in einer Datenbank zur Verfügung gestellt werden.

Neben Fahrzeugflottendaten könnten auch Komponenteninformationen in die Analyse mit aufgenommen werden. Bei niederfrequenten Bremsgeräuschen nutzt man beispielsweise eine große Anzahl von generisch synthetisierten Bremskomponenten-Beschleunigungsspektren und wertet diese mit Techniken der Künstlichen Intelligenz (KI) bzw. der Künstlichen Neuronalen Netze (ANNs) aus.  [@purscherNVHSIGNALANALYSIS2018]

#### 2. Elektroantrieb Lagerschädigungen

Im Anwendungsfall des Elektroantriebs wird die Zustandsüberwachung der Wälzlager behandelt. Bei der Entwicklung von Aggregatelagern besteht häufig ein Zielkonflikt zwischen der Lebensdauer der Lager und den NVH-Eigenschaften des gelagerten Systems [@linkeAggregatelagerMitHoheger2010]. Die beiden Störgeräusche der beiden Use Cases sind von ihrer Wirkung gegensätzlich, weisen aber dennoch einige Gemeinsamkeiten in der Geräuschbearbeitung auf. Zur Diagnose des Zustands beider Komponenten wird ein Beschleunigungssensor möglichst nahe an dem jeweiligen Überwachungsobjekt montiert. Die grundlegende Signalanalyse ist für beide Anwendungsfälle gleich. Grundsätzlich stützt sich die Analyse auf den Zeit- und Frequenzbereich. In den jeweiligen Bereichen unterscheiden sich die relevanten Features.

Wenn die fehlerfreie Funktion von Wälzlagern prozesskritisch ist, muss ihr Zustand konstant überwacht werden. Die Zustandsüberwachung von Wälzlagern wird im Rahmen der "Zustandsbasierten Instandhaltung" eingesetzt. Bei diesem Ansatz der Instandhaltung wird ein nötiger Austausch eines Lagers anhand des gemessenen Zustands bestimmt [@mokhtarimolkabadiUberwachungHydrodynamischerGleitlager2020]. Dies ist ein fortgeschrittener Ansatz im Vergleich zu einem Austausch bei Versagen oder in experimentell bestimmten Zeitintervallen. In heutigen Fahrzeugflotten kann zur Zustandsüberwachung auf bereits verbaute Sensoren zurückgegriffen werden oder bei Bedarf können weitere Sensoren an das Bussystem angeschlossen werden.

Lagerschäden haben diverse Ursachen. Neben Fehlern bei der Montage können auch Fehler im Betrieb auftreten. Zu den Betriebsfehlern gehören unter anderem eine Überbelastung oder eine unzureichende Schmierung. Im Zusammenhang mit Elektroantrieben gewinnt die elektrische Belastung von Lagern immer mehr an Relevanz. Trotz fehlerfreier Montage und optimalen Betriebsbedingungen fallen Wälzlager am Ende ihrer Lebensdauer aufgrund von Materialermüdung aus. [@bruelkjaervibroa/sAnwendungsbeispielErmittlungFehlerhafter]

Bei Porsche liegen bereits einige beschädigte Lager aus vergangenen Versuchsreihen vor um den Ausgangszustand zu ermitteln, wird eine Zustandsanalyse im Fachbereich beauftragt. Sobald absehbar ist, wann die Lager verfügbar sind, wird ein Testfahrzeug für die Messreihe gebucht. Anschließend werden die Zeitslots für die Werkstattumbauten und die Benutzung des Rollenprüfstands geplant. Ziel dieser Messung ist im ersten Schritt der Abgleich zwischen dem Road-Condition-Sensor und den hochauflösenden Sensoren von der AMI. Es werden spezielle Acoustic-Emission Sensoren eingesetzt, um die Relevanz von Oberflächenschwingungen im Ultraschallbereich zu prüfen. Die resultierende Datenmenge wird in Arbeitspaket 3 näher untersucht.

Um den Ausfall eines Lagers rechtzeitig zu erkennen, müssen die Randbedingungen möglichst umfassend überwacht werden. Relevante Größen für die Zustandsbeurteilung sind die Temperatur des Lagers, die Fremdkörper in der Schmierung und die durch das Lager verursachten Beschleunigungen. Die Informationen werden teilweise durch andere Fahrzeugsensoren ermittelt. Die Synchronität der unterschiedlichen Quellen muss dabei sichergestellt werden.

Für die Signalanalyse der von den Lagern verursachten Beschleunigungen ist es zunächst erforderlich, zwischen den existierenden Lagertypen zu unterscheiden. Die gebräuchlichsten Lager sind Wälzlager, Gleitlager und Magnetlager. Aufgrund ihrer unterschiedlichen Wirkprinzipien unterscheiden sich die während ihres Betriebs gemessenen Beschleunigungssignale. Lokale Schäden an Wälzlagern haben zum Beispiel charakteristische Schadensfrequenzen, weil sich die Wälzkörper in den Lagerschalen in Abhängigkeit von der Drehzahl des Rotors bewegen. Diese Schadensfrequenzen sind abhängig davon, ob das Wälzlager in der üblichen Konfiguration eingesetzt wird oder nicht: rotierender Innenring mit feststehendem Außenring. Wenn die Drehzahl des Lagers bekannt ist , kann daraus abgeleitet werden, welche Teile des Lagers beschädigt sind. Die charakteristischen Schadensfrequenzen können dem Außenring, dem Innenring, den Wälzkörpern oder dem Käfig zugeordnet werden. Beispielhaft sind im folgenden die allgemeinen Formeln für die charakteristischen Schadensfrequenzen eines Außenringschadens ($f_AP$) und eines Innenringschadens ($f_IP$) aufgeführt:

$$ f_{AP} = \frac{1}{2} z \Delta f \Big( 1 - \frac{D_{WK}}{D_{T}} \cos \alpha \Big) $$
$$ f_{IP} = \frac{1}{2} z \Delta f \Big( 1 + \frac{D_{WK}}{D_{T}} \cos \alpha \Big) $$
$$ \Delta f = f_{I} - f_{A} $$
Wobei folgende Variablen auftreten:

- z: Anzahl der Wälzkörper
- $\Delta f$  als die relative Drehfrequenz zwischen Innen- und Außenring
- $D_{WK}$ Wälzkörperdurchmesser
- $D_T$ Teilkreisdurchmesser
- $\alpha$ der Betriebsdruckwinkel

Die Beschleunigungssignale werden sowohl im Zeitbereich, im Frequenzbereich und im Zeit-Frequenzbereich analysiert. In den Bereichen werden unter anderem energetische und stochastische Merkmale betrachtet. Neben dem originalen Zeitsignal werden Informationen aus der Hüllkurve des Signals berücksichtigt. [@doguerSimulationWalzlagerschadenUnter2013].

Im Frequenzbereich kann ein Cepstrum verwendet werden, um periodische Strukturen in Frequenzspektren zu analysieren. [@nortonFundamentalsNoiseVibration2003] Solche Strukturen entstehen durch reflektierende Wellenpakete oder durch das Auftreten von harmonischen Frequenzen, wie z.B. Obertönen.

Um den Zustand des Lagers beurteilen zu können, werden die aktuellen Werte der Merkmale mit denen eines Referenzzustandes verglichen. Mit Hilfe von experimentellen Untersuchungen können Schwellwerte bestimmt werden, ab denen ein Wälzlager ausgetauscht werden sollte. Die berechneten Merkmale aus den verschiedenen Bereichen werden im weiteren Verlauf mit den Betriebsparametern kombiniert und als Eingangsgrößen für Machine Learning Verfahren verwendet.

### AP-2 Entwicklung des PANAMERA-Referenzmodells

#### Zielsetzung

Entwicklung des PANAMERA-Referenzmodells, bestehend aus einem Prozessmodell und einem PM–Baukasten und zur Evaluierung dienen einige ausgewählte Fahrzeugkomponenten.

#### Ergebnisse

Für ein allgemeingültiges Vorgehen im Prozess des Data-Minings gibt es verschiedene Referenzmodelle. Zwei weit verbreitete Standards sind SEMMA und CRISP-DM.

Data-Mining zählt als ein Schritt in der Wissensentdeckung in Datenbanken (engl. Knowledge Discovery in Databases (KDD)). Der Prozess des KDD wird in fünf Schritte unterteilt @azevedoKDDSEMMACRISPDM:

1. Selektion: Auswahl geeigneter Datensätze oder Auswahl einer Untergruppe an Merkmalen und Daten
2. Datenvorbereitung (Preprocessing): Beispielsweise Entfernen von ungültigen Einträgen und anderen Methoden, um konsistente Daten zu erhalten
3. Transformation der Daten: Reduzierung der Dimensionen oder anderer Transformationsmethoden
4. Data Mining: Suche nach relevanten Mustern
5. Interpretation und Evaluierung der entdeckten Muster

Der Prozess des KDD wird iterativ durchgeführt.

SEMMA wurde von dem SAS Institute entwickelt. Die Abkürzung SEMMA setzt sich aus den fünf Schritten des Modells zusammen [@azevedoKDDSEMMACRISPDM]:

1. Sample: Reduzierung der Daten auf eine geeignete Untermenge, um damit schneller arbeiten zu können. Dieser Schritt ist optional.
2. Explore: Untersuchen der Daten auf unbekannte Trends und Anomalien
3. Modify: Erstellen, Auswählen und Transformierung von Variablen
4. Model: Training der gewählten Machine Learning Modelle
5. Asses: Bewertung der Modelle hinsichtlich ihrer Ergebnisse und ihrer Performanz

CRISP-DM entstand durch ein Konsortium aus Daimler Crysler, SPSS und NCR. Cross-Industry Standard Process for Data Mining ist der Namensgeber dieser Vorgehensweise. Folgende Schritte werden absolviert [@azevedoKDDSEMMACRISPDM]:

1. Business understanding: Die Ziele und Anforderungen des Projektes werden in eine Data Mining Aufgabe überführt. Es wird eine Vorgehensweise zur Erfüllung dieser Punkte geschaffen.
2. Data understanding: Erste Daten werden gesammelt und ausgewertet. Dadurch soll ein erstes Verständnis für die Daten resultieren. Eventuelle Probleme der Datenqualität können erkannt werden. Ziel dieses Schrittes ist es, aussagekräftige Teilmengen der Daten zu erhalten und erste Hypothesen zu entwickeln.
3. Data preparation: Verarbeitung der Rohdaten zu verwendbaren Daten.
4. Modeling: Auswahl der Machine Learning Modelle sowie Training und Optimierung dieser.
5. Evaluation: Das resultierende Modell bzw. die Modelle werden kritisch bewertet. Alle vorherigen Schritte werden überprüft. Die Erfüllung des Anwendungsfalls ist ein wichtiger Teil dieser Evaluierung.
6. Deployment: Präsentation und Anwendung des finalen Models.

Die vorgestellten Vorgehensweisen des KDD haben Schnittmengen und kleinere Unterschiede. Die obigen Schritte und ersten Auswertungen der beiden Anwendungsfälle: Bremsgeräusch "Muhen" und Elektroantrieb "Lagerschaden" zeigen die Aufgaben der AMI im Forschungsprojekt für die jeweiligen Schritte 1 bis 3.

Eine Literaturrecherche zu den aktuell angewandten Machine-Learning Verfahren, die zur Erkennung von Lagerschäden, Muhen und anderen Ereignissen eingesetzt werden, ergibt nur geringfügige Unterschiede, da die zugrundeliegende Datenrepräsentation dieselbe ist.

Prinzipiell werden die erhobenen Sensordaten als Zeitreihendaten interpretiert. Hierbei können die Daten als univariate time series data (nur das Messsignal = Rohdaten) oder als multivariate time series data (inkl. berechneter Features) verwendet werden. Für die Berechnung zusätzlicher Features können gängige Verfahren, wie die Zerlegung des Signals in seine Frequenzanteile mittels Fast Fourier Transformation (FFT) / Discrete Wavelet Transformation (DWT) / Continuous Wavelet Transformation (CWT) zum Einsatz kommen.

Die Erkennung und Vorhersage von Ereignissen im Bereich der Schallemission sind ebenfalls in zwei aufeinanderfolgende Schritte unterteilt, welche sich auch auf die Architektur der verwendeten ANNs auswirken.

Im ersten Schritt werden die Zeitreihendaten oftmals mit Deep Convolutional Neural Networks (DCNN), welche die mathematische Faltungsoperation anwenden, verarbeitet und dadurch verschiedene feature maps erzeugt. Dieser Schritt wird je nach Anzahl der im neuronalen Netz enthaltenen (eindimensionalen) Convolutional Layers wiederholt. Im Anschluss werden die dadurch erzeugten feature maps durch ein Multi-Layer Perceptron (MLP) zur Klassifizierung gegeben.

1D Convolutional Neural Networks bieten im Wesentlichen folgende Vorteile [@erenGenericIntelligentBearing2019]:

* kompakte Architekturkonfiguration (für die Fehlererkennung und -überwachung in Echtzeit geeignet)
* kostengünstige Hardware-Implementierung
* Fähigkeit, ohne vorher festgelegte Transformationen (wie FFT oder DWT) Features zu extrahieren
* effizientes Training des Klassifizierers (MLP)

Zudem ist die Convolution Operation translationsinvariant.

Unterschiede bei den eingesetzten Verfahren existieren lediglich im Aufbau und Größe der neuronalen Netze, bei den Werten der Hyperparameter und bei der Abtastung der Zeitrohdaten.

Im Hinblick auf das Prozessmodell können mehrere Datenpipelines unterschieden werden:

* Gestreamte Daten aus dem Testfahrzeug
* Historische Datenbanken der Fahrzeugflotte
* Nachauswertungen von Daten aus dem Entwicklungsumfeld

Die Umsetzung der Daten-Pipelines ist aktuell in Klärung. Außerdem gilt es die Messdaten um entsprechende Metainformation (Umrechnungsfaktoren, Datentyp, Einheit des Signals, ...) zum Messkanal zu erweitern.

### AP-3 Datenerfassung und Datenvorverarbeitung (der ausgewählten Komponenten) und Entwicklung zusätzlicher benötigter dezentraler Datenvorverarbeitung

#### Zielsetzung

Die „klassischen“ Fahrzeugdaten sowie die im Rahmen des Projektes zusätzlich erhoben Fahrzeugdaten sollen möglichst vollumfänglich, zueinander synchronisiert und verlustfrei komprimiert gespeichert sowie den nachfolgenden Ketten sowohl „live“ als auch offline zur Verfügung gestellt werden.

Daher ist es das Ziel, das BDEMS von EXX um entsprechende APIs zu erweitern, um einerseits als Ausführungsplattform für fremde Softwareanteile zu dienen oder andererseits, integriert auf fremden Plattformen ausgeführt werden zu können. Ebenso sollen weitere APIs integriert werden, um die einfache Überführung von anfallenden Schritten zu unterstützen, die in der Projektumgebung stattfinden, wie z.B. Featureauswahl /-extraktion. 

#### Ergebnisse

In einer ersten Abstimmung werden Ideen zu den Schlagwörtern des Arbeitspakets aufgearbeitet. Diese werden in Abbildung \ref{ap3} in eine Mind Map zusammengefasst. Aktuell werden vor allem die Schnittstellenthemen gemeinsam mit EXX bearbeitet. Dazu werden im ersten Schritt die vorhandenen Kommunikationsendpunkte vorgestellt.

![Mind Map zu Inhalten aus AP3\label{ap3}](images/AP3.png){ width=\textwidth height=80mm }

Das vibroakustische Messsystem (VAM) von AMI ist ein IoT-Gerät, welches über verschiedene Protokolle Informationen von zwei AE-Sensoren zur Verfügung stellen kann. Außerdem kann auf dem Messsystem eine Pipeline zur Datenvorverarbeitung umgesetzt werden. Als Übertragungsprotokoll wird voraussichtlich das MQTT-Protokoll eingesetzt. Der Vorteil dieses Protokolls ist die einfache Struktur der Kontrollnachrichten, die Möglichkeit, es auf Systemen mit geringen Ressourcen zu verwenden und die Möglichkeit der einfachen Integration in das Informationssystem des Kunden durch Softwarebibliotheken. [@shaoutUsingMQTTProtocol2018]

Für die Schnittstelle unseres Messsystems zum BDEMS-Systems gilt, die voraussichtlich zu übertragende Datenmenge zu klären. In folgender Tabelle \ref{tab:throughput} sind exemplarisch einige Datendurchsatzraten bei unterschiedlichen Blockgrößen und Abtastfrequenzen des Messsystems dargestellt.

| Abtastfrequenz [Hz] | Blockgröße [-] | Zeitrohdaten [B] | Features [B] | Gesamt [B] | Interval der Blöcke [s] | Throughput [bit/s] |
| ------------------- | -------------- | ---------------- | ------------ | ---------- | ----------------------- | ------------------ |
| 20 000              | 2048           | 8192             | 1600         | 9792       | 0,1024                  | 765 000            |
| 20 000              | 65536          | 262144           | 1600         | 263744     | 3,2768                  | 643 904            |
| 1 000 000           | 2048           | 8192             | 1600         | 9792       | 0,002048                | 38 250 000         |
| 1 000 000           | 65536          | 262144           | 1600         | 263744     | 0,065536                | 32 195 312         |

Table: Durchsatz für unterschiedliche Abtastraten und Blocklängen \label{tab:throughput}

Im Normalfall kann von etwa 1 Mbit/s ausgegangen werden, wobei im Projekt ein maximaler Datendurchsatz von 38 Mbit/s zu erwarten ist.

Neben dem eigenen IOT-Gerät werden weitere akustische Messsysteme (MBBM PAK, LMS) im Testfahrzeug eingesetzt. Diese erlauben eine deutlich höhere Anzahl von Messkanälen bei geringerer Auflösung. Als einheitliches Datenformat ist hier ASAM ATFx File Format (ATFx) standardisiert. Von der Struktur ist die ATFx-Datei eine reguläre XML-Datei, die normalerweise Informationen zur Beschreibung einer Messung enthält. Der Hauptunterschied zu einer normalen XML-Datei besteht darin, dass die ATFx-Datei ein Header-Element mit einem ASAM ODS-Datenmodell enthält. [@ASAMATFxDateiformat]

Ein weitverbreitetes Datenformat (ebenfalls von ASAM) ist MDF (Measurement Data Format). Dieses ist ein binäres Dateiformat zur Speicherung aufgezeichneter oder berechneter Daten für die Nachbearbeitung von Messungen, die Offline-Auswertung oder die Langzeitspeicherung. [@ASAMMDFMessdatenformat]

Die meisten bekannten akustischen Messsysteme können heutzutage ATFX verarbeiten. Es können sogar Messeinstellungen zwischen unterschiedlichen Messsystem ausgetauscht werden. Die Software zur Auswertung und Signalverarbeitung innerhalb der Messsysteme bietet hier, neben den im Projekt eingesetzten Python-Bibliotheken hochspezialisierte Auswerteroutinen. Da das MDF-Format dort oftmals nicht lesbar ist, wäre eine Konvertierung von MDF zu ATFX wünschenswert. Bisher ist das so nicht möglich. Aktuell wird recherchiert, ob die Verwendung eines zentralen ODS-Servers zur Verwaltung und Anbindung der beiden Datentypen möglich ist und ob beim OEM die entsprechende Infrastruktur vorhanden ist.

In modernen Fahrzeugen werden eine Vielzahl von elektronischen Steuerungsgeräten und Sensoren verbaut, welche den operationellen Betrieb sowie die Zustandsüberwachung einzelner mechanischer Komponenten gewährleisten. Aus der steigenden Anzahl der integrierten Sensorelemente resultiert ein Zuwachs der anfallenden und aufzuzeichnenden Datenmenge, was einerseits die Problematik der persistenten Speicherung und Übertragung der Daten in Echtzeit verschärft, aber auch den Einsatz von datengestützten Analyseverfahren aus dem Bereich des Machine Learning (ML) ermöglicht.

Sowohl aus Gründen der Wirtschaftlichkeit als auch aufgrund der limitierten Hardwareressourcen pro Fahrzeug werden die mittels ML berechneten Modelle nicht einzeln / lokal für jedes Fahrzeug erstellt. Stattdessen werden die erhobenen Sensordaten über vordefinierte Schnittstellen in eine zentrale Infrastruktur (Cloud) überführt und dort aggregiert.

Für die Definition dieser Schnittstellen sind folgende Kriterien ausschlaggebend:

* Übertragungsrate: Quell- u. Zielsystem müssen über die gleichen Kapazitäten hinsichtlich der Datenübtragungsrate verfügen. Dies gilt für das Lesen und Versenden und, analog dazu, für das Empfangen und Schreiben der Daten.
* Protokolle: Protokolle spezifizieren, wie Daten ausgetauscht werden und müssen folglich auf Quell- u. Zielsystem verwendet werden.
* Einheitliche Datenformate inkl. aller Metadaten

Diese Verwendung einer zentralen Infrastruktur bietet gegenüber einem dezentralen Ansatz mehrere Vorteile. Einerseits können so Daten aus heterogenen Quellen akquiriert und aggregiert werden. Andererseits stehen für die Modellberechnungen mittels ML Verfahren wesentlich mehr Daten zur Verfügung, was wiederum positive Auswirkungen auf die Qualität der Modelle hat. Grundsätzlich gilt: je mehr Daten vorhanden sind, desto präziser werden die Vorhersagen der Modelle. Zusätzlich lässt sich die Gesamtheit der Daten global auf Vollständigkeit und Korrektheit überprüfen.

### AP-8 Öffentlichkeitsarbeit und Verbreitung der Ergebnisse

Im Projekt wird die Veröffentlichung in Fachzeitschriften (z.B. Mess- und Sensortechnik), die Teilnahme an Fachtagungen (MicroClean Berlin) und eine interne Hausmesse am neuen Firmenstandort angestrebt. Gegebenenfalls kann eine Softwarebibliothek im Bereich ATFX veröffentlicht werden. Zudem sollen Projektergebnisse durch soziale Netzwerke, wie beispielsweise LinkedIn geteilt werden.

### AP-9 Projektmanagemnt

Zu Beginn des Projekts werden einige organisatorische Rahmenbedingungen für die Kommunikation festgelegt. Nach einer agilen Vorgehensweise wird in 2-wöchigen Sprints zusammen an den Arbeitspaketen gearbeitet. Neben den regelmäßigen Sprints findet eine eigenverantwortliche Abstimmung mit den entsprechenden Fachabteilungen und Partnerunternehmen statt. Innerhalb der Sprints werden die Ergebnisse aus den unterschiedlichen Bereichen zusammengeführt.

Die Aufgaben werden innerhalb einer globalen Verwaltung (Jira) nach der Kanban-Methodik organisiert und die Dokumentation erfolgt auf einer eigenen Plattform (Confluence). Eine gemeinsame Bibliothek für die Softwareentwicklung wird durch Gitlab realisiert. Dies ermöglicht, z.B. die Zusammenarbeit an den Signalanalysetoolboxen.

Die Freischaltungen der genannten Plattformen erfordert eine Vielzahl von Berechtigungen und verursachte im ersten Quartal einen hohen organisatorischen Aufwand. Insbesondere im Hinblick auf verschiedene Geheimhaltungsfragen und die Absicherung im Rahmen der TISAX Zertifizierung wird ein erhöhter Aufwand zu berücksichtigen sein. Alle Projektthemen müssen diesbezüglich unter dem Aspekt der Informationssicherheit bewertet werden.

## Literaturverzeichnis
