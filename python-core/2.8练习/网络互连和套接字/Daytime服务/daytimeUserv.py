#!/usr/bin/env python
from socket import *
from time import ctime

HOST = 'localhost'
PORT = getservbyname('Daytime')
BUFSIZ = 1024
ADDR = (HOST, PORT)

udpServerSocket = socket(AF_INET, SOCK_DGRAM)
udpServerSocket.bind(ADDR)

while True:
    print('waiting for message...')
    data, addr = udpServerSocket.recvfrom(BUFSIZ)
    udpServerSocket.sendto(b'%s' % (bytes(ctime(),'utf-8')), addr)
    print('...received from and returned to:', addr)

udpServerSocket.close()
