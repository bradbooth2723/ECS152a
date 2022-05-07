#from socket import socket, AF_INET, SOCK_DGRAM
from socket import *
import random
import time
import traceback
import sys

serverName = '173.230.149.18'
#serverName = '10.255.255.1'
serverPort = 5005 #12000 5005 5006 5007

clientSocket = socket(AF_INET, SOCK_DGRAM)

startTime = time.time()
stopTime = time.time()
RTT = []

timeout = False
lastTry = False
timeoutCount = 0
timeoutSeconds = 10

clientSocket.sendto('ping'.encode(), (serverName, serverPort))
messageLength = 0
fullMessage = ''.encode()
percentage = 0.0

while messageLength != 1300000:
    timeout = False

    try:
        clientSocket.settimeout(2)
        message, serverAddress = clientSocket.recvfrom(4096)
    except error:
        print("Timeout...will try again in {} seconds".format(timeoutSeconds))
        if (lastTry == True):
            raise NameError("Timeout: Server is busy or something else is wrong. Try again later.")
        if (timeoutSeconds > 600):
            lastTry = True;
            timeoutSeconds = 600
        time.sleep(timeoutSeconds)
        timeoutSeconds = timeoutSeconds * 2 ** timeoutCount + random.uniform(0,1)
        timeoutCount = timeoutCount + 1
    else:
        stopTime = time.time()
        RTT.append(stopTime - startTime)

        fullMessage = fullMessage + message
        messageLength = messageLength + len(message)
        percentage = percentage + len(message)/1300000
        print("Received %: {}".format(round(percentage * 100)))

        timeoutSeconds = 10
        timeoutCount = 0

print("Time elapsed: {} seconds".format((RTT[-1])))
print("File Size: {} bytes".format(messageLength))
print("Throughput: {} bytes per second".format(messageLength/RTT[-1]))
clientSocket.close()
