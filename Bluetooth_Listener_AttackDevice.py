import socket
import csv
import time
import string
import threading as thread

#socket settings defined
hostMACAddress = '34:cf:f6:d0:89:db' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 7
backlog = 1
size = 1024

#socket is created with defualt protocols and bound to mac address and port
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
#socket then listens for connection
s.listen(backlog)
#if connection is found the device is connected
client = s.accept()

#opens and writes heading values to CSV file
header = ['ID', 'Connected ID', 'My MAC', 'Connected MAC', 'Date Sent', 'Date Received', 'Payload Sent', 'Payload Received']
f = open('Results.csv','w', newline='')
writer = csv.writer(f)
writer.writerow(header)

#values passed in communication to other device
#future: use function to capture mac from device and not have manual entry
_ID = 'RasPi' #this devices ID
_CID = '' #id of connected device
_MYMAC = '34:cf:f6:d0:89:db' #mac address of this device
_RECEIVEMAC = '' #mac address of connected device
_DATE = ''  #date sent
_RDATE = ''  #date received
_PAYLOAD = '' #data sent
_RPAYLOAD = ''  #data received

#function called for writing data to CSV. Global varribles are used to pass data to function instead of inside function call
def CSVOutput():
    global _ID #this devices ID
    global _CID #id of connected device
    global _MYMAC #mac address of this device
    global _RECEIVEMAC #mac address of connected device
    global _DATE #date sent
    global _RDATE #date received
    global _PAYLOAD #data sent
    global _RPAYLOAD  #data received

    # writes the data to CSV
    writer.writerow([_ID,_CID,_MYMAC,_RECEIVEMAC,_DATE,_RDATE,_PAYLOAD,_RPAYLOAD])

#function once device is connected
def Connect():
    global _ID
    global _MYMAC
    global _DATE
    global _PAYLOAD 
    global hostMACAddress
    global port

      #creates message and sets recivedMessage to nother so data is not the same as previous message 
    receivedMessage = ''
    _PAYLOAD = (time.time() * 76)% 99999
    seconds = time.time()
    _DATE = str(time.ctime(seconds))
    message =  _ID+'|'+_MYMAC+'|'+_DATE+'|'+str(_PAYLOAD) +'|'+ '\r\n'

    #waits 1 second before running loop that sends an listens for incommming data from connected socket. sets buffer size to 1024 bits 
    #Check is done to ensure message is at least 10 character long so errors don't occur
    time.sleep(1)
    while len(receivedMessage) <10:
        receivedMessage = client.recv(1024)
        s.listen(backlog)
        client.send(message)
        print(receivedMessage)
    #message is printed to the screen for the user and the data is sent to be processed for storing.
    ProcessReceived(receivedMessage)

#takes the message recieved and passed in previous function and splits it to pass to the csv function for output to file
def ProcessReceived(Message):
    global _CID
    global _RECEIVEMAC
    global _RDATE
    global _RPAYLOAD
    if Message !='':
        decodedMessage = Message.decode('utf-8').strip('\r\n')
        message = decodedMessage.split("|")
        _CID = message[0]
        _RECEIVEMAC = message[1]
        _RDATE = message[2]
        _RPAYLOAD = message[3]
        CSVOutput()

#start function called to begin program. Continues to run untill program is closed
def Start():
    while True:
        Connect()

#call for start function to begin program.
Start()