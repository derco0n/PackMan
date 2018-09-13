# PackMan
Programm zur (E-Mail-)Benachrichtung von eingegangen Sendungen.


Ursprüglicher Zweck dieses Programms ist die Meldung von eingegangenen Sendungen im Wareneingang an die jeweilige Abteilung.

Zur Realisierung wird ein Raspberry-Pi3 mit einem PiFace2-Hat verwendet, welches auf bestimmte Sensoren (Schalterzustand, Waage, Lichtschranke oder ähnlich reagiert) und entsprechend die zugehörige Abteilung benachrichtigt.

Gedanke:
-Ware für Abteilung x kommt an und wird in zugehöriges Ablagefach einsortiert.
-Am entsprechenden Fach ist ein entsprechender Sensor/Schalter angebracht welcher ausgelöst/betätigt wird
-Durch die Sensorauslösung wird eine entsprechende Benachrichtigung (z.B.: per E-Mail) für Abteilung x generiert
-Sobald die Ware aus dem Fach entnommen wird, wird durch erneute Schalterbetätigung/Sensorauslösung das Fach zurückgesetzt.
