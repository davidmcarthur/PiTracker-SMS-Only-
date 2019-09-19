import sys
import time
import serial
import trackerUtils
from builtins import ascii

class fonaSMS(object):
    global ctrlZ
    ctrlZ = chr(26)
        
    global ser
    global piLog
    print("setup SMS Serial")
    ser = trackerUtils.openSerialPort()
    print("Connected to " + ser.name + "\r")
    piLog = "piTracker-" + str(time.time()) + ".log"
    trackerUtils.initFile(piLog)
    print("SMS serial complete")
    trackerUtils.writeToFile(piLog, "Connected to " + ser.name)

##    #serial setupGPS
##    ser = serial.Serial(
##    "/dev/serial0",
##    baudrate=115200,
##    parity=serial.PARITY_NONE,
##    stopbits=serial.STOPBITS_ONE,
##    bytesize=serial.EIGHTBITS,
##    timeout = 1,)     

    # CHECK FONA
    def checkFONA(self):
        # SETUP SERIAL MODEM FOR PI/FONA
        #ser.open()
        while True:
            ser.write(b'AT\r')
            fonaStatus = ser.readline()
            if b'OK' in fonaStatus:
                print(b'The FONA is ' + fonaStatus)
                return True
            if b'ERROR' in fonaStatus:
                trackerUtils.writeToFile(piLog, ("FONA status is " + fonaStatus)) 
                print(b'The FONA is ' + fonaStatus)
        #ser.close()
        return True
            
    def initSMS(self):
        #ser.open()
        smsStatus = "SMS Status Default"
        print("init SMS")
        while True:
            ser.write(b'AT+CMGF=1\r')            # Set SMS mode to TEXT
            smsStatus = ser.readline()
            if b'OK' in smsStatus:
                print('SMS status is ' + smsStatus.decode() + ". Modem set to text mode")        
                trackerUtils.writeToFile(piLog, 'SMS status is ' + smsStatus.decode() + " Modem set to text mode")
                return True
            if b'ERROR' in smsStatus:
                trackerUtils.writeToFile(piLog, (("SMS status is " + smsStatus.decode())))
                ser.write(b'AT+CMGF=1\r')
            time.sleep(1)
        #ser.close()
    
    # Send SMS
    def sendSMS(self, recipient, message):
        #ser.open()
        try:
            def get_num(x):
                return str("".join(ele for ele in x if ele.isdigit()))
            print("called Send SMS")
            print("sending SMS")
            ser.write(('AT+CMGS="%s"\r' % recipient).encode())
            time.sleep(1)       
            print("The message being sent is " + message)               # Wait for prompt
            ser.write(message.encode())
            ser.write(chr(26).encode())                  # Exit message write and send
            time.sleep(1)
            sendStatus = ser.readlines()
            print("Send status is ")
            for line in sendStatus:
                print(line)
            if b'+CMGS' in sendStatus:
                print("Success: SMS sent!")
            else:
                print("Error: SMS not sent!")
       # except:
       #     print("Error: Something else failed!")
       #     trackerUtils.writeToFile(piLog, "Error: Something else failed!")
        finally:
            ser.__del__()