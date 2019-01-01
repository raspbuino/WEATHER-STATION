#!/usr/bin/python3
#Cron_datupdate.py (=original, Revision AA), -RAW (=login **REMOVED**)
#liest die Datei datupdate.txt, holt die aktuellen Daten
#damit wird die neue index.html neu erstellt
#und diese dann hochgeladen zum Hoster, alle 5min vielleicht

import ftplib

pfad_htmlholen = "/media/pi/Intenso/LOG/"
pfad_datupdate = "/media/pi/Intenso/LOG/"
pfad_htmlbring = "/home/pi/SPRRD/UPLOAD/"
dathtml = []
datupdt = []

#zunächst wird die gesamte index.html in eine Liste gelesen
try:
    fo = open(pfad_htmlholen + "index_basis.html", "r")
    dathtml = fo.readlines()
    fo.close()
    print("[Cron_datupdate]:....index_basisi.html geholt")
except(IOError):
        print("[Cron_datupdate]:....index_basisi.html nicht gefunden")

#jetzt werden die neuen Daten aus datupdate.txt geholt
try:
    fo = open(pfad_datupdate + "datupdate.txt", "r")
    datupdt = fo.readlines()
    fo.close()
    print(datupdt)
    print("jetzt strippen........")
   

    #Jetzt Daten in der Liste ersetzen
    #da müssen die Zeilennummer-Indices aber echt stimmen!!!
	#mit rstrip müssen die \n aus den Listenelementen entfernt werden (P3 S.180)
    dathtml[11] = "<h3>" + datupdt[0].rstrip() + "</h3>" + "\n"
    dathtml[23] = "<td>" + datupdt[1].rstrip() + "</td>" + "\n"
    dathtml[34] = "<td>" + datupdt[2].rstrip() + "</td>" + "\n"
    dathtml[46] = "<td>" + datupdt[3].rstrip() + "</td>" + "\n"
    dathtml[58] = "<td>" + datupdt[4].rstrip() + "</td>" + "\n"
    dathtml[70] = "<td>" + datupdt[5].rstrip() + "</td>" + "\n"
    dathtml[82] = "<td>" + datupdt[6].rstrip() + "</td>" + "\n"
    dathtml[94] = "<td>" + datupdt[7].rstrip() + "</td>" + "\n"
    dathtml[106] = "<td>" + datupdt[8].rstrip() + "</td>" + "\n"

    #und wieder die neue index.html erzeugen
    try:
        fo = open(pfad_htmlbring + "index.html", "w")
        fo.writelines(dathtml)
        fo.close()
		
        print("[Cron_datupdate]:....neue index.html wurde bereitgelegt!")
    except(IOError):
        print("[Cron_datupdate]:....Bereitlegen neue index.html: File nicht gefunden!")

except(IOError):
    print("[Cron_datupdate]:....datupdate.txt nicht gefunden!")
	
#Kontakt zum Server
meinftp = ftplib.FTP("**REMOVED**")
meinftp.login("**REMOVED**","**REMOVED**")
directory_server = "/" #"/" ist ftp-Hauptverzeichnis 
meinftp.cwd(directory_server)

file = open(pfad_htmlbring + "index.html", "rb") #Lesemodus binär
meinftp.storbinary("STOR index.html", file)
file.close()

print(meinftp.quit()) #"höfliches" Trennen meinerseits der ftp-Verbindung
print("[Cron_datupdate]:...die FTP-Verbindung wurde von mir getrennt!")	











