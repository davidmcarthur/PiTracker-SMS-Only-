import serial
from curses.ascii import ascii, alt
from time import sleep
from FONA_GPS import fonaGPS
from FONA_SMS import fonaSMS
import trackerUtils
import os
import time
import readline
from queue import Full
import json
import mimetypes
    
#Get GPS Data
GPSData = fonaGPS()
GPSData.openGPS()
GPSData.getGPSFix()
rawGPS = GPSData.getGPS()
fullLocData = GPSData.convertGPS(rawGPS)
for f in fullLocData:
    print(f)
# Do database things
conn = trackerUtils.initDB()
db = conn.database()
currentLat = db.child("current-location").child("latitude").get()
currentLong = db.child("current-location").child("longitude").get()
latLong = str(currentLat.val()) + ',' + str(currentLong.val())
print("The current GPS coordinates are " + latLong)
data = {"altitude": fullLocData[0], "latitude": fullLocData[4], "longitude": fullLocData[5], "speed": fullLocData[2]}
db.child("current-location").push(data)

device = fonaSMS()
device.checkFONA()
device.initSMS()

smsRecipient = "555-555-5555"

# Send GPS data to text
device.sendSMS(smsRecipient, latLong)

#time.sleep(10)      #time for FONA to send SMS???

#### needs IP connection HERE
##os.system("sudo pon fona")
#time.sleep(5)

# close IP connection HERE

##time.sleep(10)
##os.system("sudo poff fona")



