from twisted.trial import unittest

import game_state
import graph_2d
import character
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
