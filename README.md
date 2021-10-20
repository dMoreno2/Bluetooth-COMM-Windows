# Bluetooth-COMM-Windows
Python script for sending and receiving on windows for bluetooth


First, this script is currently set to run in Windows but later revisions will allow for it to function in both Unix based and Windows based system.

To start using this follow these steps to setup it up on windows.

1. Navigate to control pannel and open Bluetooth settings. Then go to the COM Ports tab and ADD a new incoming COM port.
2. Next you will want to install the software dependencise. You will need python 3, latest will do, installed.
3. Then, following this link to download <a href="https://pypi.org/project/pyserial/#files" target="_blank">pyserial</a> and unzip the file with winrar and extract to downloads.
4. Then open Command protmt and run the following commands: 
      cd C:\Users\MYUSERNAME\Downloads\pyserial-3.5
      py -3 "setup.py"
       
5. Now, download this repo and extract it where you would like.
6. Open Bluetooth Transmitter.py and change the COM port to the COMM port you have setup.
7. Then, using Command Promt, change into the directory where the extracted files are.
8. In Command Promt you enter the following to start the program: py -3 "Bluetooth Transmitter.py"
9. Using another device setup using these steps, connect ot the device via Bluetooth.
10. Results can be found in the accompanied CSV file.


This program was made to test the security of Bluetooth transmissions and how succeptible they are to interception.
