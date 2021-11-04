# Reciever


import socket
import sys
import time
from check import ip_checksum
import random

HOST = ''
PORT = 9680
expecting = 0
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg:
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print("Created Socket and bind")

expecting = 0
delayed = 0
lastOneDone = 0
alreadyAcked = []
while 1:
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    dec = data.decode("utf-8")
    seq = ord(dec[0:1])
    # print("Sequence number: ")
    msg = data[2:12].decode("utf-8")
    checksum = data[12:].decode("utf-8")
    checksum2 = str(ip_checksum(msg))
    if not d:
        break
    if chr(seq) in alreadyAcked:
        continue
    print(seq, " ", str(msg), " , checksum= ", str(checksum), " from ", str(addr))

    if (delayed == 3):
        time.sleep(11)
    else:
        delay = random.random() * 2
        time.sleep(delay)

    delay = random.random() * 2
    time.sleep(delay)
    # print("Expecting: " + str(expecting))
    # print("Current seq: " + chr(seq))
    # print("Checksum 1:" + str(checksum))
    # print("Checksum 2:" + str(checksum2))
    if str(expecting) == chr(seq) and str(checksum) == str(checksum2):
        print("ACKing: " + chr(seq))
        s.sendto(b'ACK for ' + d[0], d[1])
        alreadyAcked.append(chr(seq))
        expecting+=1
        delayed += 1
    elif chr(seq) in alreadyAcked:
        print("Duplicate!")
        #print("ACKing: " + chr(seq))
        #s.sendto(b'ACK for ' + b'lastOneDone', d[1])
    else:
        print("Corrupted!")

    if(expecting == 10):
        break

s.close()

