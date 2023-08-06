#!/usr/bin/env python3
# -*- coding: utf-8 -*-
    
# *******************************************
# *******************************************
# Help text
# *******************************************
# *******************************************

# *******************************************
# (i) README.txt
# *******************************************

readme_text =\
"""---------------------------------------
---------------------------------------
README.txt (currently only in German):
---------------------------------------
---------------------------------------

INSTALLATION FÜR LINUX UND UBUNTU:
----------------------------------------
----------------------------------------

Installation mit pip: pip3 install ivisit
bzw. mit allen abhängigen Paketen: pip3 install ivisit supylib pillow numpy

Oder alte Methode vom tar.gz-Archiv: 

1) IVisit.0.4.tar.gz in ein beliebiges Verzeichnis (z.B. Ihrer Python-Projekte) kopieren und mit
      tar xfz IVisit.0.4.tar.gz 
   entpacken.

2) In Ihrer .bashrc eine Zeile für den PYTHONPATH auf das Verzeichnis IVisit.0.4 einfügen (damit
   die Python-Module von IVisit überall sichtbar sind), z.B.
      export PYTHONPATH=/home/login-name/projects/IVisit.0.4:$PYTHONPATH

Alternative: Statt obiger zwei Zeilen in der .bashrc reicht auch das Einfügen der folgenden Zeile:
source /home/login-name/projects/IVisit/python/BashSrc

Bemerkung: Wenn mehrere Versionen von IVisit und/oder ReLabelEd parallel verwendet werden, dann können
           Sie durch den obigen source-Befehl (in einer Shell ausgeführt) diese Version aktivieren
	   (es wird dadurch PATH und PYTHONPATH geupdated, sodass sie Verzeichnisse der ausgewählten
	   Version ganz vorne in den Suchpfaden erscheinen und deshalb zuerst ausgeführt werden).

3) Starten/Test/Demo: Neue Bash öffnen (damit neuer PYTHONPATH wirksam wird) und in
   das Verzeichnis Ivisit/demos gehen. Dann den Befehl
      python demo1_gaussfilter.py demo1_gaussfilter.db&
   eingeben („&“ setzt einen eigenen Prozess ab, so dass man in der Shell weiterhin Befehle eingeben kann).
   Es sollte nun das Ivisit-Fenster starten in dem ein Demoprogramm aus der Bildverarbeitung ausgeführt
   wird (Gauß-Filter). Sie können die „Simulation“ starten indem Sie in der Button-Leiste links unten
   „Run“ drücken. In jedem Simulationsschritt werden die Parameter von den GUI-Elementen (hier: Bild-Index,
   Kernel-Radius, Kernel-Sigma) gelesen und dann der Simulationszustand geupdated (hier: das gefilterte
   Bild „Filter-Output“). Spielen Sie mit den Sliders! Oben rechts sehen Sie die Anzahl der
   Simulationsschritte. Wenn Sie in der Button-Leiste links unten auf „Stop“ drücken hält die Simulation an.
   Mit „Cont“ können Sie fortsetzen. Mit „Run“ neu starten. Mit „Init“ die Simulation initialisieren.
   Mit „Save“ speichern Sie die aktuellen Parametereinstellungen. Mit „Quit“ unten rechts können Sie die IVisit beenden.
   Ähnlich können Sie die zweite etwas komplexere Simulation starten:
      python demo2_DoG_filter.py demo2_DoG_filter.db&

4) Wichtigste Bedienelemente für eine gegebene IVisit-Simulation (wie z.B. die Demo-Simulationen)

4.1) Die Action-Button-Leiste links unten:
Save: Speichert die aktuellen Einstellungen der Parameter und Visulisierungs-Widgets
Init: Initialisiert die Simulation durch Aufrufen der init() Methode
Step: Es wird ein Simulationsschritt durch Aufrufen der step() Methode durchgeführt
Run: Es wird init() und danach wiederholt die step() Methode aufgerufen. Zwischen zwei Aufrufen der step() Methode wird 
     ein bestimmtes Zeitintervall pausiert. Die Länge des Zeitintervalls können Sie im Menüpunkt Databases/Simulations 
     durch das Attribut delay/step einstellen.
Stop: Die durch Run gestartete automatische Simulation wird gestoppt.
Cont: Fortsetzen der Simulation (ohne Initialisieren)
Simulations: Aufruf des Menüpunkts Databases/Simulations, z.B. zur Auswahl einer bestimmten zuvor gespeicherten
             Simulations- bzw. Parameterkonfiguration.
Parse: Die im Python-Simulationsskript definierten GUI-Elemente werden gescannt und in die Simulation eingefügt 
       (falls sie nicht schon vorhanden sind). Dies ist meist beim ersten Ausführen einer Simulation nötig, damit man
       nicht alle GUI-Elemente von Hand über Menüpunkt Databases einfügen muss. 

4.2) Die Action Button-Leiste rechts unten:
Quit: Beenden von IVisit
Help: Hilfe

4.3) Der schwarz unterlegte Info-Balken unter der Menüleiste <File-Name>::<ID>::<Simulations-Name> und <Steps>
File-Name: Der File-Name ganz links zeigt das Aktuell verwendete Daten-File (Endung *.db) an mit der die Simulation
           läuft. In diesem File werden die Parametereinstellungen zu den jeweiligen Simulations-Konfigurationen
           gespeichert.
Simulations-ID/Name: Die ID und der Name der aktuell verwendeten Simulations-Konfiguration. Sie können diese über Action-
                     Button Simulations bzw. Menüpunkt Databases/Simulations auswählen/ändern/neu erstellen.
Steps: Gibt an wieviele Simulationsschritte schon durchgeführt wurden.

4.4) Menüleiste:
File: Laden/Speichern eines Daten-Files zu einer Simulation (mit Endung *.db)
HUBS: Wichtigste Action-Dialoge:
HUBS/Simulations: Auswahl/Neuerstellung einer Simulations-Konfiguration: In jedem Daten-File können Sie beliebige
                  Simulations-Konfigurationen zu einer Simulation speichern, typischerweise um interessante Parameter-
                  Werte zu speichern, während man weiter nach noch besseren sucht...
HUBS/Edit-Parameter-Widgets: Verwaltung der Parameter-Widgets (siehe auch Databases/Parameter-Widgets). Parameter-Widgets
                  sind die GUI-Input-Elemente, die von der Simulation gelesen werden, und mit denen Sie typischerweise
                  System-Parameter der Simulation beeinflussen. Parameter-Widgets sind z.B. Sliders, List-Selections und
                  Textfelder. Jeder Parameter-Widget ist mit einem Parameter verbunden (siehe auch Databases/Parameter),
                  der wiederum mit einer Variablen aus dem Python-Simulations-Skript verbunden ist.
HUBS/Edit-Data-Widgets: Verwaltung der Daten-Widgets (siehe auch Databases/Data-Widgets). Data-Widgets sind die Output-
                  Elemente der GUI, mit denen System-Zustände von der Simulation ausgegeben bzw. visualisiert werden
                  können, damit das System-Verhalten beobachtet werden kann. Daten-Widgets sind z.B. Images oder
                  Textfelder. Jeder Daten-Widget ist mit einem Data-Array verbunden (siehe auch Databases/Data-Array),
                  das wiederum mit einer Variablen aus dem Python-Simulations-Skript verbunden ist.
Databases: Hier können Sie die einzelnen Tabellen des Data-Files (mit Endung *.db) bearbeiten.
            - Die meisten Menü-Punkte entsprechen den vorigen Menüpunkten
            - Mit dem Menüpunkt Databases/Comment-Widget kann man Kommentare einfügen mit dem man die Abläufe in der
              Simulation beschreiben und erklären kann.      
Simulation: Hier können Sie die Simulations-Funktionen steuern (entspricht den Aktion-Buttons unten links)
Help: Hilfefunktion

4.5) Simulations-Fläche in der Mitte
In der Mitte des IVisit-Fensters werden die Parameter-Widgets (zur Eingabe), die Data-Widgets (zur Ausgabe), und die
Comment-Widgets (zur Erklärung) dargestellt. Sie können frei verschoben werden, wobei die Positionen der Widgets
ebenfalls mit „Save“ gespeichert werden.

5) Erstellen eines eigenen Python-Simulations-Skripts
- Schauen Sie sich am besten den Aufbau der Demo-Simulations-Skripte an (demo1_gaussfilter.py und demo2_DoG_filter.py)
- Jedes Simulations-Skript enthält die folgenden Teile:
    - class SimParameters: Definiert die Simulations-Parameter die Sie über IVisit verändern/einstellen möchten
    - class SimData: Definiert die Simulations-Daten die Sie über IVisit ausgeben/visualisieren möchten
    - class Sim: Definiert die eigentliche Simulation über die Methoden
         - main_init(): Wird einemal beim Start bzw. Konstruktion der Simulation/Simulationsobjekte aufgerufen
         - init(): Wird vor jedem Neustart der Simulation aufgerufen
         - step(): Wird in jedem Simulations-Schritt aufgerufen
      Siehe auch die Basis-Klasse IVisit_Simulation im Modul ivisit.simulation.py
    - Hauptprogramm („main program“): Dort wird ein Simulations-Objekt vom Typ Sim erzeugt und durch 
      Ivisit_main(sim=sim) die Ivisit-GUI gestartet
- Definition der GUI-Elemente: 
    - Alle GUI-Elemente können im Prinzip in der IVisit-GUI von Hand erzeugt werden (z.B. unter HUBS oder Databases)
    - Es ist aber meist viel bequemer die (wichtigsten) GUI-Elemente schon im Python-Simulations-Skript zu definieren
    - z.B. Siehe in  demo1_gaussfilter.py, Zeilen 10-17 und die folgende nähere Erklärung...
- Mit der folgenden Syntax kann man im Python-Simulations-Skript Ivisit-GUI-Elemente erzeugen:
    - #@IVISIT:SIMULATION & sim_gauss_filter1  
      erzeugt einen Eintrag in der Database Simulations mit Namen sim_gauss_filter1 
    - #@IVISIT:SLIDER     & Bild-Index    & [200,1] & [0,20,5,1] & idx_image & -1 & int & 0 
         - erzeugt einen Slider mit Namen Bild_index mit Breite 200 Pixel (der zweite Wert 1 ist im Prinzip die Höhe, 
           wird aber für Slider ignoriert). 
         - [0,20,5,1] bedeutet, dass der Wertebereich des Sliders von 0 bis 20 ist, dass er 5 Ticks hat, und die
           Skalierung 1 ist (=Abstand zwischen zwei möglichen Werten)
         - idx_image: Mit dem Slider kann man die Python-Variable idx_image verändern
         - -1: Parameter List index (Index, falls idx_image eine Liste ist; -1 bedeutet, dass es keine Liste ist)
         - int: Data Type der Python-Variable
         - 0: Initialwert des Parameters
    - #@IVISIT:TEXT_IN & txt-dummy     & [20,5] & dummytextpar & -1 & "InitialText"
         - erzeugt ein Text-Eingabefeld mit Namen „txt-dummy“ der Größe 20x5 mit dem man den Wert der Python-String-
           Variablen dummytextpar belegen kann. 
         - -1 kann man wieder ignorieren (Listen-Index, falls es sich bei der Python-Variable um Liste handelt)
         - „InitialText“ ist wieder Initialwert
    - #@IVISIT:LISTSEL & lst-dummylist & [20,5] & [A,BBBBB,CCC,DDDDD] & dummytextpar & -1 & string & A
         - erzeugt eine List-Selektion mit Namen „lst-dummylist“ der Größe 20x5
         - man kann zwischen den Einträgen "A","BBBBB","CCC","DDDDD" auswählen
         - Der ausgewählte String wird in der Python-Variablen dummytextpar gespeicherte
         - -1 ist wieder Listen-Index (-1 bedeutet keine Liste)
         - string und „A“ sind Datentyp und Initialwert
	 - verwenden Sie in obiger Definitionszeile keine(!) Anführungszeichen „A“ oder ‚A‘ !!
    - #@IVISIT:CHECKBOX & chbx-dummy & [A,BBBBB,CCC,DDDDD] & dummystr & 0110
         - erzeugt eine Checkbox mit Namen „chbx-dummy“ 
         - man kann jeweils die Einträge "A","BBBBB","CCC","DDDDD" auswählen (binär, Kreuz=‘1‘ oder Leer=‘0‘)
         - Der ausgewählte String (z.B: „0110“, eine Ziffer pro Eintrag) wird im Python-String dummystr gespeicherte
         - String ‘0110‘ ist Initial-Wert als String 
	 - verwenden Sie in obiger Definitionszeile keine(!) Anführungszeichen „0110“ oder ‚0110‘ !!
    - #@IVISIT:RADIOBUTTON & rdbt-dummy & [A,BBBBB,CCC,DDDDD] & dummystr & A
         - erzeugt eine Radiobutton-Box mit Namen „rdbt-dummy“ 
         - man kann genau einen der String Einträge "A","BBBBB","CCC","DDDDD" auswählen 
         - Der ausgewählte String wird im Python-String dummystr gespeicherte
         - String ‘A‘ ist Initial-Wert als String 
	 - verwenden Sie in obiger Definitionszeile keine(!) Anführungszeichen für Strings! 
    - #@IVISIT:BUTTON & bt-dummy & [labeltext,buttontext] & dummystr
         - erzeugt einen Button mit Namen „bt-dummy“
         - Darstellung als „labeltext buttontext“, empfohlen ist „< buttontext“
         - mit labeltext/< kann man Button bewegen; buttontext ist zum Anklicken um den Button zu aktivieren
         - Falls Button geklickt wird, wird Variable dummystr=‘1‘ gesetzt (ansonsten ‘0‘)
         - nach Aufruf von step wird dummystr=‘0‘ zurückgesetzt
	 - verwenden Sie in obiger Definitionszeile keine(!) Anführungszeichen für Strings! 
    - #@IVISIT:IMAGE   & Grauwert-Bild     & 1.0    & [0,255]  & im_gray   & int
         - erzeugt eine Bild mit Namen „Grauwert-Bild“, mit Skalierungsfaktor 1.0 und Wertebereich [0,255] vom Typ int
         - In jedem Simulationsschritt (step) wird der Inhalt der Python-Variable im_gray als Bild im IVisit-GUI 
           dargestellt
    - #@IVISIT:TEXT_OUT & txtout-dummy & [20,5] & list_of_options & dummytextout
         - erzeugt Text-Ausgabe-Box mit Namen txtout-dummy der Größe 20x5, wobei in jedem Simulations-Schritt der 
           Inhalt der Python-Variable als String angezeigt wird
         - list_of_options ist entweder 'None' oder ein einzelner String oder eine Liste aus Strings; 
           mögliche Strings sind 'just_left','just_right','just_center' (default center)
"""


