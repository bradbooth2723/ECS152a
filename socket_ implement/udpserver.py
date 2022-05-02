from socket import *

serverPort = 12000

#AF_INET indicates that the underlying network is using IPv4. (Do not worry about
# this now—we will discuss IPv4 in Chapter 4.) The second parameter indicates that the socket is of type
# SOCK_DGRAM , which means it is a UDP socket (rather than a TCP socket).
serverSocket = socket(AF_INET, SOCK_DGRAM)
# ip address ( 127.0.0.1) and port number

# The above line binds (that is, assigns) the port number 12000 to the server’s socket.
serverSocket.bind(('', serverPort))

print("The server is ready to receive")
while True:
    message, clientAddress = serverSocket.recvfrom(2048 )
    print("server received:",str(message))


    # 2048 is buffer size number of bite you want to receive
    modifiedMessage = message.decode().upper()
    print("server return",str(modifiedMessage))
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    # attaches the client’s address (IP address and port number) to the capitalized message
# (after converting the string to bytes), and sends the resulting packet into the server’s socket.
serverSocket.close()
