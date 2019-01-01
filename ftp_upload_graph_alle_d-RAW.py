#!/usr/bin/python3
#ftp_upload_graph_alle_d.py (=original, Revision AA), -RAW (=login **REMOVED**)
#Diagramme 07d und 30h
import ftplib

path_UPL="/home/pi/SPRRD/UPLOAD/" #lokales Upload-Verzeichnis

#Definition Dateiliste
Liste_Graphen = [
"graphDRUCKBMN1_07d.gif",
"graphFEUCHTEN1_07d.gif",
"graphFEUCHTEB1_07d.gif",
"graphLICHTANN1_07d.gif",
"graphTEMPAUSSE_07d.gif",
"graphTEMPB1CPU_07d.gif",
"graphVOLTAGEN1_07d.gif",
"graphTEMPINNEN_07d.gif",
"graphDRUCKBMN1_30d.gif",
"graphFEUCHTEN1_30d.gif",
"graphFEUCHTEB1_30d.gif",
"graphLICHTANN1_30d.gif",
"graphTEMPAUSSE_30d.gif",
"graphTEMPB1CPU_30d.gif",
"graphVOLTAGEN1_30d.gif",
"graphTEMPINNEN_30d.gif"]

#Kontakt zum Server
meinftp = ftplib.FTP("**REMOVED**")
meinftp.login("**REMOVED**","**REMOVED**")
directory_server = "/Bilder/Bilder02/" #"/" ist ftp-Hauptverzeichnis
meinftp.cwd(directory_server)

print("Inhalt vorher von:", directory_server)
meinftp.retrlines("LIST")

#Die einzelnen Listenelemente hochladen
for Listenelement in Liste_Graphen:
    #print(path_UPL+x)
    file = open(path_UPL+Listenelement, "rb") #Lesemodus binär
    meinftp.storbinary('Stor '+Listenelement, file)
    file.close()

print("ftp: So sieht der Inhalt von ",directory_server, " nach dem Upload aus:")
meinftp.retrlines("LIST")
#print("Die lokale Datei " + directory_local+filename +" wird geschlossen.")
#file.close()
print(meinftp.quit()) #"höfliches" Trennen meinerseits der ftp-Verbindung
print('Die FTP-Verbindung wurde von mir getrennt.')

