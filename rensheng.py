from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

from enums import CommandIds, ResultIds
from service import Service

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
        command = line.split('.')
        try:
            command_id = int(command[0])
            self.dispatch_command(command_id, command[1:])
        except (IndexError, ValueError):
            print "Invalid Command: %s" % line

    def dispatch_command(self, command_id, arg_list):
        # protocol: 0.character_id.x_coord.y_coord.floor
        if command_id == CommandIds.MOVE:
            char_id = arg_list[0]
            coordinates = (arg_list[1], arg_list[2], arg_list[3])
            result = self.factory.service.move(char_id, coordinates)
            self.handle_result(result)
        elif command_id == CommandIds.INTERACT:
            pass
        else:
            pass

    def transform_error(self, error):
        return "%d:%d" % (error.id, error.reason_id)

    def handle_result(self, result):
        if result.id == ResultIds.ERROR:
            self.sendLine(self.transform_error(result))
        elif result.id == ResultIds.SUCCESS:
            self.factory.command_buffer.append(self.transform_result(result))
        else:
            print "send_result: Shouldn't be here!"

    def send_commands(self, command_buffer):
        tick = self.factory.service.tick
        data = ":".join(map(str,[ResultIds.TICK, tick])
                        + [c for c in command_buffer])
        self.sendLine(data)

    def transform_result(self, result):
        return ".".join([str(result.id)] + list(result.args))

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
