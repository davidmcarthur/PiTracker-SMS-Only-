import serial
import socket
from datetime import datetime
import pyrebase

global ser

def initDB():
    config = {
        "apiKey": "AIzaSyC9xmtp91C8RFvvLaBIE5w7gWUWgmWlkvM",
        "authDomain": "pitracker-1521337480618.firebaseapp.com/",
        "databaseURL": "https://pitracker-1521337480618.firebaseio.com/",
        "storageBucket": "pitracker-1521337480618.appspot.com",
        "serviceAccount": "PiTracker-fc1fd634be36.json"
    }
    firebase = pyrebase.initialize_app(config)
    return firebase
    
def readDB():
    return 0
    
def writeDB(db, data):
    db.child("routeData").set(data)
    
    
def openSerialPort():                                                   # Opens the Pi's serial port to begin communication
    ser = serial.Serial(
        "/dev/serial0",
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout = 1,
    )        
    return ser

def getIP():                                                           # Gets the Pi's current IP Address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    currentIP = s.getsockname()[0]
    s.close()
    return currentIP

def getUTC():                                                          # Gets the current UTC time for naming logs 
    currentUTC = datetime.utcnow()
    strUTC = str(currentUTC)
    reps = {' ':'', '-':'',':':''}
    strUTC = replace_all(strUTC, reps)
    return strUTC

def replace_all(text, dic):                                           # Performs replacement of space, "-", and ":" characters for log names
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

# Initialize new File    
def initFile(fileName):
    # file-output.py
    f = open(fileName,'w')
    f.write('Testing log')
    f.close()

# Append existing file data    
def writeToFile(fileName, message):
    # file-append.py
    f = open(fileName,'a')
    f.write('\n' + message)
    f.close()
