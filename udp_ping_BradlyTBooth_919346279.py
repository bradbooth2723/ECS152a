from socket import *

serverName = '173.230.149.18'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = 'PING'

clientSocket.sendto(message.encode(), (serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print(modifiedMessage.decode())
print(serverAddress)
clientSocket.close()
