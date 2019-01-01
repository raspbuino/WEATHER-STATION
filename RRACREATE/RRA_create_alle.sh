#da nur je einmal benötigt: Copy n Paste ins Terminal
#----------------------------------------------------
#RRA1: jede Minute für 24h
#RRA2: alle 5 Minuten für 7 Tage
#RRA3: alle 15 Minuten für 30 Tage
#RRA4: alle Stunde für 365 Tage
"""
B1DST1 #=> RRA_TEMPINNEN.rrd  1
B1TCPU #=> RRA_TEMPB1CPU.rrd  2
N1DST1 #=> RRA_TEMPAUSSE.rrd  3
N1VBAT #=> RRA_VOLTAGEN1.rrd  4
N1VCCG #=> RRA_VOLTAGEN1.rrd
N1DH1F #=> RRA_FEUCHTEN1.rrd  5
N1DH1T #=> RRA_TEMPAUSSE.rrd  
N1BM1P #=> RRA_DRUCKBMN1.rrd  6
N1BM1T #=> RRA_TEMPAUSSE.rrd
N1GY1L #=> RRA_LICHTANN1.rrd  7

Stück für Stück ein Beispiel:
rrdtool create CPUTEMP.rrd \
#=> Die DB soll erstellt werden und sie heißt CPUTEMP.rrd

--step 300
alle 300s (=5min) soll ein Temperaturwert in die DB geschrieben werden

DS:
In dieser Zeile, die mit "DS" beginnt, werden die Eigenschaften der
Datenquelle beschrieben (DS steht für Data Source)

TEMP:
das ist der Name der Datenquelle. Dieser kann frei gewählt werden

GAUGE:
Typ der Datenquelle (DST, Data Source Type).
GAUGE bedeutet, dass der übergebene Wert, egal ob positiv oder negativ,
unverändert gespeichert wird. Andere Typen:
COUNTER (speichert die Differenz zum vorherigen Wert)
DERIVE (wie COUNTER aber auch mit negativen Werten)
ABSOLUTE (nimmt an, dass der vorherige Wert nach dem Auslesen immer auf null zurückfällt)

600:
Dieser Wert heißt "Heartbeat". Eigentlich sollte hier alle 300 Sekunden ein Wert in die DB
geschrieben werden. Bleibt einmal ein Wert aus, so akzeptiert RRDtool auch noch später eintreffende Werte,
aber nur bis zu einer maximalen Verzögerung von 600 Sekunden.
Danach wird der Datenpunkt als undefiniert in die DB eingetragen.

-20:90:
Das sind die Minimal und die Maximalwerte, die die DB akzeptiert

RRA:
Schlüsselwort für Round Robin Archive

AVERAGE:
Mehrere Datenpunkte werden zusammengefasst, indem ihr Mittelwert gebildet wird.
Andere Möglichkeiten sind hier
MAX: (der höchste Wert bleibt erhalten)
MIN: (der niedrigste Wert..)
LAST: (der letzte Wert..)

0.5:12:24:
Zwölf Datenpunkte werden zu einem Archiv-Datenpunkt zusammengefasst.
In der RRDtool-Sprache heißen die ursprünglichen Datenpunkte
PDP (Primary Data Points), die konsolidierten Datenpunkte heißen
CDP (Consolidated Data Points)
Von den 12 PDPs müssen mindestens die Hälfte (Faktor 0.5, der sog. X-Files Factor, XFF) gültig sein,
also nicht undefined. Die letzte Zahl bedeutet, dass in diesem RRA 24 CDPs Platz finden.







"""

rrdtool create RRA_TEMPINNEN.rrd \
 --step 60 \
 DS:B1DST1:GAUGE:120:-10:45 \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760

#hier mit zwei Sensoren (DS18B20 und DHT22)
rrdtool create RRA_TEMPINNEN.rrd \
 --step 60 \
 DS:B1DST1:GAUGE:120:-10:45 \
 DS:B1DH1T:GAUGE:120:-10:45 \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760 

rrdtool create RRA_TEMPAUSSE.rrd \
 --step 60 \
 DS:N1DST1:GAUGE:120:-30:70 \
 DS:N1DH1T:GAUGE:120:-30:70 \
 DS:N1BM1T:GAUGE:120:-30:70 \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760

rrdtool create RRA_TEMPB1CPU.rrd \
 --step 60 \
 DS:B1TCPU:GAUGE:120:0:130 \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760

rrdtool create RRA_VOLTAGEN1.rrd \
 --step 60 \
 DS:N1VBAT:GAUGE:120:500:3500 \
 DS:N1VCCG:GAUGE:120:500:4000 \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760

rrdtool create RRA_FEUCHTEN1.rrd \
 --step 60 \
 DS:N1DH1F:GAUGE:120:-10:110 \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760

rrdtool create RRA_FEUCHTEB1.rrd \
 --step 60 \
 DS:B1DH1F:GAUGE:120:-10:110 \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760 

rrdtool create RRA_DRUCKBMN1.rrd \
 --step 60 \
 DS:N1BM1P:GAUGE:120:950:1100 \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760

rrdtool create RRA_LICHTANN1.rrd \
 --step 60 \
 DS:N1GY1L:GAUGE:120:-100:U \
 RRA:AVERAGE:0.5:1:1440 \
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:AVERAGE:0.5:60:8760 \
 RRA:MAX:0.5:1:1440 \
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MAX:0.5:60:8760 \
 RRA:MIN:0.5:1:1440 \
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880 \
 RRA:MIN:0.5:60:8760

   
  
 
