import socket
import time

def initializePackets():
    packets = []
    cap = 2408280
    seq = 1
    text = ""
    initial = 0
    limiter = 1000

    # open file to read into a string variable for easy parsing
    with open("message.txt") as file:
        for line in file:
            text = text + line

    # parse 1000 bytes of the message file and add sequence header
    # store the parsed item into a packets array to return
    while initial < cap:
        encoded = text[initial:limiter].encode()
        initial = limiter
        limiter = limiter + 1000
        packet = (str(seq) + "|").encode() + encoded
        packets.append(packet)
        seq = seq + 1

    print("Number of packets:", len(packets))
    return packets

def DynamicWindow(port):
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    initialTimeout = 5
    packets = initializePackets()
    windowSize = 1
    slowStart = True
    acknum = 0  #Number of last ack received
    windowBase = 1 #Lowest packet number in window
    windowCeil = 1 #Highest packet number in window
    lastSent = 1
    offset = 0
    doubleAck = 0
    congControl = 0

    cs.sendto(packets[0], ("127.0.0.1", port))   
    # send first 1st packet
    #breakpoint()
    
    cs.settimeout(initialTimeout)
    adjustTimeout = initialTimeout
    while(True):
        try:
            ack, add = cs.recvfrom(2048) #try to recieve acknowledgement
            
        except socket.timeout:
            windowSize = 1    
            adjustTimeout = adjustTimeout * 2
            cs.settimeout(adjustTimeout)
            cs.sendto(packets[acknum - 1], ("127.0.0.1", port))
        else:
            acknum = int(ack.decode())
            
            if acknum < windowBase: 
                doubleAck += 1
                #if recieved check if we get a double acknowlegement. If so, resend the packet we are expecting
                if(doubleAck == 2):  #We say this is 2 because the first double ack could just be out of order
                    windowSize = 1
                    cs.sendto(packets[acknum + 1], ("127.0.0.1", port))
                    doubleAck = 0
                continue
            
            offset = acknum - windowBase + 1

            if (offset <= 0):
                cs.settimeout(initialTimeout)

            if acknum == len(packets):
                print(acknum)
                break

            #if our ackWin is up to the last package in the package list, don't send any new packets
            if windowCeil == len(packets):
                print(acknum)
                cs.settimeout(initialTimeout)
                continue

            if(slowStart == True):
                windowSize += 1
                if(windowSize >= 16):
                    slowStart = False
                    congControl = windowCeil
            else:
                if(acknum >= congControl):
                    windowSize += 1
                    congControl = acknum + windowSize 
            

            windowBase  = acknum + 1
            windowCeil = windowBase + windowSize - 1

            for send in range(lastSent, windowCeil):
                cs.sendto(packets[send], ("127.0.0.1", port))
                print("Sending packet: {}".format(send + 1))
                lastSent = send + 1
            print("acknum: ", acknum)
            print("windowSize: ", windowSize)


if __name__ == "__main__":
    Port = int(input("Enter Port Number to run: "))
    DynamicWindow(Port)