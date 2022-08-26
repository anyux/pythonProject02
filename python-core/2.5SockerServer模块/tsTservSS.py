#!/usr/bin/env python

from socketserver import (TCPServer as tcp,
                          StreamRequestHandler as srh)
from time import ctime
import os

HOST = 'localhost'
PORT = 21567
ADDR = (HOST,PORT)

class MyRequestHandler(srh):
    def handle(self):
        print('...connected from : ',self.client_address)
        data = self.rfile.readline().decode('utf-8')
        print(data.strip())
        self.wfile.write(b'[%s],%s' % (bytes(ctime(), 'utf-8'),data.encode('utf-8')))
        #windows上没有这个判断无法持续运行
        if os.name != 'nt':
            self.close()

tcpServ = tcp(ADDR,MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()