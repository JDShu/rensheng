from enums import CommandIds

class Command(object):
    def __init__(self, command_id, **args):
        self.id = command_id
        self.args = args

class MoveCommand(Command):
    def __init__(self, command_id, character_id, x, y, floor):
        self.id = command_id
        self.character_id = character_id
        self.x = float(x)
        self.y = float(y)
        self.floor = int(floor)

    @property
    def coordinates(self):
        return (self.x, self.y, self.floor)

    def serialize(self):
        return "%d.%d.%f.%f.%d" % self.coordinates

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
