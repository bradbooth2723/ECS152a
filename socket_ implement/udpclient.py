#wireshark interface: loopback: Io0

from socket import *
serverName = '' #can be ip or host name
serverPort = 12000

# create the client socket: address family, ipv4 ; udp socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(),(serverName, serverPort))
#create a packet and attach the destination address to the packet,

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print("client received: ",modifiedMessage.decode())
clientSocket.close()
