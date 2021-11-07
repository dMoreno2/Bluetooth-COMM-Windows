import serial
import time
import string
import threading as thread
import csv

#boolean to keep program running
messaging = True

#genric command so program doesn't start imdeiately when opened
print("Press Key To Start")
userInput = input()
print("-- Client DFevice --\n")

#creates comm of rfcomm port for linux or windows. port values need to be changed before running
try:
    #incomming comm port
    recievedSerial = serial.Serial(port="COM3", stopbits=serial.STOPBITS_ONE)
except:
    recievedSerial = serial.Serial("/dev/rfcomm1", 9600,stopbits=serial.STOPBITS_ONE)

#start to tell device infromation is coming
recievedSerial.write(str.encode('Start\r\n'))

#opens and writes heading values to CSV file
header = ['ID', 'Connected ID', 'My MAC', 'Connected MAC', 'Date Sent', 'Date Received', 'Payload Sent', 'Payload Received']
f = open('Results.csv','w', newline='')
writer = csv.writer(f)
writer.writerow(header)

#values passed in communication to other device
#future: use function to capture mac from device and not have manual entry

_ID = 'Client' #this devices ID
_CID = '' #id of connected device
_MYMAC = '00:E0:4C:6F:0A:03' #mac address of this device
_RECEIVEMAC = '' #mac address of connected device
_DATE = ''  #date sent
_RDATE = ''  #date received
_PAYLOAD = '' #data sent
_RPAYLOAD = ''  #data received

#function to make device exit when q is hit followed by enter
def OnKeyExit():
    global messaging
    global OnKeyExit
    while messaging == True:
        userInput = input()
        if userInput =='q':
            messaging = False
            print("Program Execution Ended")


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

#main function. Called to send data to and get data from, connected device.
def SendAndReceive():
    global _ID
    global _MYMAC
    global _DATE
    global _PAYLOAD 
    global clientOrBeacon
    global firstStart

    #creates message and sets recivedMessage to nother so data is not the same as previous message 
    receivedMessage = ''
    _PAYLOAD = (time.time() * 76)% 99999
    seconds = time.time()
    _DATE = str(time.ctime(seconds))
    message =  _ID+'|'+_MYMAC+'|'+_DATE+'|'+str(_PAYLOAD) +'|'+ '\r\n'

    #waits a second before starting the loop to recieve the beacons data
    time.sleep(1)
    while len(receivedMessage)<10:
        receivedMessage = recievedSerial.readline()

    #once data is recieved, data is encoded and sent back, message is printed to the scren for the user and the data is sent to be processed for storing.
    recievedSerial.write(str.encode(message))
    print(receivedMessage)
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

#starts0 exit command function on sperate thread to ensure it will work whilst main thread is functional
OnKeyExit = thread.Thread(target = OnKeyExit)
OnKeyExit.start()

#loop that loops the sendAndReceive function till boolean is set to false by exit command
while messaging == True:
    SendAndReceive()

#closes csv file to ensure correct writing
f.close()