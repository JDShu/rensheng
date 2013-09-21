from twisted.trial import unittest

import game_state
import graph_2d
import character
import service
from enums import ResultIds

class MoveTest(unittest.TestCase):
    def test_square_graph(self):
        g = game_state.GameState()
        g.pathfinding_grid = graph_2d.SquareGraph(3,3)
        path = g.pathfinding_grid.shortest_path((0,0), (2,2))
        self.assertEqual(path[0], (0,0))
        self.assertEqual(path[-1], (2,2))
        self.assertNotEqual(len(path), 2)

    def test_move_character(self):
        g = game_state.GameState()
        g.pathfinding_grid = graph_2d.SquareGraph(3,3)
        c = character.Character("Bob")
        g.characters[0] = c
        r = g.move_character(0, (2,2))
        self.assertTrue(r.is_success)

    def test_move_character_impossible(self):
        g = game_state.GameState()
        g.pathfinding_grid = graph_2d.SquareGraph(3,3)
        c = character.Character("Bob")
        g.characters[0] = c
        r = g.move_character(0, (2,3))
        self.assertFalse(r.is_success)

class MoveServiceTest(unittest.TestCase):
    """
    Test the movement elements of the service object
    """

    def test_service_move_simple(self):
        s = service.Service()
        s.state = game_state.GameState()
        s.state.pathfinding_grid = graph_2d.SquareGraph(3,3)
        s.state.characters = { 0 : character.Character("Bob") }
        # character id, destination coordinate
        r = s.move(0, (1,0))

        for _ in xrange(20):
            s.inc_tick()

        self.assertEqual(s.character_location(0), (1,0))


    def test_service_move_long(self):
        s = service.Service()
        s.state = game_state.GameState()
        s.state.pathfinding_grid = graph_2d.SquareGraph(3,3)
        s.state.characters = { 0 : character.Character("Bob") }
        # character id, destination coordinate
        r = s.move(0, (2,2))

        for _ in xrange(200):
            s.inc_tick()

        self.assertEqual(s.character_location(0), (2,2))
