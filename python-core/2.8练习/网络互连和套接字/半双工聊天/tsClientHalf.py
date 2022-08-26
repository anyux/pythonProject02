from socket import *
from time import time
import os

HOST='192.168.255.254'
port=21567
BUFSIZ=1024
ADDR=(HOST,port)
wait_message = "数据已发送等待接收服务端消息."
status = '客户端说话:--'

tcpClientSocket = socket(AF_INET,SOCK_STREAM)
tcpClientSocket.connect(ADDR)
first_data= "我是客户端,我先说:-_-"
tcpClientSocket.send(first_data.encode('utf-8'))
while True:
    print(wait_message)
    data = tcpClientSocket.recv(BUFSIZ).decode('utf-8')
    print(data)
    print(status)
    data = input(":")
    if data is not None:
        tcpClientSocket.send(data.encode('utf-8'))


