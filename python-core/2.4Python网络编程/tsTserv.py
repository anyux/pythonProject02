#!/usr/bin/env python

from socket import *
from time import ctime
import os

HOST = '192.168.255.254'
HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpServerSocket = socket(AF_INET, SOCK_STREAM)
tcpServerSocket.bind(ADDR)
tcpServerSocket.listen(5)

while True:
    print('waiting for connection...')
    tcpClientSocket, addr = tcpServerSocket.accept()
    print('...connected from:', addr)

    while True:
        data = tcpClientSocket.recv(BUFSIZ)
        if not data:
            break
        # python2
        # tcpClientSocket.send('[%s] %s' %(ctime(), data))
        # python3
        tcpClientSocket.send(b'[%s] %s' % (bytes(ctime(), 'utf-8'), data))
        #windows上没有这个判断无法持续运行
        if os.name != 'nt':
            tcpClientSocket.close()

    tcpServerSocket.close()
