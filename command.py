from enums import CommandIds

class Command(object):
    def __init__(self, command_id, **args):
        self.id = command_id
        self.args = args

# protocol: 0;character_id;x_coord;y_coord;floor
class MoveCommand(Command):
    def __init__(self, command_id, character_id, x, y, floor):
        self.id = int(command_id)
        self.character_id = int(character_id)
        self.x = float(x)
        self.y = float(y)
        self.floor = int(floor)

    @property
    def coordinates(self):
        return (self.x, self.y, self.floor)

    def serialize(self):
        return "%d;%d;%f;%f;%d" % (self.id, self.character_id, self.x, self.y, self.floor)

    def validate(self):
        return

def parse_command(line):
    command_tokens = line.split('.')
    command_id = int(command_tokens[0])
    command_args = command_tokens[1:]
    if command_id == CommandIds.MOVE:
        command = MoveCommand(command_id, *command_args)
    else:
        return Command(command_id, command_args)
    command.validate()
    return command
