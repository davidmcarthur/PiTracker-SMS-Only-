import sys
import time
import serial
import trackerUtils
from _datetime import datetime

class fonaGPS(object):
    global ser
##    ser = serial.Serial(
##    "/dev/serial0",
##    baudrate=115200,
##    parity=serial.PARITY_NONE,
##    stopbits=serial.STOPBITS_ONE,
##    bytesize=serial.EIGHTBITS,
##    timeout = 1,
##    )
    global piLog
    ser = trackerUtils.openSerialPort()
    piLog = "piTracker-" + str(time.time()) + ".log"
    trackerUtils.initFile(piLog)

    def openGPS(self):
        #ser.open()
        print("Turning on the GPS\r")
        ser.write(b'AT+CGNSPWR=1\r')  # Turn on the GPS
        time.sleep(1)
        # Check GPS power status is ON!
        while True:
            ser.write(b'AT+CGNSPWR?\r')
            gpsPower = ser.readline()
            if b'1' in gpsPower:
                print("GPS is powered on")
                return True
            else:
                print("GPS has no power")
                print("GPS is off. Turning on...")
                trackerUtils.writeToFile(piLog, ("GPS status is " + gpsPower.decode()))
                ser.write(b'AT+CGNSPWR=1')  # Power on GPS module
        time.sleep(0.5)
        ser.write(b'AT+CGNSRST=1\r')  # GPS reset set to hot start mode
        #ser.close()
        return True
        
    # Check to see if the GPS has aquired any satellites
    def getGPSFix(self):
        #ser.open()
        print("Checking for GPS Fix")
        ser.write(b'AT+CGPSSTATUS?\r')
        gpsFix = ser.readline()
        while b'+CGPSSTATUS: Location Not Fix' in gpsFix:
            time.sleep(5) # Wait for GPS fix
            ser.write(b'AT+CGPSSTATUS?\r')
        #ser.close()
        print("GPS location is fixed")
        return True    
        
    # Get GPS Coordinates
    def getGPS(self):
        #ser.open()
        print("Getting GPS Data\r")
        while True:
            ser.write(b'AT+CGNSINF \r')
            global gpsCoord
            gpsCoord = ser.readline()
            if b'+CGNSINF: ' in gpsCoord:  # 1 = gps fix, 0 = no fisx
                print(gpsCoord)
                return gpsCoord
                return True
            if b'ERROR' in gpsCoord:
                trackerUtils.writeToFile(piLog, "Error in GPS Coord: " + gpsCoord.decode())
            ser.write(b'AT+CGNSINF=0\r')
        ser.__del__()

    # converts Rx data to Decimal Degree format
    def convertGPS(self, gpsV1):
        global deg
        deg = chr(37)
        array = gpsV1.split(b',')
        #### Format from DDMM.MMMMMM to DD MM.MMMMMM
        # Latitude
        global latDeg
        global latMin
        lat = array[1]  # text array pull latitude from input
        latDeg = int(float(lat)/100)            # Retrieves DD
        latMin = float(lat)-latDeg*100
        latMin = latMin/60
        latitude = latDeg+latMin
        latitude = str(latitude)
        print(latitude + " is decimal degree latitude")
    
        # Longitude
        global lonDeg
        global lonMin
        lon = array[2]                      	# text array pulling longitude
        lonDeg = int(float(lon)/100)
        lonMin = float(lon)-lonDeg*100
        lonMin = lonMin/60
        longitude = lonDeg+lonMin
        longitude = str(longitude)
        print(longitude + " is decimal degree longitude")
    
        # Altitude
        global alt
        alt = array[3]
        print('GPS Altitude is ' + alt.decode())
    
        # Time UTCGetting
        global utc
        utc = array[4]
        print('UTC time is ' + utc.decode())
    
        # Speed in knots
        global speed
        speed = array[7]
        print('speed in knots is ' + speed.decode())
    
        # Heading in Degrees
        global heading
        heading = array[8]
        print('Heading is ' + heading.decode() + ' degrees')
    
        # Write parsed GPS to Log file
        gpsMsg1 = (latitude + "," + longitude + " Fix Coords in Decimal Degree")
        trackerUtils.writeToFile(piLog, gpsMsg1)
        gpsMsg2 = (b'Altitude: ' + alt + b' meters, Speed: ' + speed + b' knots, Heading: ' + heading + b' Time: ' + utc + b' UTC')
        trackerUtils.writeToFile(piLog, str(gpsMsg2)) 
        
        # Google Maps link
        global gMapsLink
        gMapsLink = ("https://www.google.com/maps/@" + latitude + "," + longitude)
        print(gMapsLink)
        return [alt.decode(), utc.decode(), speed.decode(), heading.decode(), latitude, longitude]
        #return gMapsLink
