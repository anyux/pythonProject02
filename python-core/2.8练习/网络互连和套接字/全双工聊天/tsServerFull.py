from socket import *
from select import select
from time import time
import os

HOST="192.168.255.254"
port=21567
BUFSIZ=1024
ADDR=(HOST,port)
start_info = "tcp server is starting....."
wait_info = "tcp server connection"
send_message = "send message..."
waiting_info = " waitting recv client info"

tcpSocketServer = socket(AF_INET,SOCK_STREAM)
tcpSocketServer.bind(ADDR)
tcpSocketServer.listen(10)
inputs = [tcpSocketServer]
print(start_info)


def controller():
    sock_in,sock_out,sock_err = select(inputs,[],[])
    for sock_item in sock_in:
        if sock_item is inputs:
            sock_handle = get_connected()
            inputs.append(sock_handle)
    get_data(sock_in)

def get_connected():
    tcpClientSocket, add_info = tcpSocketServer.accept()
    print(wait_info, add_info, time())
    return tcpClientSocket

def get_data(tcpClientSocket):
    print(waiting_info)
    data = tcpClientSocket.recv(BUFSIZ).decode('utf-8')
    if data is not None:
        print(data)

def send_data(tcpClientSocket):
    print(send_message)
    data = input(":")
    if data is not None:
        tcpClientSocket.send(data.encode('utf-8'))


while True:

    # send_data()
    # get_data()
    controller()




