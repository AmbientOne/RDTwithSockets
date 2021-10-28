# Sender


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

from checkForClient import ip_checksum
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
while i < 10:
    msg = 'Message #'+str(i)
    checksum = ip_checksum(msg)
    error = random.random()
    #if error > 0.75:
     #checksum = checksum + str(1)
    val = str(seq) + " " + msg + " " + checksum
    s.sendto(val.encode("utf-8"), (host, port))  # sndpkt
    s.settimeout(10)

    print('Sent: ' + str(seq), ' ' + msg + ' checksum = ' + checksum)

    try:
        d = s.recvfrom(1024)
        print(d[0])
        decoded = d[0].decode('utf-8')
        if decoded.startswith('ACK'):
            seq = 1 - seq
            print("Sucessfuly ACK'ed!")
            i+=1
            continue
    except timeout:
        print('Timeout, resending')


