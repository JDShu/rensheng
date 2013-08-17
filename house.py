import json

DEFAULT_SIZE = 50

class Coord(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "<Coord: %d, %d>" % (self.x, self.y)

    def __cmp__(self, other):
        return hash((self.x, self.y)) - hash((other.x, other.y))

    def serialize(self):
        return [self.x, self.y]

class Wall(object):

    def __init__(self, coord1, coord2):
        self.coords = sorted([coord1, coord2])

    def __eq__(self, other):
        return self.coords == other.coords

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.coords[0]) ^ hash(self.coords[1])

    def serialize(self):
        temp = []
        for c in self.coords:
            temp += c.serialize()
        return temp

    def __repr__(self):
        x, y = self.coords
        return "<Wall: (%r, %r)>" % (x, y)

class Floor(object):

    def __init__(self):
        self.walls = set()
        self.tiles = set()

    def add_walls(self, coord_pair_list):
        for w in coord_pair_list:
            c1, c2 = w
            self.walls.add(Wall(Coord(*c1), Coord(*c2)))

class House(object):

    def __init__(self):
        self.width = self.length = DEFAULT_SIZE
        self.floors = [Floor()]
        self.objects = []

    def new_floor(self):
        self.floors += [Floor()]

class FloorEncoder(json.JSONEncoder):

    def default(self, floor):
        encoded = None
        try:
            encoded_walls = []
            for w in floor.walls:
                encoded_walls += w.serialize()

            encoded = {'walls' : encoded_walls,
                       'tiles' : 0} # TODO: Implement tile serialization
        except:
            json.JSONEncoder.default(self, house)
        else:
            return encoded


class HouseEncoder(json.JSONEncoder):

    def default(self, house):
        d = None
        try:
            d = {'w' : house.width,
                 'l' : house.length,
                 'floors' : FloorEncoder().encode(house.floors)}
        except:
            raise
            json.JSONEncoder.default(self, house)
        else:
            return d

def decode_house(json_data):
    h = House()
    h.width = json_data[u'w']
    h.length = json_data[u'l']
    h.floors = decode_floors(json.JSONDecoder().decode(json_data[u'floors']))
    return h

def decode_floors(json_data):
    return [decode_floor(f) for f in json_data]

def decode_floor(json_data):
    f = Floor()
    wall_data = json_data[u'walls']
    f.walls = set([decode_wall(w) for w in chunks(wall_data, 4)])
    f.tiles = 0
    return f

def decode_wall(quad):
    x1, y1, x2, y2 = quad
    return Wall(Coord(x1, y1), Coord(x2, y2))

def chunks(l, n):

    """
    Split list into n sized chunks
    """

    return zip(*[iter(l)]*n)
