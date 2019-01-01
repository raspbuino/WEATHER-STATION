#!/usr/bin/python3
#ftp_upload_graph_alle_h.py (=original, Revision AA), -RAW (=login **REMOVED**)
#Diagramme 03h, 24h, 36h
import ftplib

path_UPL="/home/pi/SPRRD/UPLOAD/" #lokales Upload-Verzeichnis

#Definition Dateiliste
Liste_Graphen = ["graphDRUCKBMN1_03h.gif",
"graphFEUCHTEN1_03h.gif",
"graphFEUCHTEB1_03h.gif",
"graphLICHTANN1_03h.gif",
"graphTEMPAUSSE_03h.gif",
"graphTEMPB1CPU_03h.gif",
"graphVOLTAGEN1_03h.gif",
"graphTEMPINNEN_03h.gif",
"graphDRUCKBMN1_24h.gif",
"graphFEUCHTEN1_24h.gif",
"graphFEUCHTEB1_24h.gif",
"graphLICHTANN1_24h.gif",
"graphTEMPAUSSE_24h.gif",
"graphTEMPB1CPU_24h.gif",
"graphVOLTAGEN1_24h.gif",
"graphTEMPINNEN_24h.gif",
"graphDRUCKBMN1_36h.gif",
"graphFEUCHTEN1_36h.gif",
"graphFEUCHTEB1_36h.gif",
"graphLICHTANN1_36h.gif",
"graphTEMPAUSSE_36h.gif",
"graphTEMPB1CPU_36h.gif",
"graphVOLTAGEN1_36h.gif",
"graphTEMPINNEN_36h.gif"]

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

