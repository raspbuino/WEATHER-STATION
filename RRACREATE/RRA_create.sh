#da nur je einmal benötigt: Copy n Paste ins Terminal

#cputemp.rrd
rrdtool create cputemp.rrd \
 --step 60 \
 DS:Tcpu:GAUGE:120:-20:120 \
 RRA:AVERAGE:0.5:5:60 \
 RRA:AVERAGE:0.5:15:672

#-------------------------------------------
#temptest.rrd
#RRA1: jede Minute für 24h
#RRA2: alle 5 Minuten für 7 Tage
#RRA3: alle 15 Minuten für 30 Tage

rrdtool create temptest.rrd \
 --step 60 \
 DS:Tcpu:GAUGE:120:U:U \
 DS:Tmas:GAUGE:120:U:U \
 RRA:AVERAGE:0.5:1:1440
 RRA:AVERAGE:0.5:5:2016 \
 RRA:AVERAGE:0.5:15:2880 \
 RRA:MAX:0.5:1:1440
 RRA:MAX:0.5:5:2016 \
 RRA:MAX:0.5:15:2880 \
 RRA:MIN:0.5:1:1440
 RRA:MIN:0.5:5:2016 \
 RRA:MIN:0.5:15:2880
