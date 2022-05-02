from socket import *
import time
from datetime import timedelta
import traceback
import sys
import time
import random

serverName = '173.230.149.18' #Test Server
#serverName = '10.255.255.1'  #Timeout Address
serverPort = 12000
timeout = False #flag is settimeout exception is raised
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = 'PING'
elapsedTime = time.time()
startTime = time.time()
timeoutSeconds = 10
timeoutCount = 0
lastTry = False
pingResponseList = []
for i in range(10):
    timeout = False
    try:
        startTime = time.time()
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        clientSocket.settimeout(10)
        message, serverAddress = clientSocket.recvfrom(2048)
        elapsedTime = time.time() - startTime
        pingResponseList.append([elapsedTime, message]) 

    except Exception:
        timeout = True
        if (lastTry == True):
            raise NameError("Timeout: Server is busy or something else is wrong.  Try again later.")
        if (timeoutSeconds > 600):
            lastTry = True;
            timeoutSeconds = 600
        time.sleep(timeoutSeconds)
        timeoutSeconds = timeoutSeconds * 2 ** timeoutCount + random.uniform(0,1)
        timeoutCount = timeoutCount + 1
        pingResponseList.append([-1, 'TIMEOUT'])
    if(timeout == False):
        timeoutSeconds = 10

print(pingResponseList)
clientSocket.close()

#Ok, so the expnential timeout function is called if you do not recieve a response.  We wait
#because we know the server exists, but it might not recieving a response because the server is
#very busy.  Ok, so I will probably write a function to handle the backoff sleep because my 
#code is starting to get a little messy.  
