#!/usr/bin/env python

from twisted.internet import protocol, reactor
from time import ctime

PORT = 21567

class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getHost()
        print('...connected from: ',clnt)

    def dataReceived(self, data: bytes):
        self.transport.write(b'[%s] %s' % (bytes(ctime(),'utf-8'),data))

factory = protocol.Factory()
factory.protocol = TSServProtocol

print('waiting for connection...')

reactor.listenTCP(PORT,factory)
reactor.run()


