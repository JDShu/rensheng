import json
from itertools import tee, izip

import graph_2d
from character import CharacterEncoder, decode_characters
from enums import ResultIds
from house import HouseEncoder, House, decode_house
from result import Result

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def path_length(path):
    return sum(graph_2d.euclidean(first, second) for first, second in pairwise(path))

def calculate_move_lifespan(character, path):
    return path_length(path)/character.speed

class Delta(object):
    """
    Represents a change in the game state that occurs every time the state updates
    """
    def __init__(self, lifespan, args):
        self.lifespan = lifespan
        if args:
            self.args = args
        else:
            self.args = None

    def update(self):
        print "l", self.lifespan
        self.lifespan -= 1
        self.change_function()

class MoveDelta(Delta):

    def __init__(self, character, destination, path):
        # save destination in case the current path becomes invalid
        self.destination = destination
        self.character = character
        self.path = path

        # calculate the lifespan
        lifespan = calculate_move_lifespan(character, path)
        Delta.__init__(self, lifespan, None)

    def change_function(self):
        current_destination = self.path[0]
        arrived = self.character.move_toward(current_destination)
        if arrived:
            self.path = self.path[1:]
            print "lifespan: ", self.lifespan


class GameState(object):

    def __init__(self):
        self.characters = {}
        self.house = House()
        self.pathfinding_grid = None
        self.deltas = set()

    def move_character(self, character_id, destination):
        # get the current graph and add the current character's position as a node
        graph = self.pathfinding_grid.copy()
        # use the graph's shortest path method
        try:
            path = graph.shortest_path(self.characters[character_id].position, destination)
            self.deltas.add(MoveDelta(self.characters[character_id], destination, path))
            return Result(ResultIds.SUCCESS)
        # if it is not reachable, set the result to a failure
        except graph_2d.ImpossiblePath:
        # otherwise set the result to success
            return Result(ResultIds.ERROR)
        return r

    def character_location(self, character_id):
        return self.characters[character_id].position

    def serialize(self):
        return StateEncoder().encode(self)

    def progress(self):
        new_deltas = set()
        for delta in self.deltas:
            delta.update()
            if delta.lifespan > 0:
                new_deltas.add(delta)
        self.deltas = new_deltas

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
