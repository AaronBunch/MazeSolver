#!/usr/bin/env python

import unittest
from MazeSolver import MazeSolver 

class MazeSolverTestCase(unittest.TestCase):
    """Tests for MazeSolver class."""

    def setUp(self):
        """Define the internal maze characters."""

        self.ms = MazeSolver()
        self.wall = self.ms.wall
        self.path = self.ms.path
        self.start = self.ms.start
        self.dest = self.ms.dest

    def test_get_maze(self):
        """The source maze is correctly loaded."""

        filename = "test_mazes/test_maze_001.txt"
        correct_maze = [self.wall * 7,
                        self.wall + self.path * 4 + self.dest + self.wall,
                        self.wall * 3 + self.path + self.wall * 3,
                        self.wall + self.start + self.path * 4 + self.wall,
                        self.wall * 7]
        test_maze = self.ms.get_maze(filename, return_maze=True)
        self.assertEqual(correct_maze, test_maze)

    def test_verify_maze(self):
        """The maze has the correct format."""

        # test right wall
        filename = "test_mazes/test_maze_002.txt"
        correct_maze = [self.wall*8,
                        self.wall + self.path*5 + self.dest + self.wall,
                        self.wall*3 + self.path + self.wall*4,
                        self.wall + self.start + self.path*4 + self.wall*2,
                        self.wall*8]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(correct_maze, test_maze)

        # test left wall
        filename = "test_mazes/test_maze_003.txt"
        correct_maze = [self.wall*8,
                        self.wall + self.path*5 + self.dest + self.wall,
                        self.wall*4 + self.path + self.wall*3,
                        self.wall*2 + self.start + self.path*4 + self.wall,
                        self.wall*8]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(correct_maze, test_maze)

        # test top wall
        filename = "test_mazes/test_maze_004.txt"
        correct_maze = [self.wall*7,
                        self.wall*4 + self.path + self.wall*2,
                        self.wall + self.path*4 + self.dest + self.wall,
                        self.wall*3 + self.path + self.wall*3,
                        self.wall + self.start + self.path*4 + self.wall,
                        self.wall*7]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(correct_maze, test_maze)

        # test bottom wall
        filename = "test_mazes/test_maze_005.txt"
        correct_maze = [self.wall*7,
                        self.wall + self.path*4 + self.dest + self.wall,
                        self.wall*3 + self.path + self.wall*3,
                        self.wall + self.start + self.path*4 + self.wall,
                        self.wall*4 + self.path + self.wall*2,
                        self.wall*7]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(correct_maze, test_maze)

        # test all walls
        filename = "test_mazes/test_maze_006.txt"
        correct_maze = [self.wall*9,
                        self.wall*6 + self.path + self.wall*2,
                        self.wall + self.path*5 + self.dest + self.wall*2,
                        self.wall*4 + self.path + self.wall*4,
                        self.wall*2 + self.start + self.path*5 + self.wall,
                        self.wall*5 + self.path + self.wall*3,
                        self.wall*9]
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        self.assertEqual(correct_maze, test_maze)

        # test missing destination
        filename = "test_mazes/test_maze_007.txt"
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        # if there is a problem, verify_maze returns None
        self.assertIsNone(test_maze)

        # test missing start
        filename = "test_mazes/test_maze_011.txt"
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        # if there is a problem, verify_maze returns None
        self.assertIsNone(test_maze)

        # test more than one start
        filename = "test_mazes/test_maze_009.txt"
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        # if there is a problem, verify_maze returns None
        self.assertIsNone(test_maze)

        # test more than one destination
        filename = "test_mazes/test_maze_010.txt"
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        # if there is a problem, verify_maze returns None
        self.assertIsNone(test_maze)

        # test rectangularity
        filename = "test_mazes/test_maze_008.txt"
        self.ms.get_maze(filename)
        test_maze = self.ms.verify_maze(return_maze=True)
        # if there is a problem, verify_maze returns None
        self.assertIsNone(test_maze)

    def test_find_char(self):
        """Returns the correct position(s) of the character."""

        filename = "test_mazes/test_maze_002.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        # find start 
        correct_row_col = (3, 1)
        test_row, test_col = self.ms.find_char(maze, self.start)
        self.assertEqual(correct_row_col, (test_row[0], test_col[0]))

        # find destination
        correct_row_col = (1, 6)
        test_row, test_col = self.ms.find_char(maze, self.dest)
        self.assertEqual(correct_row_col, (test_row[0], test_col[0]))

        # find path locations
        correct_rows = [1, 1, 1, 1, 1, 2, 3, 3, 3, 3]
        correct_cols = [1, 2, 3, 4, 5, 3, 2, 3, 4, 5]
        test_rows, test_cols = self.ms.find_char(maze, self.path)
        self.assertEqual((correct_rows, correct_cols),
                         (test_rows, test_cols))
       
        # find wall locations
        correct_rows = [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 3, 3,
                        4, 4, 4, 4, 4, 4, 4]
        correct_cols = [0, 1, 2, 3, 4, 5, 6, 0, 0, 1, 2, 4, 5, 6, 0, 6,
                        0, 1, 2, 3, 4, 5, 6]
        test_rows, test_cols = self.ms.find_char(maze, self.wall)
        self.assertEqual((correct_rows, correct_cols),
                         (test_rows, test_cols))

    def test_count_char(self):
        """Returns the correct count of the character."""

        filename = "test_mazes/test_maze_001.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        
        # count start
        correct_count = 1
        test_count = self.ms.count_char(maze, self.start)
        self.assertEqual(correct_count, test_count)

        # count destination
        correct_count = 1
        test_count = self.ms.count_char(maze, self.dest)
        self.assertEqual(correct_count, test_count)

        # count path
        correct_count = 9
        test_count = self.ms.count_char(maze, self.path)
        self.assertEqual(correct_count, test_count)

        # count wall
        correct_count = 24
        test_count = self.ms.count_char(maze, self.wall)
        self.assertEqual(correct_count, test_count)

    def test_num_branches(self):
        """Returns the correct number of branches in the maze."""

        filename = "test_mazes/test_maze_012.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        correct_count = 4
        test_count = self.ms.num_branches(maze)
        self.assertEqual(correct_count, test_count)

    def test_insert_char(self):
        """Inserts a character in the correct position."""

        filename = "test_mazes/test_maze_001.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        correct_maze = [self.wall*7,
                        self.wall + self.path*4 + self.dest + self.wall,
                        (self.wall + self.path + self.wall + self.path +
                            self.wall*3),
                        self.wall + self.start + self.path*4 + self.wall,
                        self.wall*7]
        test_maze = self.ms.insert_char(maze, 2, 1, self.path)
        self.assertEqual(correct_maze, test_maze)

    def test_get_paths(self):
        """Returns the correct open paths at a position in the maze."""

        filename = "test_mazes/test_maze_001.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        correct_paths = False, True, True, True
        test_paths = self.ms.get_paths(maze, 1, 3)
        self.assertEqual(correct_paths, test_paths)

        # check that start and dest are recognized as open paths
        correct_paths = False, False, True, True
        test_paths = self.ms.get_paths(maze, 1, 4)
        self.assertEqual(correct_paths, test_paths)

        correct_paths = False, False, True, True
        test_paths = self.ms.get_paths(maze, 3, 2)
        self.assertEqual(correct_paths, test_paths)

        # check at start and dest
        correct_paths = False, False, False, True
        test_paths = self.ms.get_paths(maze, 1, 5)
        self.assertEqual(correct_paths, test_paths)

        correct_paths = False, False, True, False
        test_paths = self.ms.get_paths(maze, 3, 1)
        self.assertEqual(correct_paths, test_paths)
       
        # check at the borders
        correct_paths = False, False, False, False
        test_paths = self.ms.get_paths(maze, 0, 0)
        self.assertEqual(correct_paths, test_paths)

        correct_paths = False, False, True, False
        test_paths = self.ms.get_paths(maze, 1, 0)
        self.assertEqual(correct_paths, test_paths)

        correct_paths = False, False, False, False
        test_paths = self.ms.get_paths(maze, 4, 0)
        self.assertEqual(correct_paths, test_paths)

        correct_paths = True, False, False, False
        test_paths = self.ms.get_paths(maze, 4, 3)
        self.assertEqual(correct_paths, test_paths)

        correct_paths = False, False, False, False
        test_paths = self.ms.get_paths(maze, 4, 6)
        self.assertEqual(correct_paths, test_paths)

        correct_paths = False, False, False, True
        test_paths = self.ms.get_paths(maze, 1, 6)
        self.assertEqual(correct_paths, test_paths)

    def test_is_dead_end(self):
        """Correctly identifies a position as a dead-end."""

        filename = "test_mazes/test_maze_001.txt"
        maze = self.ms.get_maze(filename, return_maze=True)

        correct = True
        test = self.ms.is_dead_end(maze, 1, 1)
        self.assertEqual(correct, test)
        test = self.ms.is_dead_end(maze, 1, 5)
        self.assertEqual(correct, test)
        test = self.ms.is_dead_end(maze, 3, 1)
        self.assertEqual(correct, test)
        test = self.ms.is_dead_end(maze, 3, 5)
        self.assertEqual(correct, test)
        
        correct = False
        test = self.ms.is_dead_end(maze, 1, 2)
        self.assertEqual(correct, test)
        test = self.ms.is_dead_end(maze, 1, 3)
        self.assertEqual(correct, test)
        test = self.ms.is_dead_end(maze, 2, 3)
        self.assertEqual(correct, test)
        
    def test_is_walled_in(self):
        """Correctly identifies a position as walled-in."""

        filename = "test_mazes/test_maze_013.txt"
        maze = self.ms.get_maze(filename, return_maze=True)

        correct = True
        test = self.ms.is_walled_in(maze, 1, 1)
        self.assertEqual(correct, test)
        test = self.ms.is_walled_in(maze, 1, 5)
        self.assertEqual(correct, test)
        test = self.ms.is_walled_in(maze, 3, 1)
        self.assertEqual(correct, test)
        # check a non-path tile on the border   
        test = self.ms.is_walled_in(maze, 4, 2)
        self.assertEqual(correct, test)
        
        correct = False
        test = self.ms.is_walled_in(maze, 1, 3)
        self.assertEqual(correct, test)
        test = self.ms.is_walled_in(maze, 3, 3)
        self.assertEqual(correct, test)
        # check a non-path tile on the border
        test = self.ms.is_walled_in(maze, 0, 3)
        self.assertEqual(correct, test)

    def test_is_branch(self):
        """Correctly identifies a position as a branch in the path."""

        filename = "test_mazes/test_maze_014.txt"
        maze = self.ms.get_maze(filename, return_maze=True)

        correct = True
        test = self.ms.is_branch(maze, 1, 4)
        self.assertEqual(correct, test)
        test = self.ms.is_branch(maze, 3, 2)
        self.assertEqual(correct, test)
        test = self.ms.is_branch(maze, 3, 4)
        self.assertEqual(correct, test)
        
        correct = False
        test = self.ms.is_branch(maze, 2, 3)
        self.assertEqual(correct, test)
        test = self.ms.is_branch(maze, 2, 4)
        self.assertEqual(correct, test)
        test = self.ms.is_branch(maze, 4, 2)
        self.assertEqual(correct, test)
       
    def test_count_dead_ends(self):
        """Correctly counts the number of dead-ends in a maze.
        
        Includes start and destination tiles."""

        filename = "test_mazes/test_maze_001.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        num_dead_ends = self.ms.count_dead_ends(maze)
        self.assertTrue(num_dead_ends == 4)

        filename = "test_mazes/test_maze_015.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        num_dead_ends = self.ms.count_dead_ends(maze)
        self.assertTrue(num_dead_ends == 0)

    def test_fill_in_dead_ends(self):
        """Correctly fills in all dead-ends.
        
        Does not fill in start and destination tiles, if these are located
        at dead-ends.
        """

        # no loops
        filename = "test_mazes/test_maze_100.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        maze = self.ms.fill_in_dead_ends(maze)
        num_dead_ends = self.ms.count_dead_ends(maze)
        self.assertTrue(num_dead_ends == 2)

        # simple loops
        filename = "test_mazes/test_maze_102.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        maze = self.ms.fill_in_dead_ends(maze)
        num_dead_ends = self.ms.count_dead_ends(maze)
        self.assertTrue(num_dead_ends == 2)

        # complicated loops
        filename = "test_mazes/test_maze_105.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        maze = self.ms.fill_in_dead_ends(maze)
        num_dead_ends = self.ms.count_dead_ends(maze)
        self.assertTrue(num_dead_ends == 0)

    def test_move_north(self):
        """Correctly moves the maze position north.
        
        Does not worry about running off the edge of the maze."""

        row, col = 2, 2
        new_row, new_col = self.ms.move_north(row, col)
        self.assertTrue(new_row == row-1)
        self.assertTrue(new_col == col)

    def test_move_south(self):
        """Correctly moves the maze position south.
        
        Does not worry about running off the edge of the maze."""

        row, col = 2, 2
        new_row, new_col = self.ms.move_south(row, col)
        self.assertTrue(new_row == row+1)
        self.assertTrue(new_col == col)

    def test_move_east(self):
        """Correctly moves the maze position east.
        
        Does not worry about running off the edge of the maze."""

        row, col = 2, 2
        new_row, new_col = self.ms.move_east(row, col)
        self.assertTrue(new_row == row)
        self.assertTrue(new_col == col+1)

    def test_move_west(self):
        """Correctly moves the maze position west.
        
        Does not worry about running off the edge of the maze."""

        row, col = 2, 2
        new_row, new_col = self.ms.move_west(row, col)
        self.assertTrue(new_row == row)
        self.assertTrue(new_col == col-1)

    def test_take_first_step(self):
        """Correctly takes first step in the maze."""

        row, col = (2, 3)
        filename = "test_mazes/test_maze_016.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        paths = self.ms.get_paths(maze, row, col)
        turn = 'right'
        # should step north
        correct_row, correct_col = (1, 3)
        test_row, test_col = self.ms.take_first_step(row, col, paths, turn)
        self.assertEqual((correct_row, correct_col), (test_row, test_col))
        turn = 'left'
        # should step south
        correct_row, correct_col = (3, 3)
        test_row, test_col = self.ms.take_first_step(row, col, paths, turn)
        self.assertEqual((correct_row, correct_col), (test_row, test_col))

        filename = "test_mazes/test_maze_017.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        paths = self.ms.get_paths(maze, row, col)
        turn = 'right'
        # should step east
        correct_row, correct_col = (2, 4)
        test_row, test_col = self.ms.take_first_step(row, col, paths, turn)
        self.assertEqual((correct_row, correct_col), (test_row, test_col))
        turn = 'left'
        # should step west
        correct_row, correct_col = (2, 2)
        test_row, test_col = self.ms.take_first_step(row, col, paths, turn)
        self.assertEqual((correct_row, correct_col), (test_row, test_col))
        
        filename = "test_mazes/test_maze_018.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        paths = self.ms.get_paths(maze, row, col)
        turn = 'right'
        # should step west
        correct_row, correct_col = (2, 2)
        test_row, test_col = self.ms.take_first_step(row, col, paths, turn)
        self.assertEqual((correct_row, correct_col), (test_row, test_col))

        filename = "test_mazes/test_maze_018.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        paths = self.ms.get_paths(maze, row, col)
        turn = 'right'
        # should step west
        correct_row, correct_col = (2, 2)
        test_row, test_col = self.ms.take_first_step(row, col, paths, turn)
        self.assertEqual((correct_row, correct_col), (test_row, test_col))

        filename = "test_mazes/test_maze_019.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        paths = self.ms.get_paths(maze, row, col)
        turn = 'left'
        # should step east
        correct_row, correct_col = (2, 4)
        test_row, test_col = self.ms.take_first_step(row, col, paths, turn)
        self.assertEqual((correct_row, correct_col), (test_row, test_col))

        filename = "test_mazes/test_maze_020.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        paths = self.ms.get_paths(maze, row, col)
        turn = 'left'
        # should step north
        correct_row, correct_col = (1, 3)
        test_row, test_col = self.ms.take_first_step(row, col, paths, turn)
        self.assertEqual((correct_row, correct_col), (test_row, test_col))
        
    def test_take_step(self):
        """Correctly takes a step in the maze."""

        row, col = (2, 3)
        filename = "test_mazes/test_maze_021.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        paths = self.ms.get_paths(maze, row, col)

        # coming from the north
        prev_row, prev_col = (1, 3)
        turn = 'right'
        # should step west
        correct = (2, 2, 2, 3) # new_row, new_col, new_prev_row, new_prev_col
        test = self.ms.take_step(row, col, prev_row, prev_col, paths, turn)
        self.assertEqual(correct, test)
        turn = 'left'
        # should step east  
        correct = (2, 4, 2, 3) # new_row, new_col, new_prev_row, new_prev_col
        test = self.ms.take_step(row, col, prev_row, prev_col, paths, turn)
        self.assertEqual(correct, test)
       
        # coming from the south
        prev_row, prev_col = (3, 3)
        turn = 'right'
        # should step east
        correct = (2, 4, 2, 3) # new_row, new_col, new_prev_row, new_prev_col
        test = self.ms.take_step(row, col, prev_row, prev_col, paths, turn)
        self.assertEqual(correct, test)
        turn = 'left'
        # should step west  
        correct = (2, 2, 2, 3) # new_row, new_col, new_prev_row, new_prev_col
        test = self.ms.take_step(row, col, prev_row, prev_col, paths, turn)
        self.assertEqual(correct, test)

        # coming from the east
        prev_row, prev_col = (2, 4)
        turn = 'right'
        # should step north
        correct = (1, 3, 2, 3) # new_row, new_col, new_prev_row, new_prev_col
        test = self.ms.take_step(row, col, prev_row, prev_col, paths, turn)
        self.assertEqual(correct, test)
        turn = 'left'
        # should step south  
        correct = (3, 3, 2, 3) # new_row, new_col, new_prev_row, new_prev_col
        test = self.ms.take_step(row, col, prev_row, prev_col, paths, turn)
        self.assertEqual(correct, test)

        # coming from the west
        prev_row, prev_col = (2, 2)
        turn = 'right'
        # should step south
        correct = (3, 3, 2, 3) # new_row, new_col, new_prev_row, new_prev_col
        test = self.ms.take_step(row, col, prev_row, prev_col, paths, turn)
        self.assertEqual(correct, test)
        turn = 'left'
        # should step north  
        correct = (1, 3, 2, 3) # new_row, new_col, new_prev_row, new_prev_col
        test = self.ms.take_step(row, col, prev_row, prev_col, paths, turn)
        self.assertEqual(correct, test)

    def test_break_loop(self):
        """Correctly inserts a wall to break a loop in the maze."""

        filename = "test_mazes/test_maze_022.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        self.ms.verify_maze()
        # turning right
        test_maze = self.ms.break_loop(maze, turn='right')
        correct_maze = [self.wall*7,
                        self.wall + self.path*5 + self.wall,
                        (self.wall + self.path + self.wall + self.dest +
                        self.wall + self.path + self.wall),
                        (self.wall + self.path + self.wall*3 + self.path +
                        self.wall),
                        (self.wall + self.path + self.wall + self.path*3 +
                        self.wall),
                        self.wall*3 + self.path + self.wall*3,
                        self.wall*3 + self.start + self.wall*3,
                        self.wall*7]
        self.assertEqual(correct_maze, test_maze)
        # turning left
        maze = self.ms.get_maze(filename, return_maze=True)
        self.ms.verify_maze()
        test_maze = self.ms.break_loop(maze, turn='left')
        correct_maze = [self.wall*7,
                        self.wall + self.path*5 + self.wall,
                        (self.wall + self.path + self.wall + self.dest +
                        self.wall + self.path + self.wall),
                        (self.wall + self.path + self.wall*3 + self.path +
                        self.wall),
                        (self.wall + self.path*3 + self.wall + self.path +
                        self.wall),
                        self.wall*3 + self.path + self.wall*3,
                        self.wall*3 + self.start + self.wall*3,
                        self.wall*7]
        self.assertEqual(correct_maze, test_maze)

        # testing seen_D (and partly seen_S)
        filename = "test_mazes/test_maze_023.txt"
        maze = self.ms.get_maze(filename, return_maze=True)
        self.ms.verify_maze()
        # turning right
        test_maze = self.ms.break_loop(maze, turn='right')
        correct_maze = [self.wall*7,
                        self.wall*2 + self.path*4 + self.wall,
                        (self.wall + self.dest + self.wall*3 + self.path +
                        self.wall),
                        (self.wall + self.path + self.wall*3 + self.path +
                        self.wall),
                        (self.wall + self.path*2 + self.start + self.path*2 +
                        self.wall),
                        self.wall*7]
        self.assertEqual(correct_maze, test_maze)
        # turning left
        maze = self.ms.get_maze(filename, return_maze=True)
        self.ms.verify_maze()
        test_maze = self.ms.break_loop(maze, turn='left')
        correct_maze = [self.wall*7,
                        self.wall + self.path*5 + self.wall,
                        (self.wall + self.dest + self.wall*3 + self.path +
                        self.wall),
                        self.wall*5 + self.path + self.wall,
                        (self.wall + self.path*2 + self.start + self.path*2 +
                        self.wall),
                        self.wall*7]
        self.assertEqual(correct_maze, test_maze)




if __name__ == '__main__':
    unittest.main()

