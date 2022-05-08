from socket import *
from pathlib import Path
import requests

serverName = '173.230.149.18'
serverPort = 23662
response = b""

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
clientSocket.send(b"GET /ecs152a.html HTTP/1.1\r\nConnection: close\r\nX-Client-project: project-152A-part2\r\n\r\n")
while True:
    x = clientSocket.recv(4096)
    if len(x)== 0:
        break
    response = response + x
    #TODO: Save response to HTML file
clientSocket.close()

response = response.decode()

x = response.find('\r\n\r\n') + 4
response = response[x:]
cd = Path.cwd()
hfile = open(cd / Path('ecs152a.html'), 'w')
hfile.write(response)
hfile.close()
itBegin = 0
itEnd = 0
count = 0
while( response[itBegin:].find("<img src=") != -1):
    if (count == 1):
        breakpoint()
    itBegin = response[itBegin:].find("<img src=")
    itBegin = itBegin + response[itBegin:].find('"') + 1
    itEnd = itBegin + response[itBegin:].find('"')
    temp = response[itBegin:itEnd]
    pathItB = temp.find('//') + 2
    pathItE = pathItB + temp[pathItB:].find('/')

    host = temp[pathItB:pathItE]
    path = temp[pathItE:]

    nameLoc = 0
    while(path[nameLoc:].find('/') != -1):
        nameLoc = nameLoc + path[nameLoc:].find('/') + 1
    
    imageName = path[nameLoc:]

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, 80))

    getR = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host)
    clientSocket.send(getR.encode())
    image = b""
    while True:
        x = clientSocket.recv(4096)
        if len(x) == 0:
            break
        image = image + x

    flag = image.find(b'200 OK')
    if(flag != -1):
        y = image.find(b'\r\n\r\n') + 4
        image = image[y:]
        hfile = open(cd / Path(imageName),'wb')
        hfile.write(image)
        hfile.close()
    count = count + 1
