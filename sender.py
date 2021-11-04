
from socket import timeout
import socket
import sys
import time
from check import ip_checksum
import random

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

host = 'localhost'
port = 9680

seq = 0

# function that sendspkt
i = 0


#Create a sliding window for the data where start = 0 and end = 4
#When oldest packet is acked increase window size by 1 and wait for acking next packet
#Have timeout for oldest in-flight pkt (aka whatever is set to n)

#We don't want to resend packages already out, we want to send the one right after

inTransit = 0
#timeoutFlag active
flag = 0
firstTime = 0
#hold data
notAcked = {}
timeoutInRow = 0

packetsInTransit = []
beginningVal = 0
maxSize = 4
flagReachedMaxSize = 0
finished = 0
#previous beginningVal

def addPackages():
    for i in range(10):
        msg = 'Message #' + str(i)
        notAcked[i] = msg

def sendAllPackets():
    global inTransit, flag
    global notAcked
    for i in range(beginningVal, maxSize):
        checksum = ip_checksum(notAcked[i])
        # error = random.random()
        # if error > 0.75:
        # checksum = str(checksum) + str(1)
        val = str(i) + " " + notAcked[i] + "" + str(checksum)
        inTransit+=1
        packetsInTransit.append(str(i))
        s.sendto(val.encode("utf-8"), (host, port))  # sndpkt
        print("Sequence number: " + str(i) + " Message: " + notAcked[i] + " Checksum: " + str(checksum))
        print("--------------------------------------------------------------")
        if(flag == 0):
            s.settimeout(10)
            flag = 1
def sendSinglePacket():
    global inTransit
    if maxSize < 10 and flagReachedMaxSize != 1:
        checksum = ip_checksum(notAcked[maxSize])
        val = str(maxSize) + " " + notAcked[maxSize] + "" + str(checksum)
        inTransit += 1
        packetsInTransit.append(str(maxSize))
        s.sendto(val.encode("utf-8"), (host, port))  # sndpkt
        print("Sequence number: " + str(maxSize) + " Message: " + notAcked[maxSize] + " Checksum: " + str(checksum))
        print("--------------------------------------------------------------")


while finished != 1:
    if(firstTime == 0):
        addPackages()
        firstTime = 1


    if inTransit == 0:
        sendAllPackets()
    elif inTransit < 4:
        sendSinglePacket()

    try:
        d = s.recvfrom(1024)
        print("--------------------------------------------------------------")
        print(d[0])
        decoded = d[0].decode('utf-8')
        if decoded.startswith('ACK') and str(decoded[8]) == str(seq):
            seq += 1
            print("Sucessfuly ACK'ed!")
            print("--------------------------------------------------------------")

            i += 1
            flag = 0
            beginningVal+=1
            inTransit-=1
            timeoutInRow = 0
            if str(seq) == maxSize:
                finished = 1
            if firstTime == 1:
                maxSize-=1
                firstTime = 2
            if(maxSize < len(notAcked)):
                maxSize+=1
            else:
                flagReachedMaxSize = 1

            continue
        elif str(decoded[8]) != seq:
            continue
    except timeout:
        print('Timeout, resending all packets in window')
        inTransit = 0
        maxSize = beginningVal
        if (maxSize + 4 > len(notAcked)):
            maxSize = len(notAcked)
        else:
            maxSize = maxSize + 4
        firstTime = 1
    if timeoutInRow == 3:
        break




