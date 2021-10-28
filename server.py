#Reciever

import socket
import sys
#from _thread import *
#import threading

listOfClients = []
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 9680  # Arbitrary non-privileged port
bufferSize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

print("Socket now listening")

def sendAllMessage(message):
    for client in listOfClients:
        client.send(message.encode("utf-8"))
    return 0

def clientthread(conn):
    #Sending message to connected client
    welcomeMessage =  "Welcome to the server Type something and hit enter\n"

    conn.send(welcomeMessage.encode("utf-8"))

    #infinite Loop

    while True:
        #Data from client
        data = conn.recv(1024)
        tmpData = data.decode("utf-8")
        reply = "OK..." + tmpData
        if not data:
            break
        if tmpData[0:2] == "!q":
            for client in listOfClients:
                if client == conn:
                    listOfClients.remove(client)
                    break
            break
        if tmpData[0:8] == "!sendall":
            sendAllMessage(tmpData[9:])
        else:
            conn.send(reply.encode("utf-8"))
    

bytesToSend = str.encode("Hello from the server.")
while 1:
    # Accepting a connection - blocking call
    bytesAddressPair = s.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client

    s.sendto(bytesToSend, address)
    '''conn, addr = s.accept()
    print("Connected with " + addr[0] + ':' + str(addr[1]))
    listOfClients.append(conn)
    #start new thread takes 1st arg as function name to be run, second is the args to the func
    threading.Thread(target=clientthread, args=(conn,)).start()
    '''

#s.close()

