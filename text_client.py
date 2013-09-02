import json

# Twisted imports
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import stdio

from service import decode_service
from enums import MessageIds, CommandIds

import text_menus

commands = {"move" : CommandIds.MOVE,
            "interact" : CommandIds.INTERACT}

def help_text(line_args):
    if not line_args:
        return text_menus.command_menu
    elif line_args[0] in commands:
        return text_menus.command_help[line_args[0]]
    else:
        return "No such command: %s" % line_args[0]

class IOState():
    """ Track where in the interface we are """

    def __init__(self):
        self.current_command = None
        self.message = None
        self.ready = False

    def handle_command(self, line):
        line_args = line.split(" ")
        if self.current_command == None:
            if line_args[0] in commands:
                self.current_command = commands[line]
                return "command set to %s" % line
            elif line_args[0] == "help":
                return help_text(line_args[1:])
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

class IOProtocol(LineReceiver, object):
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

    def sendLine(self, line):
        super(IOProtocol, self).sendLine(line)
        self.transport.write('>>> ')

class AppProtocol(LineReceiver):

    def __init__(self):
        pass

    def lineReceived(self, line):
        data = line.split(':', 1)
        response_id = int(data[0])
        if response_id == MessageIds.TICK:
            if commands_exist(data):
                commands = data[1].split(':')
                self.factory.io.sendLine("Server message at tick %d: %s"
                                         % (int(commands[0]), commands[1:] ))
        elif response_id == MessageIds.LOAD:
            self.factory.service = decode_service(data[1])

    def connectionMade(self):
        self.factory.server = self

    def clientConnectionLost(self, connection, reason):
        print connection, reason

def commands_exist(data):
    return len(data[1].split(':')) > 1

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
