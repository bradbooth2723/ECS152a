from socket import *
import requests

serverName = '173.230.149.18'
serverPort = 23662

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
clientSocket.send(b"GET /ecs152a.html HTTP/1.1\r\nConnection:close\r\nX-Client-project:project-151a-part2\r\n\r\n")
response = clientSocket.recv(4096)
print(response.decode())
clientSocket.close()
