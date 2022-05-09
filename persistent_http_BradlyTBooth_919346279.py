#Persistant HTTP Request
#Bradly T Booth: 20220507
#ECS152a

from socket import *
from pathlib import Path
from bs4 import BeautifulSoup
import time
import os

serverName = '173.230.149.18'
serverPort = 23662
response = b""
listTime = []

startTime = time.time()
clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
clientSocket.settimeout(10)
clientSocket.connect((serverName, serverPort))
clientSocket.send(b"GET /ecs152a.html HTTP/1.1\r\nConnection:keep-alive\r\nX-Client-project: project-152A-part2\r\n\r\n")
first = True
length = -1
#breakpoint()
while len(response) != length:
    x = clientSocket.recv(4096)
    if first == True:
        x = x.decode()
        y = x.split('\r\n\r\n')
        temp = y[0]
        m = temp.find('length')
        length = int(temp[m+8:])
        response = y[1].encode()
        first = False
        continue
    if len(x)==0:
        listTime.append(time.time() - startTime)
        break
    response = response + x

response = response.decode()

cd = Path.cwd()
hfile = open(cd / Path('ecs152a.html'), 'w')
hfile.write(response)
hfile.close()

soup = BeautifulSoup(response, 'html.parser')
i = False
ATF = time.time()

for link in soup.find_all('img'):
    localFlag = False
    temp = link.get('src')
    pathItB = temp.find('//')
    if(pathItB != -1):
        pathItB = pathItB + 2
        pathItE = pathItB + temp[pathItB:].find('/')
        host = temp[pathItB:pathItE]
        path = temp[pathItE:]
    else:
        localFlag = True
        path = temp

    nameLoc = 0
    while(path[nameLoc:].find('/') != -1):
        nameLoc = nameLoc + path[nameLoc:].find('/') + 1
    imageName = path[nameLoc:]
    
    image = b""
    header = b""
    requestTime = time.time()
    if(localFlag == False):
        newSocket = socket(AF_INET, SOCK_STREAM)
        newSocket.connect((host, 80))
        getR = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path,host)
        newSocket.send(getR.encode())

        while True:
            x = newSocket.recv(4096)
            if len(x) == 0:
                if(i == False):
                    ATF = time.time() - startTime
                    i = True
                listTime.append(time.time() - requestTime)
                break
            image = image + x
    else:
        getR = "GET /{} HTTP/1.1\r\nHost:{}\r\nConnection:keep-alive\r\nX-Client-project:project-152A-part2\r\n\r\n".format(path,serverName)
        clientSocket.send(getR.encode())
        first = True
        length = -1
        while len(image) != length:
            x = clientSocket.recv(4096)
            if first == True:
                y = x.split(b'\r\n\r\n')
                header = y[0]
                m = header.find(b'length')
                length = int(header[m+8:])
                image = y[1]
                first = False
                continue
            image = image + x
        listTime.append(time.time() - requestTime)
             
    flag = image.find(b'200 OK')
    if(localFlag == True):
        flag = header.find(b'200 OK')
    if(flag != -1):
        y = image.find(b'\r\n\r\n') + 4
        image = image[y:]
        os.makedirs(cd / Path('images'), exist_ok = True)
        hfile = open(cd / Path('images') / Path(imageName), 'wb')
        hfile.write(image)
        hfile.close()

PLT = time.time() - startTime
    
a = "********************************************************"
print(a)
print("HTTP Client Version: Persistent HTTP")
print("Total Page Load Time: {} seconds".format(PLT))
print("Average Request Delay: {} seconds".format(sum(listTime)/len(listTime)))
print("Above the Fold Load Time: {} seconds".format(ATF))
print("Request per Second:       {} seconds".format(len(listTime)/sum(listTime)))
print(a)
