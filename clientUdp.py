'''import socket

msgFromClient = "Hello UDP Server"

bytesToSend = str.encode(msgFromClient)

serverAddressPort = ("127.0.0.1", 9680)

bufferSize = 1024

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
'''

from socket import timeout
import socket
import sys
import time
import threading

from check import ip_checksum
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host='localhost'
port = 9680

s.settimeout(1)

seq = 0


for i in range(10):
    msg= 'Message #'+str(i)
    checksum = ip_checksum(msg)
    error = random.random()
    #if error>0.75:
    # checksum=checksum+str(1)
    s.sendto(str(seq)+' '+msg + '' + checksum ,(host,port))
    print('Sent: '+ str(seq),' '+ msg + ' checksum = ' + checksum)
    try:
        d = s.recvfrom(1024)
        print(d[0])
        decoded = d[0].decode('utf-8')
        if decoded.startswith('ACK'):
            seq= 1 - seq
    except timeout:
        print('Timeout')