#Non Persistant HTTP Request
#Bradly T Booth: 20220507
#ECS152a

from socket import *
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import time
import os

serverName = '173.230.149.18'
serverPort = 23662
response = b""
listTime = [] #List of all request delays

startTime = time.time()
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
clientSocket.send(b"GET /ecs152a.html HTTP/1.1\r\nConnection: close\r\nX-Client-project: project-152A-part2\r\n\r\n")
while True:
    x = clientSocket.recv(4096)
    if len(x)== 0: #If len is 0 then buffer is empty...Hopefully this doesn't lead to an issue where file is not downloaded if there is large delay on network
        listTime.append(time.time() - startTime)
        break
    response = response + x

clientSocket.close()

response = response.decode()

x = response.find('\r\n\r\n') + 4 #Index of last position of the header
response = response[x:] #removing header
cd = Path.cwd() #path of current working directory
hfile = open(cd / Path('ecs152a.html'), 'w') 
hfile.write(response)  
hfile.close()

soup = BeautifulSoup(response, 'html.parser')
i = False #Used for above the fold time calculation
ATF = time.time() #initializing variable

for link in soup.find_all('img'): #iterating through all elements with image tag
    localFlag = False #used to determine if image is external or local 
    temp = link.get('src')
    pathItB = temp.find('//')
    if(pathItB != -1): #external request URL should begin with '//' or 'http://'.  Either way, both have '//' whereas local request does not
        pathItB = pathItB + 2
        pathItE = pathItB + temp[pathItB:].find('/') #parsing URL for hostname and path of image
        host = temp[pathItB:pathItE]
        path = temp[pathItE:]
    else:
        localFlag = True 
        path = temp #local file equals full string
    
    nameLoc = 0
    #Getting index of filename
    while(path[nameLoc:].find('/') != -1):
        nameLoc = nameLoc + path[nameLoc:].find('/') + 1
    imageName = path[nameLoc:]

    requestTime = time.time()#starting time for HTTP request
    #image request...different depending on whether local or external request
    if(localFlag == False):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((host, 80))
        getR = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path,host)
        clientSocket.send(getR.encode())
    else:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        getR = "GET /{} HTTP/1.1\r\nHost:{}\r\n\Connection:close\r\nX-Client-project:project-152A-part2\r\n\r\n".format(path,serverName)
        clientSocket.send(getR.encode())
    
    image = b""
    while True:
        x = clientSocket.recv(4096)
        if len(x) == 0:
            if(i == False):
                ATF = time.time() - startTime
                i = True
            listTime.append(time.time() - requestTime)
            break

        image = image + x

    flag = image.find(b'200 OK') #verifying that request for file was OK before writing
    if(flag != -1):
        y = image.find(b'\r\n\r\n') + 4
        image = image[y:]
        os.makedirs(cd / Path('images'), exist_ok = True)
        hfile = open(cd / Path('images') / Path(imageName), 'wb')
        hfile.write(image)
        hfile.close()
PLT = time.time() - startTime
#Printing program report
a = "********************************************************"
print(a)
print("HTTP Client Version: Non Persistent HTTP")
print("Total Page Load Time:     {} seconds".format(PLT))
print("Average Request Delay:    {} seconds".format(sum(listTime)/len(listTime)))
print("Above the Fold Load Time: {} seconds".format(ATF))
print("Requests per Second:      {}".format(len(listTime)/sum(listTime)))
print(a)
