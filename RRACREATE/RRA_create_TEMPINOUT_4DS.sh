#da nur je einmal benötigt: Copy n Paste ins Terminal
#----------------------------------------------------
#RRA1: jede Minute für 24h
#RRA2: alle 5 Minuten für 7 Tage
#RRA3: alle 15 Minuten für 30 Tage
#RRA4: alle Stunde für 365 Tage

rrdtool create RRD_TEMPINOUT.rrd \
 --step 60 \
 DS:N1DST1:GAUGE:120:-30:70 \
 DS:N1DH1T:GAUGE:120:-30:70 \
 DS:N1BM1T:GAUGE:120:-30:70 \
 DS:B1DST1:GAUGE:120:-30:70 \
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
 
