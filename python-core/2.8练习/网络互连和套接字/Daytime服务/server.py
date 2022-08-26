#!/usr/bin/env python
from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024

ADDR = (HOST, PORT)
tcpServer = socket(AF_INET,SOCK_STREAM)
tcpServer.bind(ADDR)

