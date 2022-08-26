from socket import *
from time import time,sleep
import os
from  select import select

HOST = "192.168.255.254"
port = 21567
# port = 1234
BUFSIZ = 1024
ADDR = (HOST, port)
start_info = "tcp client is starting....."
wait_info = "tcp client connected"
send_message = "send message..."
waiting_info = " waitting recv client info"

tcpClientSocket = socket(AF_INET, SOCK_STREAM)
tcpClientSocket.connect(ADDR)
outputs = [tcpClientSocket]


def controller():
    sock_in,sock_out,sock_err = select(inputs,[],[])
    for sock_item in sock_in:
        if sock_item is outputs:
            sock_handle = get_connected()
            inputs.append(sock_handle)
    get_data(sock_in)



def get_data():
    print(waiting_info)
    data = tcpClientSocket.recv(BUFSIZ).decode('utf-8')
    if data is not None:
        print(data)



def send_data():
    print(send_message)
    data = input(":")
    if data is not None:
        tcpClientSocket.send(data.encode('utf-8'))



while True:

    get_data()
    send_data()
