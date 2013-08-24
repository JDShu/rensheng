import json

from house import HouseEncoder, House, decode_house
from character import CharacterEncoder, decode_characters
from result import Result
from enums import ResultIds

class GameState(object):

    def __init__(self):
        self.characters = {}
        self.house = House()

    def move_character(self, character_id, coordinates):
        # assume no errors for now
        r = Result(ResultIds.SUCCESS)
        return r

    def serialize(self):
        return StateEncoder().encode(self)

class StateEncoder(json.JSONEncoder):
    def default(self, state):
        d = None
        try:
            d = {'characters' : CharacterEncoder().encode(state.characters),
                 'house'      : HouseEncoder().encode(state.house)}
        except:
            json.JSONEncoder.default(self, state)
        else:
            return d

def decode_state(json_data):
    house = json.JSONDecoder().decode(json_data[u'house'])
    characters = json.JSONDecoder().decode(json_data[u'characters'])
    state = GameState()
    state.house = decode_house(house)
    state.characters = decode_characters(characters)
    return state
