import json

from game_state import GameState, decode_state

class Service(object):
    """
    Handles the game logic.
    """

    def __init__(self):
        self.state = None
        self.tick = 0
        self.command_buffer = []

    def new_game(self):
        self.state = GameState()

    def move(self, character_id, coordinates):
        result = self.state.move_character(character_id, coordinates)
        return result

    def interact(self):
        pass

    def inc_tick(self):
        self.tick += 1

def decode_service(json_string):
    s = Service()
    json_data = json.JSONDecoder().decode(json_string)
    s.state = decode_state(json_data)
    return s
