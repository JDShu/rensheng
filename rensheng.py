from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

from enums import CommandIds, ResultIds
from service import Service
from command import parse_command

TICK_DURATION = 0.2

class AppProtocol(LineReceiver):

    def __init__(self):
        pass

    def connectionMade(self):
        data = self.factory.service.state.serialize()
        self.sendLine(str(ResultIds.LOAD) + ':' + data)
        self.factory.clients.append(self)

    def lineReceived(self, line):
        print "recieved command: %s" % line
        try:
            command = parse_command(line)
            self.dispatch_command(command)
        except (IndexError, ValueError):
            print "Invalid Command: %s" % line

    def dispatch_command(self, command_obj):
        # protocol: 0.character_id.x_coord.y_coord.floor
        if command_obj.id == CommandIds.MOVE:
            result = self.factory.service.move(command_obj.character_id, command_obj.coordinates)
            self.handle_result(result, command_obj)
        elif command_id == CommandIds.INTERACT:
            pass
        else:
            pass

    def transform_error(self, error):
        return "%d:%d" % (error.id, error.reason_id)

    def handle_result(self, result, command_obj):
        if result.is_error:
            self.sendLine(self.transform_error(result))
        elif result.is_success:
            self.factory.command_buffer.append(command_obj)
        else:
            print "send_result: Shouldn't be here!"

    def send_commands(self, command_buffer):
        tick = self.factory.service.tick
        data = ":".join(map(str,[ResultIds.TICK, tick])
                        + [c.serialize() for c in command_buffer])
        self.sendLine(data)

    def transform_result(self, result):
        return ".".join(map(str, result.args))

class AppFactory(ServerFactory):

    protocol = AppProtocol

    def __init__(self):
        self.service = None
        self.command_buffer = []
        self.clients = []

    def inc_tick(self):
        self.service.inc_tick()
        from twisted.internet import reactor
        reactor.callLater(TICK_DURATION, self.inc_tick)
        #print "Tick %d" % service.tick

        for client in self.clients:
            client.send_commands(self.command_buffer)
        self.command_buffer = []

if __name__ == '__main__':

    f = AppFactory()
    service = Service()

    import character, game_state

    game = game_state.GameState()
    game.characters[0] = character.Character('john')
    game.house.floors[0].add_walls([t for t in zip(zip([2]*5, range(5)), zip([3]*5, range(5)))])
    service.state = game
    f.service = service
    from twisted.internet import reactor
    reactor.listenTCP(9999, f)
    reactor.callWhenRunning(f.inc_tick)
    reactor.run()
