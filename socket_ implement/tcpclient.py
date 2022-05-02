from socket import *
serverName = ''
serverPort = 12001

# IPV4, type indicates TCP
clientSocket = socket(AF_INET, SOCK_STREAM)

# this line is different from UDP
# that before the client can send data to the server
#connection must first be established
#this establish three way handshake
clientSocket.connect((serverName, serverPort))
sentence = input("Input lowercase sentence:")



clientSocket.send(sentence.encode())
#the client program simply drops the bytes in the string sentence
# into the TCP connection. The client then waits to receive bytes from the server
while True:
    modifiedSentence = clientSocket.recv(1024)
    print("From Server: ", modifiedSentence.decode())

# clientSocket.close()
