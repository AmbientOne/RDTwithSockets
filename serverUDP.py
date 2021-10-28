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

while 1:
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    seq = data[0]
    msg = data[2:12]
    checksum = data[12:]
    print(str(msg.decode("utf-8")))
    checksum2 = ip_checksum(msg.decode("utf-8"))
    val = str(seq) + " " + str(msg) + " , checksum= " + str(checksum) + " from " + str(addr)
    print(val)
    if not d:
        break
    delay = random.random() * 2
    time.sleep(delay)
    print(str(expecting))
    print(str(seq))
    if str(expecting) == str(seq) and str(checksum) == str(checksum2):
        s.sendto(b'ACK for ' + d[0], d[1])
        expecting = 1 - expecting
    else:
        print("Didn't work idiot!")
s.close()

