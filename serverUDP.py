import socket
import sys
import time
from check import ip_checksum
import random

HOST = ''
PORT = 9680
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))
print("Created Socket and bind")
expecting=0


while 1:
    d = s.recvfrom(1024)
    data=d[0]
    addr=d[1]
    seq=data[0]
    msg=data[2:12]
    checksum=data[12:]
    print(str(data))
    checksum2=ip_checksum(msg)
    print('' + seq + '-' + msg + ' ,checksum= ' + checksum + ' from ' + str(addr))
    if not d:
        break
    delay=random.random()*2
    time.sleep(delay)
    if str(expecting)==str(seq) and str(checksum)==str(checksum2):
        s.sendto(b'ACK for '+ d[0], d[1])
        expecting= 1 - expecting
s.close()