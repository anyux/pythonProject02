#!/usr/bin/evn python

from socket import *

HOST = 'localhost'
PORT = 2222
BUFSIZ = 1024

myhost = input('请输入server端ip或域名:')
myport = input('请输入server端端口号:')
if  len(myhost):
    HOST = myhost

if  len(myport):
    PORT = int(myport)


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