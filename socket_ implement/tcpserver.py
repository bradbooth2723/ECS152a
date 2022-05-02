from socket import *
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# establishing our welcoming socket
#now wait and listen for client knock
serverSocket.listen(1)
#ask server to listen for the request from client
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    print("connection established")
    sentence = connectionSocket.recv(8).decode()
    print("server received: ",sentence)
    capitalizedSentence = sentence.upper()
    print("server output: ", capitalizedSentence)
    connectionSocket.send(capitalizedSentence.encode())
connectionSocket.close()
