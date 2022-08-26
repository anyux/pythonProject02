from socket import *
from time import time
import os

HOST = '192.168.255.254'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
wait_message = "数据已发送等待接收客户端消息."
status = '服务端说话:--'

tcpServerSocket = socket(AF_INET, SOCK_STREAM)
tcpServerSocket.bind(ADDR)
tcpServerSocket.listen(10)

print('waiting for connection...')

tcpClientSocket, addr = tcpServerSocket.accept()
print('...connected from:', addr)

while True:
    data = tcpClientSocket.recv(BUFSIZ).decode('utf-8')
    print(data)
    print(status)
    data = input(":")
    tcpClientSocket.send(data.encode('utf-8'))
    print(wait_message)
