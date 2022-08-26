#!/usr/bin/env python
from socket import *
HOST = '192.168.255.254'
HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024

ADDR = (HOST, PORT)

tcpClientSocket = socket(AF_INET,SOCK_STREAM)
tcpClientSocket.connect(ADDR)
while True:
    data = input('> ')
    if not data:
        break
    tcpClientSocket.send(data.encode('utf-8'))
    data = tcpClientSocket.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))
tcpClientSocket.close()