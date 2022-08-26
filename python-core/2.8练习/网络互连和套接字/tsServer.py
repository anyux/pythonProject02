#!/usr/bin/env python

from socket import *
from time import ctime
import os

HOST = '192.168.255.254'
#HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
command_list = ['ls','date','name']
python_list = ['os.listdir()','ctime()','os.name']



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
        #tcpClientSocket.send(b'[%s] %s' % (bytes(ctime(), 'utf-8'), data))
        data = data.decode('utf-8')
        if data in command_list:
            index = command_list.index(data)
            result = eval(python_list[index])
            if type(result) is not str:
                result = ','.join(result)
            print(result)
            tcpClientSocket.send(b'%s' % (bytes(result, 'utf-8')))
        else:
            tcpClientSocket.send(b'[%s] %s' % (bytes(ctime(), 'utf-8'), bytes(data, 'utf-8')))
        #windows上没有这个判断无法持续运行
        if os.name != 'nt':
            tcpClientSocket.close()

    tcpServerSocket.close()
