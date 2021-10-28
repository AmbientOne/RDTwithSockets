print("Hello World!")

#Socket client example in python

import socket	#for sockets
import sys

try:
    #creats an TCP(SOCK_STREAM) socket ipv4(AF_INET),
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message')
    sys.exit()
#create an AF_INET, STREAM socket (TCP)

print('Socket Created')

host = "www.google.com"
port = 80
#Https 443 for Https


try:
    remote_ip = socket.gethostbyname(host)

except socket.gaierror:
    #Gethostbyname (Could not resolve) error
    print("Hostname could not be resolved. Exiting")
    sys.exit()

print("Ip address of " + host + " is " + remote_ip)

#Connect to a remote sever
s.connect((remote_ip, port))

print('Socket Connected to ' + host + ' on ip ' + remote_ip)

message = "GET / HTTP/1.1\r\n\r\n"

try:
    #Set the whole string
    s.send(message.encode('utf-8'))
except socket.error:
    #Send failed
    print('Send failed')
    sys.exit()

print('Message send successfully')

#Receives socket reply
reply = s.recv(4096)

print(reply)


s.close()