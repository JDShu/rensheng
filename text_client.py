import json

# Twisted imports
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import stdio

from service import decode_service
from enums import ResultIds

class IOProtocol(LineReceiver):
    from os import linesep as delimiter

    def __init__(self, app_factory):
        self.f = app_factory
        self.f.io = self

    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        self.sendLine('Echo: ' + line)
        self.transport.write('>>> ')
        self.f.server.sendLine(line)

class AppProtocol(LineReceiver):

    def __init__(self):
        pass

    def lineReceived(self, line):
        data = line.split(':', 1)
        response_id = int(data[0])
        if response_id == ResultIds.TICK:
            if len(data[1].split(':')) > 1:
                self.factory.io.sendLine(line)
        elif response_id == ResultIds.LOAD:
            self.factory.service = decode_service(data[1])

    def connectionMade(self):
        self.factory.server = self

    def clientConnectionLost(self, connection, reason):
        print connection, reason

class AppFactory(ClientFactory):

    protocol = AppProtocol

    def __init__(self):
        self.service = None
        self.server = None

if __name__ == '__main__':
    f = AppFactory()
    stdio.StandardIO(IOProtocol(f))

    from twisted.internet import reactor
    reactor.connectTCP("localhost",9999,f) # connect to IRC
    reactor.run()
