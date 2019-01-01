#!/usr/bin/python3
#xensors-AA.py

import Adafruit_DHT

class xsCPU:

    def __init__(self):
        self.path = "/sys/class/thermal/thermal_zone0/temp"
        self.lastvalidvalue = 0
        self.sumvalue = 0
        self.valuecounts = 0

    def read_value(self):
        try:
            file = open(self.path)
            actualvalue = file.readline()
            file.close()
            actualvalue = float(actualvalue) #noch Faktor 1000 drin
            if 0 < actualvalue <130000: #Plausicheck
                self.lastvalidvalue = actualvalue
            else:
                actualvalue = self.lastvalidvalue
        except (IOError, ValueError):
            actualvalue = self.lastvalidvalue
            print("[xsCPU, read_value, Exception]: IOError oder ValueError!")
        self.sumvalue += actualvalue
        self.valuecounts += 1
        return(actualvalue)

    def pull_meanvalue(self):
        meanvalue = self.sumvalue/self.valuecounts
        return(meanvalue)

    def pull_valuecounts(self):
        return(self.valuecounts)

    def pull_lastvalidvalue(self):
        return(self.lastvalidvalue)

    def meanvalue_reset(self):
        self.sumvalue = 0
        self.valuecounts = 0


class xsDS18B20:

    def __init__(self, sensoraddress):
        self.sensoraddress = sensoraddress # z.B.: "28-0415a4a8c7ff"
        self.lastvalidvalue = 0
        self.sumvalue = 0
        self.valuecounts = 0

    def read_value(self):
        try:
            file = open("/sys/devices/w1_bus_master1/"+str(self.sensoraddress)+"/w1_slave")
            filecontent = file.read()
            file.close()
            secondline = filecontent.split("\n")[1]
            temperaturedata = secondline.split(" ")[9]
            actualvalue = float(temperaturedata[2:]) #noch Faktor 1000 drin
            if -30000 < actualvalue < 70000: #Plausicheck
                self.lastvalidvalue = actualvalue
            else:
                actualvalue = self.lastvalidvalue
        except (IOError, ValueError):
            actualvalue = self.lastvalidvalue
            print("[xsDS18B20, read_value, Exception]: IOError oder ValueError!")
        self.sumvalue += actualvalue
        self.valuecounts += 1
        return(actualvalue)

    def pull_meanvalue(self):
        meanvalue = self.sumvalue/self.valuecounts
        return(meanvalue)

    def pull_valuecounts(self):
        return(self.valuecounts)

    def pull_lastvalidvalue(self):
        return(self.lastvalidvalue)

    def meanvalue_reset(self):
        self.sumvalue = 0
        self.valuecounts = 0


class xsDHT22:

    def __init__(self, GPIO_BCM):
        self.GPIO_BCM = GPIO_BCM # z.B.: 2
        self.feuchte_lastvalidvalue = 0
        self.temperatur_lastvalidvalue = 0
        self.feuchte_sumvalue = 0
        self.temperatur_sumvalue = 0
        self.valuecounts = 0

    def read_value(self):
        feuchte, temperatur = Adafruit_DHT.read(Adafruit_DHT.DHT22, self.GPIO_BCM) # Data an GPIO 2
        if -20 < temperatur < 50: #Plausicheck Temperatur
            self.temperatur_lastvalidvalue = temperatur
        else:
            temperatur = self.temperatur_lastvalidvalue
        self.temperatur_sumvalue += temperatur
        if -10 < feuchte < 110: #Plausicheck Feuchte
            self.feuchte_lastvalidvalue = feuchte
        else:
            feuchte = self.feuchte_lastvalidvalue
        self.feuchte_sumvalue += feuchte
        self.valuecounts += 1
        return(feuchte, temperatur)

    def pull_feuchte_meanvalue(self):
        feuchte_meanvalue = self.feuchte_sumvalue/self.valuecounts
        return(feuchte_meanvalue)

    def pull_temperatur_meanvalue(self):
        temperatur_meanvalue = self.temperatur_sumvalue/self.valuecounts
        return(temperatur_meanvalue)

    def pull_valuecounts(self):
        return(self.valuecounts)

    def pull_feuchte_lastvalidvalue(self):
        return(self.feuchte_lastvalidvalue)

    def pull_temperatur_lastvalidvalue(self):
        return(self.temperatur_lastvalidvalue)

    def meanvalue_reset(self):
        self.feuchte_sumvalue = 0
        self.temperatur_sumvalue = 0
        self.valuecounts = 0

