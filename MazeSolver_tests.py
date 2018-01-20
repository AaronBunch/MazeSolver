#!/usr/bin/env python

import unittest
from MazeSolver import MazeSolver 

class MazeSolverTestCase(unittest.TestCase):
    """Tests for MazeSolver class."""

    def setUp(self):
        """Define the internal maze characters."""

        self.wall = '\u2588'
        self.path = ' '
        self.start = 'S'
        self.dest = 'D'
        # instantiate a MazeSolver object
        self.ms = MazeSolver()

    def test_get_maze(self):
        """Is the source maze accurately loaded?"""

        filename = "test_maze_001.txt"
        correct_maze = [self.wall * 7,
                        self.wall + self.path * 4 + self.dest + self.wall,
                        self.wall * 3 + self.path + self.wall * 3,
                        self.wall + self.start + self.path * 4 + self.wall,
                        self.wall * 7]
        test_maze = self.ms.get_maze(filename, return_maze=True)
        self.assertEqual(test_maze, correct_maze)

    def test_verify_maze(self):
        """Is a boundary wall correctly added when necessary?"""

        # test right wall
        filename = "test_maze_002.txt"
        correct_maze = [self.wall*8,
                        self.wall + self.path*5 + self.dest + self.wall,
                        self.wall*3 + self.path + self.wall*4,
                        self.wall + self.start + self.path*4 + self.wall*2,
                        self.wall*8]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(test_maze, correct_maze)

        # test left wall
        filename = "test_maze_003.txt"
        correct_maze = [self.wall*8,
                        self.wall + self.path*5 + self.dest + self.wall,
                        self.wall*4 + self.path + self.wall*3,
                        self.wall*2 + self.start + self.path*4 + self.wall,
                        self.wall*8]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(test_maze, correct_maze)

        # test top wall
        filename = "test_maze_004.txt"
        correct_maze = [self.wall*7,
                        self.wall*4 + self.path + self.wall*2,
                        self.wall + self.path*4 + self.dest + self.wall,
                        self.wall*3 + self.path + self.wall*3,
                        self.wall + self.start + self.path*4 + self.wall,
                        self.wall*7]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(test_maze, correct_maze)

        # test bottom wall
        filename = "test_maze_005.txt"
        correct_maze = [self.wall*7,
                        self.wall + self.path*4 + self.dest + self.wall,
                        self.wall*3 + self.path + self.wall*3,
                        self.wall + self.start + self.path*4 + self.wall,
                        self.wall*4 + self.path + self.wall*2,
                        self.wall*7]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(test_maze, correct_maze)

        # test all walls
        filename = "test_maze_006.txt"
        correct_maze = [self.wall*9,
                        self.wall*6 + self.path + self.wall*2,
                        self.wall + self.path*5 + self.dest + self.wall*2,
                        self.wall*4 + self.path + self.wall*4,
                        self.wall*2 + self.start + self.path*5 + self.wall,
                        self.wall*5 + self.path + self.wall*3,
                        self.wall*9]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(test_maze, correct_maze)

if __name__ == '__main__':
    unittest.main()

