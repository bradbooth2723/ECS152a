from socket import *
import traceback
import sys
import time
import random


def pingMessage(message='', elapsedTime=0, serverAddress='173.230.149.18', packetNumber=0, sendRecFlag=0):
    if(sendRecFlag == 0):
        print("Message: {} recieved from {}.  Round Trip Time: {}".format(message, serverAddress, elapsedTime))
    elif(sendRecFlag == 1):
        print("Packet {}: Pinging {}".format(packetNumber, serverAddress))
    elif(sendRecFlag == 2):
        print("Packet {} Lost".format(packetNumber))



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
packetsReceived = 0
packetsDropped = 0
#breakpoint()
#Loops 10 times:  Sends out 10 ping requests from server
for i in range(10):
    timeout = False
    pingMessage(packetNumber=i+1, serverAddress=serverName, sendRecFlag=1)
    try:
        startTime = time.time()

        clientSocket.sendto(encodedMessage, (serverName, serverPort))
        clientSocket.settimeout(10)    #Will throw exception if clientSocket does not recieve a response in 10 seconds.
        message, serverAddress = clientSocket.recvfrom(2048)

        elapsedTime = time.time() - startTime
 
    except error:
        timeout = True
        if (lastTry == True):
            raise NameError("Timeout: Server is busy or something else is wrong.  Try again later.")  #Raises exception if wait time becomes longer than 10 minutes
        if (timeoutSeconds > 600):
            lastTry = True;
            timeoutSeconds = 600

        time.sleep(timeoutSeconds)  
        timeoutSeconds = timeoutSeconds * 2 ** timeoutCount + random.uniform(0,1)  #Determines wait time if packet is lost again
        timeoutCount = timeoutCount + 1

        #pingResponseList.append(-1)    #Appends element to list indicating dropped packet 
        pingMessage(packetNumber = i+1, sendRecFlag = 2)
        
        packetsDropped = packetsDropped + 1
    else:
        pingMessage(message = message, serverAddress = serverAddress, elapsedTime = elapsedTime)
        pingResponseList.append(elapsedTime) #Appends response time 
        packetsReceived = packetsReceived + 1

    if(timeout == False):
        timeoutSeconds = 10
        timeoutCount = 0

mx = max(pingResponseList)
mn = min(pingResponseList)
sm = sum(pingResponseList)

print("\nPing Statistics: Packets Sent: 10, Packets Received: {}, Packets Lost: {}".format(packetsReceived, packetsDropped))
print("Max RTT: {} seconds.".format(mx))
print("Min RTT: {} seconds.".format(mn))
print("Sum RTT: {} seconds.".format(sm))
print("Average RTT: {} seconds.".format(sm/10))

clientSocket.close()
