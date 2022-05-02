from socket import *
import time
from datetime import timedelta
import traceback
import sys
import time
import random

#TODO: Print ping response message after each packet received.  Will probably implement a function to do that (We saw how well that went last time we did that)
#TODO: Print ping statistics at very end of program

serverName = '173.230.149.18' #Test Server
#serverName = '10.255.255.1'  #Timeout Address
serverPort = 12000   #Other Ports: 5005, 5000=6, 5007
timeout = False #flag is settimeout exception is raised

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = 'PING'
encodedMessage = message.encode()  #Encoded message
elapsedTime = time.time()
startTime = time.time()
timeoutSeconds = 10     #Amount of time program will wait before sending another response to server if a timeout has occured
timeoutCount = 0        #Number of times no response has been recieved from server in a row
lastTry = False         #If timeout becomes longer than 10 minutes, will try one more request before raising an exception
pingResponseList = []   #List of responses from server

#Loops 10 times:  Sends out 10 ping requests from server
for i in range(10):
    timeout = False
    try:
        startTime = time.time()
        clientSocket.sendto(encodedMessage, (serverName, serverPort))
        clientSocket.settimeout(10)    #Will throw exception if clientSocket does not recieve a response in 10 seconds.
        message, serverAddress = clientSocket.recvfrom(2048)
        elapsedTime = time.time() - startTime
        pingResponseList.append(elapsedTime) #Appends response time 
         
    except Exception:
        timeout = True
        if (lastTry == True):
            raise NameError("Timeout: Server is busy or something else is wrong.  Try again later.")  #Raises exception if wait time becomes longer than 10 minutes
        if (timeoutSeconds > 600):
            lastTry = True;
            timeoutSeconds = 600
        time.sleep(timeoutSeconds)  
        timeoutSeconds = timeoutSeconds * 2 ** timeoutCount + random.uniform(0,1)  #Determines wait time if packet is lost again
        timeoutCount = timeoutCount + 1
        pingResponseList.append(-1)    #Appends element to list indicating dropped packet 
    if(timeout == False):
        timeoutSeconds = 10
        timeoutCount = 0

packetsReceived = 0
packetsDropped = 0
for i in pingResponseList:
    if(i[0] == -1):
        packetsDropped += 1
    else:
        packetsRecieved += 1

print(pingResponseList)
clientSocket.close()

#Ok, so the expnential timeout function is called if you do not recieve a response.  We wait
#because we know the server exists, but it might not recieving a response because the server is
#very busy.  Ok, so I will probably write a function to handle the backoff sleep because my 
#code is starting to get a little messy.  This notion of backoff function confuses and infuriates me!!
