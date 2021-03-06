import json

from game_state import GameState, decode_state

class Service(object):
    """
    Handles the game logic.
    """

    def __init__(self):
        self.state = None
        self.tick = 0

    def new_game(self):
        self.state = GameState()

    def move(self, character_id, coordinates):
        result = self.state.move_character(character_id, coordinates)
        return result

    def character_location(self, character_id):
        return self.state.character_location(character_id)

    def interact(self):
        pass

    def inc_tick(self):
        self.state.progress()
        self.tick += 1

    def dispatch_command(self, command_obj):
        if command_obj.id == CommandIds.MOVE:
            result = self.move(command_obj.character_id, command_obj.coordinates)
            return result
        elif command_id == CommandIds.INTERACT:
            pass
        else:
            pass

def decode_service(json_string):
    s = Service()
    json_data = json.JSONDecoder().decode(json_string)
    s.state = decode_state(json_data)
    return s
