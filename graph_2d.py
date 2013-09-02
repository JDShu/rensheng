import math
from collections import namedtuple
import networkx as nx


Point = namedtuple('Point', ['x', 'y'])

def euclidean(pos_1, pos_2):
    """
    2d euclidean distance
    """

    return math.hypot(abs(pos_1.x-pos_2.x), abs(pos_1.y-pos_2.y))

class ImpossiblePath(Exception):
    def __init__(self, start, destination):
        self.start = start
        self.destination = destination

    def __repr__(self):
        return repr((start, destination))

class Graph2D(object):

    def __init__(self, orig=None):
        if orig == None:
            self.graph = nx.Graph()
        else:
            self.graph = orig

    def add_node(self, point):
        self.graph.add_node(Point(*point))

    def add_edge(self, point1, point2, weight):
        p1, p2 = Point(*point1), Point(*point2)
        self.graph.add_edge(p1, p2, weight=weight)

    def shortest_path(self, start, destination):
        start, destination = Point(*start), Point(*destination)
        try :
            return nx.algorithms.shortest_paths.astar.astar_path(self.graph, start, destination, euclidean)
        except nx.NetworkXNoPath:
            raise ImpossiblePath(start, destination)

    def copy(self):
        return Graph2D(self.graph.copy())

class SquareGraph(Graph2D):

    def __init__(self, w, h):
        Graph2D.__init__(self)
        for i in xrange(w):
            for j in xrange(h):
                self.add_node((i, j))
                if j != 0:
                    self.add_edge((i,j), (i, j-1), 1)
                if i != 0:
                    self.add_edge((i,j), (i-1, j), 1)
