#!/usr/bin/python3
#SPRRD_V7draft-AB.py
#Hauptprogramm

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24 #see BLavery/lib_nrf24 /change: line 374 added: self.spidev.max_speed_hz = 100000
import time
import spidev
import rrdtool #pip3
import Adafruit_DHT
import csv
import xensors

#Pfade---------------------------------------------------------------------
pfad_LOG = "/media/pi/Intenso/LOG/"
pfad_RRA = "/home/pi/SPRRD/RRA/"
pfad_UPL = "/home/pi/SPRRD/UPLOAD/"

#Logdateien----------------------------------------------------------------
dEvents = "eventlog.txt"
#--------------------------------------------------------------------------

roehre = [0xF0, 0xF0, 0xF0, 0xF0, 0xD2]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17) #def begin(self, csn_pin, ce_pin=0): # csn & ce are RF24 terminology. csn = SPI's CE!
time.sleep(1)
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x2a) #(0x2a)#42

print("getChannel()= ", radio.getChannel())

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_HIGH)
radio.openReadingPipe(0, roehre)
print("DETAILS...")
radio.printDetails()
time.sleep(2)
Durchgangsnr = 0
Hauptloopnr = 0

payload = []
datzeile = []
timeout = 50     #[s] 50 geht so, 90 geht net
schlafzeit = 1   #[s]
B1intervall = 5

N1DH1T_last = 0
N1DH1F_last = 0
N1DST1_last = 0
B1DST1_last = 0
B1TCPU_last = 0
B1DH1F_last = 0
B1DH1T_last = 0
DHTfehlerN1 = 0
DHTfehlerB1 = 0

Teiler_B1DH1F = 0
Teiler_B1DH1T = 0

B1counter = 0
B1Messnr = 0

B1DST1 = 0 #Basis1 DS18B20 Temperatur T1
B1TCPU = 0 #Basis1 CPU Temperatur
B1DH1F = 0 #Basis1 DHT22 Nr1 rel. Feuchte (an Pin3=GPIO2)
B1DH1T = 0 #Basis1 DHT22 Nr1 Temperatur
N1DST1 = 0 #Node1  DS18B20 Temperatur T1
N1VBAT = 0 #Node1  Voltage Batterien
N1VCCG = 0 #Node1  Voltage geregelt (3.3V)
N1DH1F = 0 #Node1  DHT22 Nr1 rel. Feuchte
N1DH1T = 0 #Node1  DHT22 Nr1 Temperatur
N1BM1P = 0 #Node1  BMP180 Nr1 Druck (QFE auf 100m)
N1BM1T = 0 #Node1  BMP180 Nr1 Temperatur
N1GY1L = 0 #Node1  GY30 Lichtsensor

#xensors initialisieren ------------
xsB1TCPU = xensors.xsCPU()
xsB1DST1 = xensors.xsDS18B20("28-0415a4a8c7ff")

#Funktionen-------------------------------------------------------------
#neuerLogeintrag => nur bei besoderen Events ein Eintrag mit Zeitstempel
def neuerLogeintrag(logtext):
    try:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(pfad_LOG + dEvents, "a") as out:
            logstr = ("[" + timestr + "]: (" + str(Hauptloopnr) + ") " + logtext)
            out.write(logstr + "\n")
            print("....es wurde ins Logfile geschrieben")
            print(logstr)
    except(IOError):
        print("Logfile nicht gefunden...")
#-----------------------------------------------------------------------

neuerLogeintrag("Programmneustart: SPRRD_V7draft.py")
payload_vorhanden = False

#-----------------------------------------------------------------------

while True:
    timeout_start = time.time()
    Durchgangsnr = 0
    B1DST1sum = 0
    B1TCPUsum = 0
    B1DH1Tsum = 0
    B1DH1Fsum = 0

    while time.time() < timeout_start + timeout:
        Durchgangsnr += 1

#kurz nach Daten am Funk lauschen, ansonsten Daten am Master sammeln
        radio.startListening()
        if radio.available(0): #sind Daten verfügbar
            #while radio.available(0):
            print("Daten verfügbar, Durchgangsnr=", Durchgangsnr-1)
            radio.read(payload, 32) #PayloadSize ist bekannt und fix (=32 Bytes)

            print(payload)

#die 8 einzelnen Payloadpakete rausschneiden, umwandeln in Fließkomazahlen mit zwei Dezimalstellen
            N1gauges=[round((int.from_bytes(payload[(i*4):(i*4+4)],byteorder="little",signed=True))/100,2) for i in range(0,8)]
            #Namenszuordnung
            N1DST1 = N1gauges[0] #[°C]  DS18B20
            N1VBAT = N1gauges[1] #[mV]
            N1VCCG = N1gauges[2] #[mV]
            N1DH1F = N1gauges[3] #[%]   DHT22
            N1DH1T = N1gauges[4] #[°C]  DHT22
            N1BM1P = N1gauges[5] #[hPa] BMP180 (QFE 100m)
            N1BM1T = N1gauges[6] #[°C]  BMP180
            N1GY1L = N1gauges[7] #[lx]  Licht

            #Sonderbehandlung einiger Werte, der DHT22 spinnt ab und an und wirft abstruse Werte aus
            if -30 < N1DH1T < 70:             #alles gut, neuer letzter Wert wird gesetzt
                N1DH1T_last = N1DH1T
            else:                             #DHT spinnt => auf letzten Wert zurückgreifen
                N1DH1T = N1DH1T_last
                DHTfehlerN1 += 1

            if -10 < N1DH1F < 110:            #alles gut, neuer letzter Wert wird gesetzt
                N1DH1F_last = N1DH1F
            else:                             #DHT spinnt => auf letzten Wert zurückgreifen
                N1DH1F = N1DH1F_last

            if -30 < N1DST1 < 70:             #Plausicheck Temperatur
                N1DST1_last = N1DST1
            else:
                N1DST1 = N1DST1_last

            payload_vorhanden = True
            radio.stopListening()

        time.sleep(schlafzeit)

#Lokale Daten aus den Dateien alle B1intervall mal auslesen (also nicht zu oft...)
        B1counter += 1
        if B1counter >= B1intervall:
            B1Messnr += 1

            B1DST1 = xsB1DST1.read_value()
            B1TCPU = xsB1TCPU.read_value()

#DHT22 an Basis 1 auslesen (max alle 2 Sekunden!)
            B1DH1F, B1DH1T = Adafruit_DHT.read(Adafruit_DHT.DHT22, 2) # Data an GPIO 2
            time.sleep(schlafzeit)
            try:
                if -10 < B1DH1T < 40:
                    B1DH1Tsum = B1DH1Tsum + B1DH1T
                    Teiler_B1DH1T += 1
                    B1DH1T = round(B1DH1T, 2)
            except(TypeError):
                #neuerLogeintrag("[Main]/Exception:....B1DH1T TypeError")
                print("[Main]/Exception:....B1DH1T TypeError!")

            #Feuchte näher betrachtet. Messsumme wird nur hochgezählt, wenn ok
            try:
                if -10 < B1DH1F < 110:
                    B1DH1Fsum = B1DH1Fsum + B1DH1F
                    Teiler_B1DH1F += 1
                    B1DH1F = round(B1DH1F, 2)
            except(TypeError):
                DHTfehlerB1 += 1
                #neuerLogeintrag("[Main]/Exception:....B1DH1F TypeError")
                print("[Main]/Exception:....B1DH1F TypeError!")
#-----------------------------------------------------------------------

            print("DgNr:", Durchgangsnr, " B1ct:", B1counter,
            " Tlr_B1DH1F:", Teiler_B1DH1F, " Tlr_B1DH1T:", Teiler_B1DH1T,
            " B1DST1:", B1DST1, " B1TCPU:", B1TCPU,
            " B1DH1T:", B1DH1T, " B1DH1F:", B1DH1F)

            #B1counter wieder auf Null setzen
            B1counter = 0

#Timeout fürs Datensammeln
    #summierte Daten mitteln
    #B1DST1 = round(B1DST1sum/B1Messnr/1000, 2)
    #B1TCPU = round(B1TCPUsum/B1Messnr/1000, 2)
    B1DST1 = round(xsB1DST1.pull_meanvalue()/1000, 2) ######neu
    xsB1DST1.meanvalue_reset()                        ######neu
    B1TCPU = round(xsB1TCPU.pull_meanvalue()/1000, 2) ######neu
    xsB1TCPU.meanvalue_reset()                        ######neu

    if Teiler_B1DH1T != 0: #d.h. da gab es nicht nur Fehler in der Schleife
        B1DH1T = round(B1DH1Tsum/Teiler_B1DH1T, 2)
        B1DH1T_last = B1DH1T
    else:
        neuerLogeintrag("[Main]:....nach Summierung: B1DH1T nochmal alter  B1DH1T_last!")
        print("[Main]/else:....Teiler_B1DH1T ist NULL => Zuordnung alter Wert: ", B1DH1T_last)
        B1DH1T = B1DH1T_last

    if Teiler_B1DH1F != 0: #dito
        B1DH1F = round(B1DH1Fsum/Teiler_B1DH1F, 2)
        B1DH1F_last = B1DH1F
    else:
        neuerLogeintrag("[Main]:....nach Summierung: B1DH1F nochmal alter Wert B1DH1F_last!")
        print("[Main]/else:....Teiler_B1DH1F ist NULL => Zuordnung alter Wert: ", B1DH1F_last)
        B1DH1F = B1DH1F_last

    B1Messnr = 0
    Teiler_B1DH1F = 0
    Teiler_B1DH1T = 0


    #Printausgabe
    print("Durchgangsnr=", Durchgangsnr-1)
    print("B1DST1=", B1DST1, "[°C]")
    print("B1TCPU=", B1TCPU, "[°C]")
    print("B1DH1T=", B1DH1T, "[°C]")
    print("B1DH1F=", B1DH1F, "[%]")
    print("DHTfehlerN1:", DHTfehlerN1)
    print("DHTfehlerB1:", DHTfehlerB1)
    #if payload_vorhanden:
    print("N1DST1=", N1DST1, "[°C]")
    print("N1VBAT=", N1VBAT, "[mV]")
    print("N1VCCG=", N1VCCG, "[mV]")
    print("N1DH1F=", N1DH1F, "[%]")
    print("N1DH1T=", N1DH1T, "[°C]")
    print("N1BM1P=", N1BM1P, "[hPa] QFE")
    print("N1BM1T=", N1BM1T, "[°C]")
    print("N1GY1L=", N1GY1L, "[lx]")

    #Daten in Datei hinterlegen
    print("[Main]:....START datupdate.txt schreiben!")
    timestr1 = time.strftime("%d.%m.%Y")
    timestr2 = time.strftime("%H:%Mh")
    strupdate = ("akt. Update: " + timestr1 + " um " + timestr2)

    datzeile = [strupdate + "\n",
    str(N1DST1) + "\n",
    str(B1DST1) + "\n",
    str(N1DH1F) + "\n",
    str(B1DH1F) + "\n",
    str(N1BM1P) + "\n",
    str(N1GY1L) + "\n",
    str(N1VBAT) + "\n",
    str(B1TCPU) + "\n"]
    try:
        fo = open(pfad_LOG + "datupdate.txt", "w")
        fo.writelines(datzeile)
        fo.close()
        print("[Main]:....ENDE datupdate.txt schreiben!")
    except(IOError):
        print("[Main]/Exception:....File datupdate.txt nicht gefunden!")

    #RRD-Updates
    print("-------------START RRD-UPDATES...")

    if Hauptloopnr > 1:
        rrdtool.update(pfad_RRA+"RRA_TEMPINNEN.rrd", "N:"+str(B1DST1)+":"+str(B1DH1T))
        rrdtool.update(pfad_RRA+"RRA_TEMPB1CPU.rrd", "N:"+str(B1TCPU))
        rrdtool.update(pfad_RRA+"RRA_FEUCHTEB1.rrd", "N:"+str(B1DH1F))
        print("1. RRA_TEMPINNEN.rrd")
        print("2. RRA_TEMPB1CPU.rrd")
        print("3. RRA_FEUCHTEB1.rrd")

        #Payloaddaten
        rrdtool.update(pfad_RRA+"RRA_TEMPAUSSE.rrd", "N:"+str(N1DST1)+":"+str(N1DH1T)+":"+str(N1BM1T))
        rrdtool.update(pfad_RRA+"RRA_FEUCHTEN1.rrd", "N:"+str(N1DH1F))
        rrdtool.update(pfad_RRA+"RRA_VOLTAGEN1.rrd", "N:"+str(N1VBAT)+":"+str(N1VCCG))
        rrdtool.update(pfad_RRA+"RRA_LICHTANN1.rrd", "N:"+str(N1GY1L))
        rrdtool.update(pfad_RRA+"RRA_DRUCKBMN1.rrd", "N:"+str(N1BM1P))
        print("3. RRA_TEMPAUSSE.rrd")
        print("4. RRA_FEUCHTEN1.rrd")
        print("5. RRA_VOLTAGEN1.rrd")
        print("6. RRA_LICHTANN1.rrd")
        print("8. RRA_DRUCKBMN1.rrd")
        print("-------------ENDE RRD-UPDATES...")

        #CSV schreiben
        try:
            timestralles = time.strftime("%Y%m%d-%H%M%S")
            timestrmonat = time.strftime("%Y%m")
            with open(pfad_LOG + "sprrdlog_" + timestrmonat + ".csv", "a") as out:
                cw = csv.writer(out, delimiter=";", lineterminator="\n")
                cw.writerow([timestralles, Hauptloopnr, Durchgangsnr-1,
                DHTfehlerN1, DHTfehlerB1, B1DST1, B1TCPU, N1DST1, N1VBAT,
                N1VCCG,N1DH1F,N1DH1T,N1BM1P, N1BM1T, N1GY1L, B1DH1T, B1DH1F,
                payload_vorhanden])
                print("[Main, CSV schreiben]:....wurde ins Logfile geschrieben!")
        except(IOError):
            print("[Main, CSV schreiben]/Exception:....Logfile nicht gefunden!")

    else:
        neuerLogeintrag("[Main]:....ein nullter Hauptloop, kein Datenlog!")
    payload_vorhanden = False
    Hauptloopnr += 1


###################################
#immer, wenn Daten empfangen wurden, sollen alle RRAs aktualisiert werden
#Datenauswertung NODE1 via nRF24L01+
#Beispiel: payload =
#[5,0,0,0,15,0,0,0,205,0,0,0,189,11,0,0,69,156,0,0,37,161,7,0,133,141,91,0,133,29,44,4]
#[PL01---|PL02----|PL03-----|PL04------|PL05------|PL06------|PL07--------|PL08-------|
#|5      |15      |205      |3005      |40005     |500005    |6000005     |70000005   |
#|0..3   |4..7    |8..11    |12..15    |16..19    |20..23    |24..27      |28..31     |


"""
            try:
                #Temperatur B1DST1 aus Datei einlesen
                file = open("/sys/devices/w1_bus_master1/28-0415a4a8c7ff/w1_slave")
                filecontent = file.read()
                file.close()
                secondline = filecontent.split("\n")[1]
                temperaturedata = secondline.split(" ")[9]
                B1DST1 = float(temperaturedata[2:]) #noch Faktor 1000 drin
                #Plausicheck (in der Datei ist noch Faktor 1000)
                if -30000 < B1DST1 < 70000:
                    B1DST1_last = B1DST1
                else:
                    B1DST1 = B1DST1_last
                    neuerLogeintrag("B1DST1 war außer Range")
                #Messsumme bilden, so oder so
                B1DST1sum = B1DST1sum + B1DST1
            except (IOError, ValueError):
                B1DST1 = B1DST1_last #nochmal den bisherigen Wert verwenden
                B1DST1sum = B1DST1sum + B1DST1
                neuerLogeintrag("Exception: B1DST1 IOError oder ValueError")
                print("IO-Error (BS1DST1) trat auf - wurde aber sauber abgefangen")

            try:
                #Temperatur B1TCPU aus Datei einlesen
                file = open("/sys/class/thermal/thermal_zone0/temp")
                B1TCPU = file.readline()
                file.close()
                B1TCPU = float(B1TCPU) #noch Faktor 1000 drin
                #Plausicheck (in der Datei ist noch Faktor 1000 drin)
                if 0 < B1TCPU <130000:
                    B1TCPU_last = B1TCPU
                else:
                    B1TCPU = B1TCPU_last
                    neuerLogeintrag("[Main]/else:....B1TCPU war außer Range, wird nicht gezählt")
                    #Messsumme bilden
                B1TCPUsum = B1TCPUsum + B1TCPU
            except (IOError, ValueError):
                B1TCPU = B1TCPU_last #nochmal den bisherigen Wert verwenden
                B1TCPUsum = B1TCPUsum + B1TCPU
                neuerLogeintrag("[Main]/Exception:....B1TCPU IOError oder ValueError")
                print("[Main]/Exception:....B1TCPU IOError oder ValueError!")
"""




