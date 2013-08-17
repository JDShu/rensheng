import json

# Twisted imports
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import stdio

from service import decode_service
from enums import ResultIds, CommandIds

commands = {"move" : CommandIds.MOVE,
            "interact" : CommandIds.INTERACT}

class IOState():
    """ Track where in the interface we are """

    def __init__(self):
        self.current_command = None
        self.message = None
        self.ready = False

    def handle_command(self, line):
        if self.current_command == None:
            if line in commands:
                self.current_command = commands[line]
                return "command set to %s" % line
            else:
                return "Invalid command!"
        elif self.current_command == CommandIds.MOVE:
            try:
                character_id, x, y, level = line.split(",")
                x = int(x)
                y = int(y)
                level = int(level)
                character_id = int(character_id)
                details = (character_id, x, y, level)
                print (CommandIds.MOVE,) + details
                self.message = "%d.%d.%d.%d.%d" % ((CommandIds.MOVE,) + details)
                self.ready = True
                self.current_command = None
                return "Character %d sent to coordinates (%d,%d) on floor %d" % details
            except ValueError:
                return "Invalid move details. Format is <character id>,<x>,<y>,<floor>"

class IOProtocol(LineReceiver):
    from os import linesep as delimiter

    def __init__(self, app_factory):
        self.f = app_factory
        self.f.io = self
        self.state = IOState()

    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        feedback = self.state.handle_command(line)
        print feedback
        self.transport.write('>>> ')
        if self.state.ready:
            self.state.ready = False
            self.f.server.sendLine(self.state.message)

class AppProtocol(LineReceiver):

    def __init__(self):
        pass

    def lineReceived(self, line):
        data = line.split(':', 1)
        response_id = int(data[0])
        if response_id == ResultIds.TICK:
            if len(data[1].split(':')) > 1:
                self.factory.io.sendLine("Server feedback: " + line)
        elif response_id == ResultIds.LOAD:
            self.factory.service = decode_service(data[1])

    def connectionMade(self):
        self.factory.server = self

    def clientConnectionLost(self, connection, reason):
        print connection, reason

class AppFactory(ClientFactory):

    protocol = AppProtocol

    def __init__(self):
        # Client's tracking of the service state
        self.service = None
        self.server = None

if __name__ == '__main__':
    f = AppFactory()
    stdio.StandardIO(IOProtocol(f))

    from twisted.internet import reactor
    reactor.connectTCP("localhost",9999,f) # connect to IRC
    reactor.run()
