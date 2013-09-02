import json

import graph_2d
from house import HouseEncoder, House, decode_house
from character import CharacterEncoder, decode_characters
from result import Result
from enums import ResultIds

class GameState(object):

    def __init__(self):
        self.characters = {}
        self.house = House()
        self.pathfinding_grid = None

    def move_character(self, character_id, coordinates):
        # get the current graph and add the current character's position as a node
        graph = self.pathfinding_grid.copy()
        # use the graph's shortest path method
        try:
            p = graph.shortest_path(self.characters[character_id].position, coordinates)
            return Result(ResultIds.SUCCESS)
        # if it is not reachable, set the result to a failure
        except graph_2d.ImpossiblePath:
        # otherwise set the result to success
            return Result(ResultIds.ERROR)
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
