import math
import json

class CharacterEncoder(json.JSONEncoder):

    def default(self, character):
        d = None
        try:
            d = {'name' : character.name,
                 #'age'  : character.age,
                 #'needs' : character.needs
                 }
        except:
            json.JSONEncoder.default(self, character)
        else:
            return d

class Character(object):
    current_max = 0

    def __init__(self, name):
        self.id = Character.current_max
        Character.current_max += 1
        self.name = name
        self.position = (0, 0)
        self.speed = 0.1

    def move_toward(self, destination):
        """ Returns True if arrived at destination """

        original_position = self.position

        x1, y1 = self.position
        x2, y2 = destination

        x, y = x2-x1, y2-y1
        mag = math.hypot(x,y)

        if mag < self.speed:
            self.position = destination
            return True

        unit_x = x/mag
        unit_y = y/mag

        self.position = (x1 + unit_x*self.speed, y1 + unit_y*self.speed)
        return False

def decode_characters(json_data):
    """
    Expects an array of properly formated characters
    """

    characters = {}
    for cid, data in json_data.iteritems():
        characters[int(cid)] = Character(data[u'name'])
    return characters
