import serial
import time
import string
import threading as thread
import csv

messaging = True

clientOrBeacon = ''

print("WELCOME LISTENER")

try:
    recievedSerial = serial.Serial(port="/dev/rfcomm0", 9600,stopbits=serial.STOPBITS_ONE)
    print('Connected')
except:
    print('Error Occured')
    exit()

header = ['ID', 'Connected ID', 'My MAC', 'Connected MAC', 'Date Sent', 'Date Received', 'Payload Sent', 'Payload Received']
f = open('Results.CSV','w', newline='')
writer = csv.writer(f)
writer.writerow(header)


_ID = 'RasPI' #this devices ID
_CID = '' #id of connected device
_MYMAC = 'XX:XX:XX:XX:XX:XX:XX' #mac address of this device
_RECEIVEMAC = '' #mac address of connected device
_DATE = ''  #date sent
_RDATE = ''  #date received
_PAYLOAD = '' #data sent
_RPAYLOAD = ''  #data received

running = True

def OnKeyExit():
    global messaging
    global OnKeyExit
    while messaging == True:
        userInput = input()
        if userInput =='q':
            print("Program Execution Ended")

def CSVOutput():
    global _ID #this devices ID
    global _CID #id of connected device
    global _MYMAC #mac address of this device
    global _RECEIVEMAC #mac address of connected device
    global _DATE #date sent
    global _RDATE #date received
    global _PAYLOAD #data sent
    global _RPAYLOAD  #data received
    
    writer.writerow([_ID,_CID,_MYMAC,_RECEIVEMAC,_DATE,_RDATE,_PAYLOAD,_RPAYLOAD])

def Receive():
    global _ID
    global _MYMAC
    global _DATE
    global _PAYLOAD 
    global clientOrBeacon

    receivedMessage = ''
    while len(receivedMessage)<10:
        receivedMessage = recievedSerial.readline()
    
    print(receivedMessage)
    #time.sleep(5)
    ProcessReceived(receivedMessage)

def ProcessReceived(Message):
    global _CID
    global _RECEIVEMAC
    global _RDATE
    global _RPAYLOAD
    if Message !='':
        decodedMessage = Message.decode('utf-8').strip('\r\n')
        message = decodedMessage.strip().split('|')
        _CID = message[0]
        _RECEIVEMAC = message[1]
        _RDATE = message[2]
        _RPAYLOAD = message[3]
        CSVOutput()

OnKeyExit = thread.Thread(target = OnKeyExit)
OnKeyExit.start()

while messaging == True:
    Receive()

f.close()