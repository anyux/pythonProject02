#!/usr/bin/env python
from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024

ADDR = (HOST, PORT)

tcpClient = socket.connect(ADDR)

while True:
    pass