#!/usr/bin/evn python

from socket import *

HOST = 'localhost'
PORT = getservbyname('Daytime')
BUFSIZ = 1024

ADDR = (HOST, PORT)



print('...请求服务端信息...',ADDR)
udpClientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    data = input('> ')
    if not data:
        break
    udpClientSocket.sendto(data.encode('utf-8'),ADDR)
    data,ADDR = udpClientSocket.recvfrom(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))

udpClientSocket.close()